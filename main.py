import mysql.connector
from openpyxl import Workbook

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="inventory_db"
)

cursor = conn.cursor()



def view_products():

    cursor.execute("SELECT * FROM products")

    print("\n" + "=" * 45)
    print("       INVENTORY PRODUCTS")
    print("=" * 45)

    for row in cursor:

        print("-" * 40)
        print(f"ID       : {row[0]}")
        print(f"Product  : {row[1]}")
        print(f"Category : {row[2]}")
        print(f"Price    : ₹{row[3]}")
        print(f"Stock    : {row[4]}")
        print("-" * 40)



def add_product():

    try:
        name = input("Enter Product Name: ").strip()
        category = input("Enter Category: ").strip()

        if not name:
            print("Product Name cannot be empty!")
            return

        if not category:
            print("Category cannot be empty!")
            return

        price = float(input("Enter Price: "))
        stock = int(input("Enter Stock: "))

        if price < 0:
            print("Price cannot be negative!")
            return

        if stock < 0:
            print("Stock cannot be negative!")
            return

        query = """
        INSERT INTO products
        (product_name, category, price, stock)
        VALUES (%s, %s, %s, %s)
        """

        values = (name, category, price, stock)

        cursor.execute(query, values)
        conn.commit()

        print("Product Added Successfully!")

    except ValueError:
        print("Invalid Input! Please enter valid numeric values.")



def update_product_stock():

    try:
        product_id = int(input("Enter Product ID: "))
        new_stock = int(input("Enter New Stock: "))

        if new_stock < 0:
            print("Stock cannot be negative!")
            return

        query = """
        UPDATE products
        SET stock = %s
        WHERE product_id = %s
        """

        values = (new_stock, product_id)

        cursor.execute(query, values)
        conn.commit()

        if cursor.rowcount > 0:
            print("Stock Updated Successfully!")
        else:
            print("Product ID Not Found!")

    except ValueError:
        print("Invalid Input! Please enter valid numbers.")



def delete_product():

    product_id = int(input("Enter Product ID to delete: "))

    query = """
    DELETE FROM products
    WHERE product_id = %s
    """

    values = (product_id,)

    cursor.execute(query, values)
    conn.commit()

    if cursor.rowcount > 0:
        print("Product Deleted Successfully!")
    else:
        print("Product ID Not Found!")



def add_purchase():

    try:
        product_id = int(input("Enter Product ID: "))
        quantity = int(input("Enter Purchase Quantity: "))

        if quantity <= 0:
            print("Quantity must be greater than 0!")
            return

        purchase_date = input("Enter Purchase Date (YYYY-MM-DD): ")

        purchase_query = """
        INSERT INTO purchases
        (product_id, quantity, purchase_date)
        VALUES (%s, %s, %s)
        """

        purchase_values = (product_id, quantity, purchase_date)

        cursor.execute(purchase_query, purchase_values)

        stock_query = """
        UPDATE products
        SET stock = stock + %s
        WHERE product_id = %s
        """

        stock_values = (quantity, product_id)

        cursor.execute(stock_query, stock_values)

        conn.commit()

        print("Purchase Recorded Successfully!")

    except ValueError:
        print("Invalid Input! Please enter valid numbers.")



def add_sale():

    try:
        product_id = int(input("Enter Product ID: "))
        quantity = int(input("Enter Sale Quantity: "))

        if quantity <= 0:
            print("Quantity must be greater than 0!")
            return

        sale_date = input("Enter Sale Date (YYYY-MM-DD): ")

        cursor.execute(
            "SELECT stock FROM products WHERE product_id = %s",
            (product_id,)
        )

        result = cursor.fetchone()

        if result is None:
            print("Product ID Not Found!")
            return

        current_stock = result[0]

        if quantity > current_stock:
            print("Not Enough Stock Available!")
            return

        sale_query = """
        INSERT INTO sales
        (product_id, quantity, sale_date)
        VALUES (%s, %s, %s)
        """

        sale_values = (product_id, quantity, sale_date)

        cursor.execute(sale_query, sale_values)

        stock_query = """
        UPDATE products
        SET stock = stock - %s
        WHERE product_id = %s
        """

        stock_values = (quantity, product_id)

        cursor.execute(stock_query, stock_values)

        conn.commit()

        print("Sale Recorded Successfully!")

    except ValueError:
        print("Invalid Input! Please enter valid numbers.")


def low_stock_alert():

    cursor.execute("""
    SELECT product_id, product_name, stock
    FROM products
    WHERE stock < 5
    """)

    products = cursor.fetchall()

    print("\n⚠ LOW STOCK PRODUCTS ⚠\n")

    if len(products) == 0:
        print("No low stock products found.")

    else:
        for product in products:
            print(f"ID: {product[0]}")
            print(f"Product: {product[1]}")
            print(f"Stock: {product[2]}")
            print("-" * 30)


