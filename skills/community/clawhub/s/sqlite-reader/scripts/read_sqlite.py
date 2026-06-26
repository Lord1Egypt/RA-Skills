#!/usr/bin/env python3
# read_sqlite.py - A utility to read and query SQLite databases

import sqlite3
import sys
import argparse
import json
import csv
import os

def list_tables(conn):
    """List all tables in the database"""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    return [table[0] for table in tables]

def get_table_schema(conn, table_name):
    """Get schema information for a specific table"""
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    
    schema = []
    for col in columns:
        schema.append({
            'cid': col[0],
            'name': col[1],
            'type': col[2],
            'notnull': bool(col[3]),
            'dflt_value': col[4],
            'pk': bool(col[5])
        })
    
    # Get indexes
    cursor.execute(f"PRAGMA index_list({table_name});")
    indexes = cursor.fetchall()
    
    return {
        'table_name': table_name,
        'columns': schema,
        'indexes': [{'seq': idx[0], 'name': idx[1], 'unique': bool(idx[2]), 'origin': idx[3], 'partial': bool(idx[4])} for idx in indexes]
    }

def execute_query(conn, query, limit=None):
    """Execute a SQL query and return results"""
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        if limit:
            rows = cursor.fetchmany(limit)
        else:
            rows = cursor.fetchall()
        
        # Get column names
        columns = [description[0] for description in cursor.description]
        
        return {
            'columns': columns,
            'rows': rows,
            'rowcount': cursor.rowcount
        }
    except Exception as e:
        return {'error': str(e)}

def export_to_csv(data, filename):
    """Export query results to CSV file"""
    if not data.get('rows') or not data.get('columns'):
        return False
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data['columns'])
            for row in data['rows']:
                writer.writerow(row)
        return True
    except Exception as e:
        print(f"Error writing CSV: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='SQLite database reader')
    parser.add_argument('database', help='Path to SQLite database file')
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list-tables', action='store_true', help='List all tables')
    group.add_argument('--schema', metavar='TABLE', help='Show schema for specified table')
    group.add_argument('--query', metavar='SQL', help='Execute SQL query')
    group.add_argument('--export-csv', metavar='FILENAME', help='Export query results to CSV (requires --query)')
    
    parser.add_argument('--limit', type=int, help='Limit number of rows returned')
    
    args = parser.parse_args()
    
    # Check if database file exists
    if not os.path.exists(args.database):
        print(f"Error: Database file '{args.database}' not found.")
        sys.exit(1)
    
    try:
        conn = sqlite3.connect(args.database)
        
        if args.list_tables:
            tables = list_tables(conn)
            print("Tables in database:")
            for i, table in enumerate(tables, 1):
                print(f"{i:2d}. {table}")
                
        elif args.schema:
            schema = get_table_schema(conn, args.schema)
            print(f"Schema for table '{schema['table_name']}':")
            print("\nColumns:")
            for col in schema['columns']:
                pk_marker = " (PK)" if col['pk'] else ""
                null_marker = " NOT NULL" if col['notnull'] else ""
                default = f" DEFAULT {col['dflt_value']}" if col['dflt_value'] else ""
                print(f"  {col['cid']:2d}. {col['name']:<20} {col['type']:<12}{null_marker}{default}{pk_marker}")
            
            if schema['indexes']:
                print("\nIndexes:")
                for idx in schema['indexes']:
                    unique = " UNIQUE" if idx['unique'] else ""
                    print(f"  {idx['name']:<20}{unique} (origin: {idx['origin']})")
        
        elif args.query:
            result = execute_query(conn, args.query, args.limit)
            if 'error' in result:
                print(f"Query error: {result['error']}")
                sys.exit(1)
            
            print(f"Query: {args.query}")
            print(f"Rows returned: {len(result['rows'])}")
            
            if result['rows']:
                # Print header
                header = " | ".join([f"{col:<15}" for col in result['columns']])
                print("-" * len(header))
                print(header)
                print("-" * len(header))
                
                # Print rows
                for row in result['rows']:
                    row_str = " | ".join([f"{str(cell)[:15]:<15}" for cell in row])
                    print(row_str)
            
            # Export to CSV if requested
            if args.export_csv:
                if export_to_csv(result, args.export_csv):
                    print(f"\nData exported to: {args.export_csv}")
                else:
                    print(f"\nFailed to export to CSV: {args.export_csv}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()