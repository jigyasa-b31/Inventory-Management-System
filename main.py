import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="inventory_db"
)

cursor = conn.cursor()



def view_products():
    cursor.execute("SELECT * FROM products")

    print("\n----- PRODUCTS -----\n")

    for row in cursor:
        print(f"ID: {row[0]}")
        print(f"Product: {row[1]}")
        print(f"Category: {row[2]}")
        print(f"Price: ₹{row[3]}")
        print(f"Stock: {row[4]}")
        print("-" * 30)



def add_product():
    name = input("Enter Product Name: ")
    category = input("Enter Category: ")
    price = float(input("Enter Price: "))
    stock = int(input("Enter Stock: "))

    query = """
    INSERT INTO products
    (product_name, category, price, stock)
    VALUES (%s, %s, %s, %s)
    """

    values = (name, category, price, stock)

    cursor.execute(query, values)
    conn.commit()

    print("Product Added Successfully!")



def update_product_stock():

    product_id = int(input("Enter Product ID: "))
    new_stock = int(input("Enter New Stock: "))

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

    product_id = int(input("Enter Product ID: "))
    quantity = int(input("Enter Purchase Quantity: "))
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



def add_sale():

    product_id = int(input("Enter Product ID: "))
    quantity = int(input("Enter Sale Quantity: "))
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



while True:

    print("\n===== Inventory Management System =====")
    print("1. View Products")
    print("2. Add Product")
    print("3. Update Product Stock")
    print("4. Delete Product")
    print("5. Add Purchase")
    print("6. Add Sale")
    print("7. Exit")

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
        print("Exiting Program...")
        break

    else:
        print("Invalid Choice! Try Again.")