def inventory_report():

    cursor.execute("SELECT COUNT(*) FROM products")
    total_products = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(stock) FROM products")
    total_stock = cursor.fetchone()[0]

    cursor.execute("""
    SELECT product_name, stock
    FROM products
    ORDER BY stock DESC
    LIMIT 1
    """)
    highest_stock = cursor.fetchone()

    cursor.execute("""
    SELECT product_name, stock
    FROM products
    ORDER BY stock ASC
    LIMIT 1
    """)
    lowest_stock = cursor.fetchone()

    print("\n===== INVENTORY REPORT =====\n")

    print(f"Total Products: {total_products}")
    print(f"Total Stock Units: {total_stock}")

    print(f"\nHighest Stock Product: {highest_stock[0]}")
    print(f"Stock: {highest_stock[1]}")

    print(f"\nLowest Stock Product: {lowest_stock[0]}")
    print(f"Stock: {lowest_stock[1]}")

    print("\n============================")


def export_to_excel():

    cursor.execute("""
    SELECT product_id, product_name, category, price, stock
    FROM products
    """)

    products = cursor.fetchall()

    wb = Workbook()
    ws = wb.active

    ws.title = "Inventory Report"

    ws.append([
        "Product ID",
        "Product Name",
        "Category",
        "Price",
        "Stock"
    ])

    for product in products:
        ws.append(product)

    wb.save("inventory_report.xlsx")

    print("Excel Report Exported Successfully!")


def search_product():

    name = input("Enter Product Name: ")

    query = """
    SELECT *
    FROM products
    WHERE product_name = %s
    """

    cursor.execute(query, (name,))
    result = cursor.fetchone()

    if result:
        print("\n----- PRODUCT FOUND -----")
        print(f"ID: {result[0]}")
        print(f"Product: {result[1]}")
        print(f"Category: {result[2]}")
        print(f"Price: ₹{result[3]}")
        print(f"Stock: {result[4]}")
        print("-" * 30)

    else:
        print("Product Not Found!")


def purchase_history():

    query = """
    SELECT *
    FROM purchases
    ORDER BY purchase_date DESC
    """

    cursor.execute(query)

    purchases = cursor.fetchall()

    print("\n===== PURCHASE HISTORY =====\n")

    if len(purchases) == 0:
        print("No Purchase Records Found.")

    else:
        for purchase in purchases:

            print(f"Purchase ID: {purchase[0]}")
            print(f"Product ID : {purchase[1]}")
            print(f"Quantity   : {purchase[2]}")
            print(f"Date       : {purchase[3]}")
            print("-" * 30)


def sales_history():

    query = """
    SELECT *
    FROM sales
    ORDER BY sale_date DESC
    """

    cursor.execute(query)

    sales = cursor.fetchall()

    print("\n===== SALES HISTORY =====\n")

    if len(sales) == 0:
        print("No Sales Records Found.")

    else:
        for sale in sales:

            print(f"Sale ID    : {sale[0]}")
            print(f"Product ID : {sale[1]}")
            print(f"Quantity   : {sale[2]}")
            print(f"Date       : {sale[3]}")
            print("-" * 30)



while True:

    print("\n" + "=" * 50)
    print("     INVENTORY MANAGEMENT SYSTEM")
    print("=" * 50)

    print("1.  View Products")
    print("2.  Add Product")
    print("3.  Update Product Stock")
    print("4.  Delete Product")
    print("5.  Add Purchase")
    print("6.  Add Sale")
    print("7.  Low Stock Alert")
    print("8.  Inventory Report")
    print("9.  Export Inventory to Excel")
    print("10. Search Product")
    print("11. Purchase History")
    print("12. Sales History")
    print("13. Exit")

    print("=" * 50)

    choice = input("\nEnter your choice: ")

    if choice == "1":
        view_products()

    elif choice == "2":
        add_product()

    elif choice == "3":
        update_product_stock()

    elif choice == "4":
        delete_product()

    elif choice == "5":
        add_purchase()

    elif choice == "6":
        add_sale()

    elif choice == "7":
        low_stock_alert()

    elif choice == "8":
        inventory_report()

    elif choice == "9":
        export_to_excel()

    elif choice == "10":
        search_product()

    elif choice == "11":
        purchase_history()

    elif choice == "12":
        sales_history()

    elif choice == "13":
        print("Exiting Program...")
        break

    else:
        print("Invalid Choice! Try Again.")