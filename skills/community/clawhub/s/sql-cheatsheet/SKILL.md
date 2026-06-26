---
name: sql-cheatsheet
description: Comprehensive SQL cheatsheet with SELECT, JOINs, INSERT/UPDATE/DELETE, aggregation, window functions, subqueries, and best practices. Use when needing quick reference for SQL queries, database operations, or common query patterns.
---

# SQL Cheatsheet

Quick reference for SQL queries and database operations.

---

## 📖 Basic SELECT

### Retrieve Data
```sql
-- Select all columns
SELECT * FROM table_name;

-- Select specific columns
SELECT column1, column2 FROM table_name;

-- Select with alias
SELECT column1 AS alias1, column2 AS alias2 FROM table_name;

-- Distinct values
SELECT DISTINCT column FROM table_name;

-- Limit results
SELECT * FROM table_name LIMIT 10;

-- MySQL/PostgreSQL LIMIT with offset
SELECT * FROM table_name LIMIT 10 OFFSET 20;

-- SQL Server TOP
SELECT TOP 10 * FROM table_name;
```

### WHERE Clause
```sql
-- Equality
SELECT * FROM table WHERE column = 'value';

-- Comparison
SELECT * FROM table WHERE column > 100;
SELECT * FROM table WHERE column <= 50;

-- Multiple conditions
SELECT * FROM table WHERE column1 = 'a' AND column2 > 10;
SELECT * FROM table WHERE column1 = 'a' OR column2 > 10;

-- IN clause
SELECT * FROM table WHERE column IN ('a', 'b', 'c');

-- BETWEEN
SELECT * FROM table WHERE column BETWEEN 1 AND 100;

-- LIKE (pattern matching)
SELECT * FROM table WHERE column LIKE 'prefix%';  -- Starts with
SELECT * FROM table WHERE column LIKE '%suffix';  -- Ends with
SELECT * FROM table WHERE column LIKE '%contains%';  -- Contains
SELECT * FROM table WHERE column LIKE '_attern';  -- Single char wildcard

-- IS NULL / IS NOT NULL
SELECT * FROM table WHERE column IS NULL;
SELECT * FROM table WHERE column IS NOT NULL;

-- NOT
SELECT * FROM table WHERE column NOT IN ('a', 'b');
```

### ORDER BY
```sql
-- Ascending (default)
SELECT * FROM table ORDER BY column ASC;

-- Descending
SELECT * FROM table ORDER BY column DESC;

-- Multiple columns
SELECT * FROM table ORDER BY column1 ASC, column2 DESC;
```

---

## 🔗 JOINs

### INNER JOIN (intersection)
```sql
SELECT a.*, b.*
FROM table_a a
INNER JOIN table_b b ON a.id = b.a_id;
```

### LEFT JOIN (all from left)
```sql
SELECT a.*, b.*
FROM table_a a
LEFT JOIN table_b b ON a.id = b.a_id;
```

### RIGHT JOIN (all from right)
```sql
SELECT a.*, b.*
FROM table_a a
RIGHT JOIN table_b b ON a.id = b.a_id;
```

### FULL OUTER JOIN (all from both)
```sql
-- PostgreSQL, SQL Server
SELECT a.*, b.*
FROM table_a a
FULL OUTER JOIN table_b b ON a.id = b.a_id;
```

### CROSS JOIN (cartesian product)
```sql
SELECT a.*, b.*
FROM table_a a
CROSS JOIN table_b b;
```

### SELF JOIN
```sql
SELECT a.name, b.name AS manager_name
FROM employees a
LEFT JOIN employees b ON a.manager_id = b.id;
```

### Multiple JOINs
```sql
SELECT o.*, c.name, p.product_name
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id
INNER JOIN products p ON o.product_id = p.id;
```

---

## ➕ Aggregation

### COUNT, SUM, AVG, MIN, MAX
```sql
-- Count rows
SELECT COUNT(*) FROM table;

-- Count non-null values
SELECT COUNT(column) FROM table;

-- Sum
SELECT SUM(column) FROM table;

-- Average
SELECT AVG(column) FROM table;

-- Minimum
SELECT MIN(column) FROM table;

-- Maximum
SELECT MAX(column) FROM table;
```

