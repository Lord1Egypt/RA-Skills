# SQL Profiler ⚡

## Overview

The `sql-profiler` skill helps data engineers and developers identify and optimize performance bottlenecks in their SQL queries. It provides in-depth analysis of query plans, suggests specific optimizations, and explains complex database concepts in plain English, supporting various SQL dialects including Databricks SQL, PostgreSQL, Spark SQL, and ANSI SQL.

## Features

-   **Query Analysis:** Detects common performance anti-patterns like missing indexes, full table scans, N+1 problems, inefficient joins, and improper use of functions.
-   **EXPLAIN/EXPLAIN ANALYZE Interpretation:** Translates verbose query plan outputs into actionable insights, highlighting the most expensive operations.
-   **Optimization Suggestions:** Offers concrete, actionable recommendations for query rewrites, index creation, partitioning strategies, and other performance enhancements.
-   **Before/After Examples:** Provides clear examples of inefficient queries and their optimized counterparts.
-   **Multi-Dialect Support:** Understands and profiles SQL for:
    -   Databricks SQL
    -   PostgreSQL
    -   Spark SQL
    -   ANSI SQL (general standard)
-   **Performance Impact Estimation:** Where possible, estimates the potential performance gains from applying suggested optimizations.

## Usage

The `sql-profiler` skill is invoked with the `/sql-profiler` command, followed by a subcommand and relevant arguments.

### `analyze` - Analyze a SQL query for performance issues

Analyzes a given SQL query and identifies potential performance bottlenecks.

**Syntax:**
`/sql-profiler analyze --query "SELECT * FROM my_table WHERE ..." [--dialect postgresql|databricks|sparksql|ansi] [--explain-output "ACTUAL EXPLAIN OUTPUT HERE"]`

**Arguments:**
-   `--query` (required): The SQL query string to analyze.
-   `--dialect` (optional): The SQL dialect. Supported: `postgresql`, `databricks`, `sparksql`, `ansi`. Defaults to `ansi` if not specified.
-   `--explain-output` (optional): The output from `EXPLAIN` or `EXPLAIN ANALYZE` for the query. Providing this significantly improves the accuracy and depth of the analysis.

**Example:**
```
/sql-profiler analyze --query "SELECT customer_name, SUM(order_total) FROM orders GROUP BY customer_name ORDER BY SUM(order_total) DESC LIMIT 10;" --dialect postgresql
```

**Example with EXPLAIN output:**
```
/sql-profiler analyze --query "SELECT * FROM large_table WHERE created_at < '2023-01-01' AND status = 'active';" --dialect databricks --explain-output "== Physical Plan ==
*(1) Project [id#123, created_at#124, status#125]
+- *(1) Filter (isnotnull(created_at#124) AND (created_at#124 < 2023-01-01) AND isnotnull(status#125) AND (status#125 = active))
   +- *(1) FileScan csv [id#123, created_at#124, status#125] Batched: false, DataFilters: [isnotnull(created_at#124), (created_at#124 < 2023-01-01), isnotnull(status#125), (status#125 = active)], Format: CSV, Location: InMemoryFileIndex[dbfs:/user/hive/warehouse/large_table], PartitionFilters: [], PushedFilters: [IsNotNull(created_at), LessThan(created_at,2023-01-01), IsNotNull(status), EqualTo(status,active)], ReadSchema: struct<id:string,created_at:timestamp,status:string>
"
```

**Output:**
The command will return a detailed analysis including:
-   **Identified Issues:** A list of potential performance problems.
-   **Explanation:** A plain English explanation of *why* each issue is a problem.
-   **Suggestions:** Specific recommendations for optimizing the query.
-   **Before/After:** Code examples demonstrating the original and optimized query (if applicable).
-   **Estimated Impact:** A qualitative or quantitative estimate of performance improvement.

### `explain-plan` - Interpret EXPLAIN/EXPLAIN ANALYZE output

Provides a human-readable interpretation of a raw `EXPLAIN` or `EXPLAIN ANALYZE` output.

**Syntax:**
`/sql-profiler explain-plan --output "RAW EXPLAIN OUTPUT HERE" [--dialect postgresql|databricks|sparksql|ansi]`

**Arguments:**
-   `--output` (required): The full text output from an `EXPLAIN` or `EXPLAIN ANALYZE` command.
-   `--dialect` (optional): The SQL dialect the EXPLAIN output belongs to. Defaults to `ansi`.

**Example:**
```
/sql-profiler explain-plan --output "Aggregate  (cost=250.75..250.76 rows=1 width=36) (actual time=0.089..0.089 rows=1 loops=1)
  ->  Sort  (cost=250.75..250.76 rows=1 width=36) (actual time=0.088..0.088 rows=1 loops=1)
        Sort Key: (sum(orders.order_total)) DESC
        Sort Method: quicksort  Memory: 25kB
        ->  HashAggregate  (cost=250.72..250.73 rows=1 width=36) (actual time=0.082..0.082 rows=1 loops=1)
              Group Key: orders.customer_name
              Batches: 1  Memory Usage: 24kB
              ->  Seq Scan on orders  (cost=0.00..200.00 rows=10000 width=16) (actual time=0.003..0.024 rows=10000 loops=1)
" --dialect postgresql
```

**Output:**
A plain English breakdown of the query plan, highlighting:
-   The most expensive operations (e.g., full table scans, sorts, hash joins).
-   Why these operations are costly.
-   Recommendations to reduce their impact.

### `optimize` - Get specific optimization suggestions for a query

Directly asks for optimization suggestions for a query without full analysis, assuming common issues.

**Syntax:**
`/sql-profiler optimize --query "SELECT * FROM customers WHERE region = 'EMEA';" [--dialect postgresql|databricks|sparksql|ansi]`

