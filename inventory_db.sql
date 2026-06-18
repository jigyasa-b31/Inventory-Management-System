CREATE DATABASE inventory_db;

USE inventory_db;

CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10,2),
    stock INT DEFAULT 0
);

DESC products;

INSERT INTO products
(product_name, category, price, stock)
VALUES
('iPhone 15', 'Mobile', 79999, 10),
('Samsung S24', 'Mobile', 74999, 15),
('OnePlus 12', 'Mobile', 64999, 8);

SELECT * FROM products;

CREATE TABLE purchases (
    purchase_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    quantity INT,
    purchase_date DATE,
    FOREIGN KEY (product_id)
    REFERENCES products(product_id)
);

DESC purchases;

CREATE TABLE sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    quantity INT,
    sale_date DATE,
    FOREIGN KEY (product_id)
    REFERENCES products(product_id)
);

DESC sales;

SHOW TABLES;

INSERT INTO purchases
(product_id, quantity, purchase_date)
VALUES
(1, 5, CURDATE()),
(2, 3, CURDATE());

SELECT * FROM purchases;

INSERT INTO sales
(product_id, quantity, sale_date)
VALUES
(1, 2, CURDATE()),
(3, 1, CURDATE());

SELECT * FROM sales;

SELECT * FROM products;

SHOW TABLES;
SELECT * FROM products;
SELECT * FROM purchases;
SELECT * FROM sales;