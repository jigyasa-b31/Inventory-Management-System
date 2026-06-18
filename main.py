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

# view_products()

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

# add_product()

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

# update_product_stock()

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

# delete_product()