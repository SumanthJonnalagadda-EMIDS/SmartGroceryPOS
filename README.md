## 🧑‍💼 SmartGroceryPOS – Customer Billing System
If you are using Jupyter Notebook
Basing_Jupyter_Grocery_App:
  -grocery.ipynb: "📓 Interactive Jupyter Notebook version"
  -items.csv: "🧺 Item list with prices"
  -invoice_records.csv: "🧾 Automatically created after purchase"
  -feedback_records.csv: "💬 Automatically Stores customer feedback"

SmartGroceryPOS:
  -app.py: "🐍 Terminal-based executable Python script"
  -items.csv: "🧺 Main inventory file with item names and prices"
  -invoice_records.csv: "🧾 Automatically created file storing customer invoices"
  -feedback_records.csv: "💬 Stores customer feedback post-purchase"
  -manufacturer_items.csv: "🏭 Items added/managed by the manufacturer role"
  -shopkeeper_invoices.csv: "📦 Invoices generated when shopkeeper places orders"
  -customer_feedback.csv: "🗣️ Feedback exclusively from customer role"

### 🎯 Purpose:
This project simulates how a **customer shops** at a virtual grocery store using the terminal.  
It supports item selection, cart editing, invoice generation with tax, and feedback — all recorded in CSV files.

---
## 👥 Role in This Module:
### 🛒 Customer
- 🔹 Enters their name
- 🔹 Views available items with prices
- 🔹 Can:
  - Add items to cart
  - Save items for later
  - Edit cart (change quantity or remove)
- 🔹 Proceeds to payment
- 🔹 Gets a detailed invoice
- 🔹 Can provide feedback
---
## 🧩 Functional Flow (Step-by-Step)
1. **🧍 Customer Name**: Program begins by asking for the customer’s name.
2. **📦 Item List**: Reads items from `items.csv` and shows them.
3. **🛒 Add or Save Items**:
   - Type item name to **add to cart**.
   - Type `save item_name qty` to **save for later**.
   - Type `done` to **finish** adding.
4. **🧾 Edit Cart**:
   - Update quantity or remove items (`qty = 0`).
   - Move saved items to cart if needed.
5. **💳 Checkout**:
   - If cart is not empty, payment can proceed.
   - **20% Tax + ₹3 Government Tax** is applied.
6. **📄 Invoice**:
   - Shows a clean, colored receipt in terminal.
   - Stores data in `invoice_records.csv`.
7. **💬 Feedback**:
   - Prompts user for feedback post-purchase.
   - Saves it to `feedback_records.csv`.
---
## 📘 What I Learned – Concept Summary
| 🔢 Topic/Concept       | ✅ What You Learned (In Simple Words)                                                                         |
| ---------------------- | ------------------------------------------------------------------------------------------------------------ |
| `pandas`               | How to read and modify CSV files like tables using DataFrames.                                               |
| `csv` module           | Writing structured data (like invoices and feedback) into `.csv` files.                                      |
| `uuid`                 | Creating unique IDs for each transaction (like order numbers).                                               |
| `datetime`             | Getting and formatting the current date and time for records.                                                |
| `colorama`             | Making the terminal colorful and readable using colored output.                                              |
| `Dictionary`           | Storing shopping cart, saved items, and invoice info in key-value pairs.                                     |
| `Functions`            | Dividing your code into smaller blocks (like `additem()`, `display_invoice()`) to reuse and organize better. |
| `If-else` Conditions   | Making decisions in your code (e.g., valid input or not, role-based logic).                                  |
| `Loops`                | Repeating steps like asking for items until the user types `done`.                                           |
| `Input Validation`     | Making sure users give proper input like numbers or existing item names.                                     |
| File Handling          | Automatically creating and updating files like `invoice_records.csv`.                                        |
| Role-Based Design      | Managing multiple user types (Customer, Shopkeeper, Manufacturer) with different permissions and flows.      |
| Real-World Flow Design | Building an end-to-end system like a mini Point of Sale (POS) with feedback, cart management, invoice, etc.  |
| Error Handling         | Safely handling invalid inputs (wrong item name, non-number quantity, etc.).                                 |

---
## ⚠️ Edge Cases I Handled
| Edge Case                         | What Happens                                         |
|----------------------------------|------------------------------------------------------|
| ❌ Invalid item name             | Shown “item not found” message                      |
| 🔢 Non-integer quantity          | Re-prompt until valid input is given                |
| 🗑️ Quantity = 0                  | Removes item from cart or saved list                |
| ⏹️ Early `done` command          | Ends item entry safely                              |
| 🛒 Empty cart                    | Warns and stops checkout                            |
| 📁 Missing CSV files             | Files are created automatically when saving         |
| 💬 Skipped feedback              | Stores as `"Not given any feedback"`                |
| 🧹 Extra spaces in CSV columns   | Handled by `df.columns.str.strip()`                 |

## ✅ What I Practiced (in Simple Terms)
- Read items and prices from a CSV file  
- Simulate a smart grocery shopping flow  
- Apply tax logic and show invoice clearly  
- Store every transaction and feedback safely  
- Handle wrong user inputs smartly  
- Write clean and modular code using functions  
- Use colors to improve the terminal experience