**Arguments:**
-   `--query` (required): The SQL query to optimize.
-   `--dialect` (optional): The SQL dialect. Defaults to `ansi`.

**Example:**
```
/sql-profiler optimize --query "SELECT o.order_id, c.customer_name FROM orders o JOIN customers c ON o.customer_id = c.customer_id WHERE c.registration_date < '2022-01-01';" --dialect sparksql
```

**Output:**
-   **Suggestions:** A list of direct optimization tips, potentially including index recommendations, join order changes, or query rewrites.
-   **Before/After:** Code examples for rewrites.
-   **Rationale:** Brief explanation of why the suggestion improves performance.

## Core Concepts Explained

### Missing Indexes
**Problem:** When a database needs to find specific rows based on conditions in `WHERE` clauses, `JOIN` conditions, or `ORDER BY` clauses, it often performs a "full table scan" (reads every row). This is slow for large tables.
**Solution:** Creating an index on the columns used in these conditions allows the database to quickly jump to the relevant rows, similar to using an index in a book.
**Impact:** Can dramatically reduce query execution time, especially for large tables and selective queries.

### Full Table Scans
**Problem:** Reading every single row in a table to find a small subset of data. This is inefficient.
**Solution:** Often solved by adding appropriate indexes, partitioning large tables, or rewriting queries to filter earlier.
**Impact:** Avoids unnecessary I/O and CPU usage, leading to faster queries.

### N+1 Problem
**Problem:** Occurs when an application executes N additional queries for each result of an initial query. For example, fetching a list of users, then for each user, fetching their associated orders in separate queries.
**Solution:** Use `JOIN` operations, `IN` clauses, or subqueries to fetch all related data in a single, more efficient query. In some ORMs, "eager loading" helps.
**Impact:** Reduces the number of round trips to the database, significantly speeding up data retrieval.

### Bad Joins (Cross Joins, Inefficient Join Order)
**Problem:**
-   **Cross Join (unintentional):** Occurs when join conditions are missing or incorrect, resulting in a Cartesian product (every row from table A joined with every row from table B). This generates huge result sets and can crash databases.
-   **Inefficient Join Order:** Databases try to optimize join order, but sometimes a specific order (e.g., filtering a large table *before* joining with another) is much more efficient.
**Solution:**
-   Always specify explicit join conditions (`ON clause`).
-   Consider the cardinality and size of tables when joining. Filter small tables or highly selective conditions first.
-   Use `EXPLAIN` to see the join order and adjust if necessary (e.g., using hints, though generally not recommended unless absolutely needed).
**Impact:** Correct joins prevent performance disasters and ensure data accuracy. Optimized join order can significantly reduce intermediate result set sizes.

## Databricks SQL / Spark SQL Specifics

Databricks SQL and Spark SQL operate on a distributed architecture. Optimizations often involve:
-   **Data Skew:** Uneven distribution of data, causing some tasks to take much longer. Handled by salting keys, repartitioning, or using `BROADCAST` hints for small tables.
-   **Shuffle Operations:** Data movement across the network, which is expensive. Minimizing shuffles through efficient `JOIN` strategies, `GROUP BY`, and `ORDER BY` clauses is crucial.
-   **Caching:** Caching frequently accessed tables or intermediate results in memory can speed up subsequent queries.
-   **File Formats:** Using columnar formats like Parquet or Delta Lake is crucial for performance due to predicate pushdown and column pruning.
-   **Z-Ordering:** For Delta Lake, `OPTIMIZE ... ZORDER BY` helps colocate related data in the same set of files, reducing the amount of data read for queries with high-cardinality columns.

## PostgreSQL Specifics

PostgreSQL is a powerful relational database. Key optimizations include:
-   **Indexes:** B-tree, Hash, GIN, GiST, BRIN indexes for various data types and query patterns.
-   **`VACUUM` and `ANALYZE`:** Regularly running these commands helps the query planner make accurate decisions and reclaims space from dead tuples.
-   **`WITH` clauses (CTEs):** Can improve readability but sometimes prevent the optimizer from pushing down predicates, leading to materialized CTEs that are less efficient.
-   **Partitioning:** For very large tables, declarative partitioning can greatly improve performance by allowing queries to scan only relevant partitions.
-   **Prepared Statements:** Reduce parsing overhead for frequently executed queries.

## ANSI SQL (General Best Practices)

-   **Select only necessary columns:** Avoid `SELECT *`.
-   **Filter early:** Use `WHERE` clauses to reduce data before joins or aggregations.
-   **Avoid functions in `WHERE` clauses on indexed columns:** `WHERE YEAR(date_column) = 2023` prevents index usage. Instead, `WHERE date_column BETWEEN '2023-01-01' AND '2023-12-31'`.
-   **Understand `UNION` vs `UNION ALL`:** `UNION` implies a distinct sort, `UNION ALL` does not. Use `UNION ALL` if duplicates are acceptable and performance is critical.
-   **Subqueries vs. Joins:** Often, `JOIN`s are more performant than correlated subqueries.
-   **Use `LIMIT` with `ORDER BY`:** If you only need a few rows, combine `LIMIT` with an `ORDER BY` to return the most relevant data efficiently.

## Disclaimer

The `sql-profiler` skill provides AI-driven suggestions. While highly effective, it's crucial to:
1.  **Test all optimizations:** Apply suggestions to a staging environment and measure actual performance impact.
2.  **Understand your data:** The best optimization depends on your specific data distribution, query patterns, and system architecture.
3.  **Consult documentation:** Refer to the official documentation for your specific SQL dialect for advanced tuning.

This skill is a powerful assistant, not a replacement for human expertise and rigorous testing.

## Contributing

Found a bug or have a suggestion? Open an issue or submit a pull request on the ClawHub repository.

## License

MIT License.
