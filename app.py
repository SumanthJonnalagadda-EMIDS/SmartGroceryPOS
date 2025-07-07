import pandas as pd
import os
import csv
import uuid
from datetime import datetime
from colorama import Fore, Style, init
init(autoreset=True)

# --------- Utility Functions ---------


def log_action(file_name, actor, action, item=None, extra=None):
    data = {
        'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Actor': actor,
        'Action': action,
        'Item': item,
        'Details': extra
    }
    file_exists = os.path.isfile(file_name)
    with open(file_name, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

# --------- Display Invoice ---------


def display_invoice(actor, name, invoice_data, cart_data):
    print("\n" + Fore.YELLOW + Style.BRIGHT + "🧾 INVOICE RECEIPT".center(60))
    print(Fore.LIGHTMAGENTA_EX + "=" * 60)
    print(Fore.CYAN + Style.BRIGHT + f"{'FINAL INVOICE':^60}")
    print(Fore.LIGHTMAGENTA_EX + "=" * 60)
    print(Fore.WHITE + f"{actor + ' Name:':<20} {Fore.LIGHTGREEN_EX}{name}")
    print(
        f"{'Transaction ID:':<20} {Fore.LIGHTGREEN_EX}{invoice_data['Transaction ID']}")
    print(f"{'Date & Time:':<20} {Fore.LIGHTGREEN_EX}{invoice_data['Date']}")

    print(Fore.LIGHTMAGENTA_EX + "-" * 60)
    print(Fore.LIGHTCYAN_EX + Style.BRIGHT +
          f"{'Item':<20}{'Qty':<10}{'Price (₹)':<10}{'Total (₹)'}")
    print(Fore.LIGHTMAGENTA_EX + "-" * 60)

    for item, qty in cart_data.items():
        price = int(invoice_data['Prices'][item])
        item_total = price * qty
        print(Fore.WHITE + f"{item:<20}{qty:<10}{price:<10}{item_total}")

    print(Fore.LIGHTMAGENTA_EX + "-" * 60)
    print(Fore.YELLOW + f"{'Subtotal:':<48} ₹{invoice_data['Subtotal']}")
    print(Fore.YELLOW + f"{'Tax (20%):':<48} ₹{invoice_data['Tax']}")
    print(Fore.YELLOW + f"{'Gov. Tax:':<48} ₹{invoice_data['Gov Tax']}\n")
    print(Fore.LIGHTMAGENTA_EX + "=" * 60)
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT +
          f"{'TOTAL PAID:':<48} ₹{invoice_data['Total Amount']}")
    print(Fore.LIGHTMAGENTA_EX + "=" * 60)
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT +
          "\n👏 Thank you! Have a nice day! 👏\n")

    invoice_file = f"{actor.lower()}_invoices.csv"
    file_exists = os.path.isfile(invoice_file)
    with open(invoice_file, 'a', newline='') as file:
        fieldnames = ['Transaction ID', f'{actor} Name', 'Date', 'Item', 'Quantity',
                      'Price', 'Item Total', 'Subtotal', 'Tax', 'Gov Tax', 'Total Amount']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for item, qty in cart_data.items():
            writer.writerow({
                'Transaction ID': invoice_data['Transaction ID'],
                f'{actor} Name': name,
                'Date': invoice_data['Date'],
                'Item': item,
                'Quantity': qty,
                'Price': invoice_data['Prices'][item],
                'Item Total': qty * invoice_data['Prices'][item],
                'Subtotal': invoice_data['Subtotal'],
                'Tax': invoice_data['Tax'],
                'Gov Tax': invoice_data['Gov Tax'],
                'Total Amount': invoice_data['Total Amount']
            })

    feedback = input(
        Fore.CYAN + "Would you like to provide feedback? (yes/no): ").strip().lower()
    fb = input(Fore.LIGHTYELLOW_EX +
               "Please enter your feedback: ").strip() if feedback == 'yes' else "Not given"
    feedback_record = {
        'Transaction ID': invoice_data['Transaction ID'],
        f'{actor} Name': name,
        'Feedback': fb
    }
    file_exists = os.path.isfile(f'{actor.lower()}_feedback.csv')
    with open(f'{actor.lower()}_feedback.csv', 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=feedback_record.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(feedback_record)
    print(Fore.LIGHTGREEN_EX + "✅ Feedback recorded successfully!")

# --------- Shopping Flow ---------


def shopping_flow(df, actor, name, save_to_file=None):
    cart = {}
    save_for_later = {}

    print(Fore.YELLOW + "\nAvailable Items:")
    for _, row in df.iterrows():
        print(f"{row['Item']:<15} ₹{row['Price']}")

    while True:
        cmd = input("\nAdd item or 'save [item] [qty]' or 'done': ").strip()
        if cmd.lower() == 'done':
            break
        elif cmd.startswith('save'):
            try:
                _, item, qty = cmd.split()
                if item in df['Item'].values:
                    save_for_later[item] = save_for_later.get(
                        item, 0) + int(qty)
                    print(Fore.CYAN + f"💾 Saved for later: {item} x{qty}")
                else:
                    print(Fore.RED + "Item not found!")
            except:
                print(Fore.RED + "Invalid save command.")
        else:
            item = cmd
            if item in df['Item'].values:
                qty = int(input(f"Enter quantity for {item}: "))
                cart[item] = cart.get(item, 0) + qty
                print(Fore.GREEN + f"✅ Added: {item} x{qty}")
            else:
                print(Fore.RED + "Item not found!")

    if save_for_later:
        print(Fore.LIGHTMAGENTA_EX + "\n💾 Saved for Later:")
        for item, qty in save_for_later.items():
            print(f"{item:<15} Qty: {qty}")
        move = input(
            "\nDo you want to move saved items to cart? (yes/no): ").strip().lower()
        if move == 'yes':
            for item, qty in save_for_later.items():
                cart[item] = cart.get(item, 0) + qty
            save_for_later.clear()

    if not cart:
        print(Fore.YELLOW + "No items in cart.")
        return

    edit = input("Do you want to edit cart? (yes/no): ").strip().lower()
    while edit == 'yes':
        for item, qty in cart.items():
            print(f"{item:<15} Qty: {qty}")
        item_to_edit = input("Enter item to edit (or 'done'): ").strip()
        if item_to_edit == 'done':
            break
        if item_to_edit in cart:
            new_qty = int(input(f"New quantity for {item_to_edit}: "))
            cart[item_to_edit] = new_qty
        else:
            print("Item not in cart.")

    pay = input(
        "\nWould you like to proceed with the payment? (yes/no): ").strip().lower()
    if pay != 'yes':
        print(Fore.YELLOW + "Transaction cancelled.")
        return

    prices = {item: int(df[df['Item'] == item]['Price'].values[0])
              for item in cart}
    subtotal = sum(prices[i] * q for i, q in cart.items())
    tax = round(subtotal * 0.2, 2)
    gov_tax = 3
    total = subtotal + tax + gov_tax
    tid = str(uuid.uuid4())[:8]

    invoice = {
        'Transaction ID': tid,
        'Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Subtotal': subtotal,
        'Tax': tax,
        'Gov Tax': gov_tax,
        'Total Amount': total,
        'Prices': prices
    }
    display_invoice(actor, name, invoice, cart)

    if save_to_file:
        if os.path.exists(save_to_file):
            df_items = pd.read_csv(save_to_file)
        else:
            df_items = pd.DataFrame(columns=['Item', 'Price'])

        for item in cart:
            if item not in df_items['Item'].values:
                df_items = pd.concat([df_items, pd.DataFrame(
                    [{'Item': item, 'Price': prices[item]}])], ignore_index=True)

        df_items.to_csv(save_to_file, index=False)

# --------- Full Functional Flows ---------


def main():
    while True:
        print("\n🔒 Login as:")
        print("1. Shopkeeper")
        print("2. Customer")
        print("3. Manufacturer")
        print("4. Exit")
        role = input("Select role (1/2/3/4): ").strip()

        if role == '1':
            if not os.path.exists("manufacturer_items.csv"):
                print(Fore.RED + "No manufacturer items available.")
            else:
                df = pd.read_csv("manufacturer_items.csv")
                shopping_flow(df, "Shopkeeper", "Shopkeeper",
                              save_to_file="items.csv")

        elif role == '2':
            if not os.path.exists("items.csv"):
                print(Fore.RED + "No items available.")
            else:
                name = input("Enter customer name: ").strip()
                df = pd.read_csv("items.csv")
                shopping_flow(df, "Customer", name)

        elif role == '3':
            print("\n🏭 Manufacturer Menu")
            while True:
                print("1. Add Item")
                print("2. Edit Item")
                print("3. Remove Item")
                print("4. Back")
                choice = input("Choose option: ").strip()

                if choice == '1':
                    item = input("Enter item name: ").strip()
                    price = input("Enter price: ").strip()
                    df = pd.read_csv("manufacturer_items.csv") if os.path.exists(
                        "manufacturer_items.csv") else pd.DataFrame(columns=['Item', 'Price'])
                    df = pd.concat([df, pd.DataFrame([[item, price]], columns=[
                                   'Item', 'Price'])], ignore_index=True)
                    df.to_csv("manufacturer_items.csv", index=False)
                    print("✅ Item added.")

                elif choice == '2':
                    item = input("Enter item name to edit: ").strip()
                    df = pd.read_csv("manufacturer_items.csv")
                    if item in df['Item'].values:
                        price = input("Enter new price: ").strip()
                        df.loc[df['Item'] == item, 'Price'] = int(price)
                        df.to_csv("manufacturer_items.csv", index=False)
                        print("✅ Item updated.")
                    else:
                        print("❌ Item not found.")

                elif choice == '3':
                    item = input("Enter item name to remove: ").strip()
                    df = pd.read_csv("manufacturer_items.csv")
                    df = df[df['Item'] != item]
                    df.to_csv("manufacturer_items.csv", index=False)
                    print("🗑️ Item removed.")

                elif choice == '4':
                    break
                else:
                    print("Invalid option.")

        elif role == '4':
            print("👋 Exiting program...")
            break

        else:
            print("❌ Invalid option. Try again.")


if __name__ == "__main__":
    main()