### GROUP BY
```sql
-- Group by one column
SELECT category, COUNT(*)
FROM products
GROUP BY category;

-- Group by multiple columns
SELECT category, status, COUNT(*), SUM(price)
FROM products
GROUP BY category, status;

-- With WHERE (filter before grouping)
SELECT category, COUNT(*)
FROM products
WHERE price > 100
GROUP BY category;
```

### HAVING (filter after grouping)
```sql
SELECT category, COUNT(*) as product_count
FROM products
GROUP BY category
HAVING COUNT(*) > 10;

-- HAVING with WHERE
SELECT category, COUNT(*)
FROM products
WHERE price > 100
GROUP BY category
HAVING COUNT(*) > 5;
```

### GROUP BY + ORDER BY
```sql
SELECT category, SUM(price) as total
FROM products
GROUP BY category
ORDER BY total DESC;
```

---

## ➡️ Window Functions

### Basic Window
```sql
-- Row number
SELECT
  name,
  department,
  salary,
  ROW_NUMBER() OVER (ORDER BY salary DESC) as rank
FROM employees;

-- Partition by department
SELECT
  name,
  department,
  salary,
  ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as dept_rank
FROM employees;
```

### Ranking Functions
```sql
-- ROW_NUMBER: unique number, no ties
ROW_NUMBER() OVER (ORDER BY salary DESC)

-- RANK: gaps in ranking for ties
RANK() OVER (ORDER BY salary DESC)

-- DENSE_RANK: no gaps for ties
DENSE_RANK() OVER (ORDER BY salary DESC)

-- NTILE: divide into buckets
NTILE(4) OVER (ORDER BY salary DESC) as quartile
```

### Aggregate Window Functions
```sql
SELECT
  name,
  department,
  salary,
  AVG(salary) OVER (PARTITION BY department) as dept_avg,
  SUM(salary) OVER (PARTITION BY department) as dept_total
FROM employees;
```

### Running Total / Cumulative Sum
```sql
SELECT
  date,
  amount,
  SUM(amount) OVER (ORDER BY date) as running_total
FROM transactions;
```

---

## 📝 Subqueries & CTEs

### Subquery in WHERE
```sql
SELECT *
FROM products
WHERE price > (SELECT AVG(price) FROM products);
```

### Subquery in FROM
```sql
SELECT avg_price
FROM (
  SELECT category, AVG(price) as avg_price
  FROM products
  GROUP BY category
) AS category_avg
WHERE avg_price > 100;
```

### Subquery in SELECT
```sql
SELECT
  name,
  (SELECT COUNT(*) FROM orders WHERE orders.customer_id = customers.id) as order_count
FROM customers;
```

### EXISTS / NOT EXISTS
```sql
SELECT *
FROM customers c
WHERE EXISTS (
  SELECT 1 FROM orders o
  WHERE o.customer_id = c.id
);
```

### Common Table Expressions (CTE)
```sql
WITH category_stats AS (
  SELECT
    category,
    COUNT(*) as count,
    AVG(price) as avg_price
  FROM products
  GROUP BY category
)
SELECT * FROM category_stats
WHERE count > 10;
```

### Recursive CTE
```sql
WITH RECURSIVE employee_hierarchy AS (
  -- Anchor member
  SELECT id, name, manager_id, 1 as level
  FROM employees
  WHERE manager_id IS NULL

  UNION ALL

  -- Recursive member
  SELECT e.id, e.name, e.manager_id, eh.level + 1
  FROM employees e
  JOIN employee_hierarchy eh ON e.manager_id = eh.id
)
SELECT * FROM employee_hierarchy;
```

---

## ✏️ Modify Data

### INSERT
```sql
-- Insert single row
INSERT INTO table (column1, column2)
VALUES ('value1', 'value2');

-- Insert multiple rows
INSERT INTO table (column1, column2)
VALUES
  ('value1', 'value2'),
  ('value3', 'value4');

-- Insert from another table
INSERT INTO table2 (column1, column2)
SELECT column1, column2 FROM table1 WHERE condition;
```

