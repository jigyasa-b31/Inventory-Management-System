import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="inventory_db"
)

cursor = conn.cursor()

cursor.execute("SELECT * FROM products")

for row in cursor:
    print(f"ID: {row[0]}")
    print(f"Product: {row[1]}")
    print(f"Category: {row[2]}")
    print(f"Price: ₹{row[3]}")
    print(f"Stock: {row[4]}")
    print("-" * 30)