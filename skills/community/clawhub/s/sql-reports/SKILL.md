# SQL Reports

Query Delivery Orders from SQL Server and generate delivery reports for business analysis.

## Overview

This skill connects to a SQL Server database to extract and analyze delivery order data. It's designed for warehouse managers and logistics teams who need quick access to delivery statistics without writing SQL queries manually.

## Database Connection

- **Server:** LTEDP056\SQLEXPRESS
- **Port:** 1433
- **Database:** DeliveryDB
- **Driver:** ODBC Driver 17 for SQL Server

## Prerequisites

1. Python 3.8+ installed
2. pyodbc library installed: `pip install pyodbc`
3. ODBC Driver 17 for SQL Server installed on Windows
4. Network access to LTEDP056 server on port 1433

## Available Queries

### 1. summary_by_month
Returns monthly delivery summary with total orders, revenue, and delivery status breakdown.

**Output:** Table with Month, TotalOrders, TotalRevenue, Delivered, Pending, Cancelled columns

### 2. monthly_comparison
Compare delivery performance between two months.

**Input:** Month1 (YYYY-MM), Month2 (YYYY-MM)
**Output:** Side-by-side comparison table

### 3. quarterly_report
Generate comprehensive quarterly delivery report with trends.

**Input:** Year (YYYY), Quarter (1-4)
**Output:** Detailed report with weekly breakdown

### 4. summary_by_year
Annual delivery summary with year-over-year growth metrics.

**Input:** Year (YYYY)
**Output:** Annual statistics and growth indicators

## Usage

Run from command line:
```bash
python query.py summary_by_month
python query.py monthly_comparison 2025-01 2025-02
python query.py quarterly_report 2025 1
python query.py summary_by_year 2025