### UPDATE
```sql
-- Update all rows (careful!)
UPDATE table
SET column1 = 'new_value';

-- Update specific rows
UPDATE table
SET column1 = 'new_value'
WHERE condition;

-- Update multiple columns
UPDATE table
SET column1 = 'value1', column2 = 'value2'
WHERE condition;

-- Update with join (PostgreSQL)
UPDATE products p
SET price = price * 1.1
FROM categories c
WHERE p.category_id = c.id AND c.name = 'Electronics';
```

### DELETE
```sql
-- Delete all rows (careful!)
DELETE FROM table;

-- Delete specific rows
DELETE FROM table WHERE condition;

-- Delete with subquery
DELETE FROM products
WHERE category_id NOT IN (SELECT id FROM categories);
```

### TRUNCATE (faster than DELETE for all rows)
```sql
TRUNCATE TABLE table_name;
```

---

## 🏗️ Schema Operations

### CREATE TABLE
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  is_active BOOLEAN DEFAULT TRUE
);

-- With foreign key
CREATE TABLE orders (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  total DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### ALTER TABLE
```sql
-- Add column
ALTER TABLE table ADD COLUMN new_column VARCHAR(100);

-- Modify column
ALTER TABLE table ALTER COLUMN column TYPE VARCHAR(200);

-- Rename column
ALTER TABLE table RENAME COLUMN old_name TO new_name;

-- Drop column
ALTER TABLE table DROP COLUMN column;

-- Add constraint
ALTER TABLE table ADD CONSTRAINT constraint_name UNIQUE (column);
```

### DROP TABLE
```sql
DROP TABLE table_name;

-- Drop if exists
DROP TABLE IF EXISTS table_name;
```

### CREATE INDEX
```sql
-- Basic index
CREATE INDEX idx_table_column ON table(column);

-- Composite index
CREATE INDEX idx_table_col1_col2 ON table(column1, column2);

-- Unique index
CREATE UNIQUE INDEX idx_table_column ON table(column);

-- Drop index
DROP INDEX idx_table_column;
```

---

## 💡 Useful Patterns

### Pagination
```sql
-- PostgreSQL, MySQL
SELECT * FROM table
ORDER BY id
LIMIT 10 OFFSET 40;  -- Page 5 (10 per page)

-- SQL Server
SELECT * FROM table
ORDER BY id
OFFSET 40 ROWS FETCH NEXT 10 ROWS ONLY;
```

### Top N Per Group
```sql
WITH ranked AS (
  SELECT
    name,
    department,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rn
  FROM employees
)
SELECT * FROM ranked WHERE rn <= 3;
```

### Find Duplicates
```sql
SELECT column, COUNT(*)
FROM table
GROUP BY column
HAVING COUNT(*) > 1;
```

### Date Functions
```sql
-- Current date/time
SELECT CURRENT_DATE;
SELECT CURRENT_TIMESTAMP;
SELECT NOW();  -- PostgreSQL

-- Extract parts
SELECT EXTRACT(YEAR FROM date_column) FROM table;
SELECT EXTRACT(MONTH FROM date_column) FROM table;

-- Date arithmetic
SELECT date_column + INTERVAL '7 days' FROM table;
SELECT DATE_ADD(date_column, INTERVAL 7 DAY) FROM table;  -- MySQL
```

### CASE Statements
```sql
SELECT
  name,
  price,
  CASE
    WHEN price < 50 THEN 'Budget'
    WHEN price < 100 THEN 'Mid-range'
    ELSE 'Premium'
  END as price_category
FROM products;
```

### COALESCE (handle NULL)
```sql
SELECT COALESCE(column, 'default_value') FROM table;
```

---

## ⚡ Performance Tips

1. **Use EXPLAIN** to understand query execution plans
2. **Index columns** used in WHERE, JOIN, and ORDER BY
3. **Avoid SELECT *** - select only needed columns
4. **Use LIMIT** to preview results
5. **Prefer UNION ALL** over UNION if duplicates don't matter
6. **Avoid functions on indexed columns** in WHERE clause
7. **Use EXISTS** instead of IN for large datasets
8. **Batch large operations** to avoid locking

**Test queries with EXPLAIN:**
```sql
EXPLAIN SELECT * FROM table WHERE condition;
EXPLAIN ANALYZE SELECT * FROM table WHERE condition;  -- PostgreSQL
```
