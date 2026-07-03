-- Sample SQLite schema for sql-buddy demo
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(200) UNIQUE NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    parent_id INTEGER REFERENCES categories(id)
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    category_id INTEGER REFERENCES categories(id),
    stock INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id),
    total DECIMAL(12,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    paid_at DATETIME
);

CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    price DECIMAL(10,2) NOT NULL
);

-- Insert sample data
INSERT INTO users (name, email, status) VALUES 
    ('Alice', 'alice@example.com', 'active'),
    ('Bob', 'bob@example.com', 'active'),
    ('Charlie', 'charlie@example.com', 'inactive');

INSERT INTO categories (name) VALUES 
    ('Electronics'), ('Clothing'), ('Books'), ('Home & Garden');

INSERT INTO products (name, price, category_id, stock) VALUES
    ('Smartphone', 5999.00, 1, 50),
    ('Laptop', 12999.00, 1, 30),
    ('T-Shirt', 99.00, 2, 200),
    ('JavaScript Guide', 79.00, 3, 150),
    ('Plant Pot', 29.00, 4, 100);

INSERT INTO orders (user_id, total, status) VALUES
    (1, 6098.00, 'paid'),
    (2, 12999.00, 'paid'),
    (1, 79.00, 'pending'),
    (3, 29.00, 'paid');

INSERT INTO order_items (order_id, product_id, quantity, price) VALUES
    (1, 1, 1, 5999.00),
    (1, 3, 1, 99.00),
    (2, 2, 1, 12999.00),
    (3, 4, 1, 79.00),
    (4, 5, 1, 29.00);
