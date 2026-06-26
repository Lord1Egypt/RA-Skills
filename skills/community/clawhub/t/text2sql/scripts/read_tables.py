#!/usr/bin/env python3
"""
Text-to-SQL Database Table Reader Script
Function: Read database connection information from local configuration file, 
          get all table names and table structures, save as two separate JSON files,
          and optionally generate database knowledge YAML file
"""

import argparse
import sys
import os
import json
from datetime import datetime, date
from sqlalchemy import create_engine, inspect, text


def read_database_tables(config_file: str = "text-to-sql-config.json", generate_knowledge: bool = True, excel_file: str = None, output_dir: str = "./output") -> dict:
    """
    Read database connection information from local configuration file, get all table names and structures,
    save as two separate JSON files, or read data from Excel file and call API to generate knowledge file
    
    Args:
        config_file: Database configuration file path
        generate_knowledge: Whether to generate database knowledge YAML file
        excel_file: Excel file path, if provided, ignore db_url operation
        output_dir: Output directory path for generated files
        
    Returns:
        dict: Dictionary containing table list and structure information
    """
    try:
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize variables
        tables_info = {}
        normalized_table_names = []
        db_url = None
        db_name = "unknown_db"
        source_type = "database"
        
        # Handle Excel file or database
        if excel_file:
            if not os.path.exists(excel_file):
                return {
                    "success": False,
                    "message": f"Excel file {excel_file} does not exist"
                }
            
            print(f"Processing Excel file: {excel_file}")
            source_type = "excel"
            db_name = os.path.splitext(os.path.basename(excel_file))[0]
        else:
            # Check if configuration file exists
            if not os.path.exists(config_file):
                return {
                    "success": False,
                    "message": f"Configuration file {config_file} does not exist, please configure database first"
                }
            
            # Read configuration file
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            db_url = config.get("db_url")
            
            if not db_url:
                return {
                    "success": False,
                    "message": "Database URL not found in configuration file"
                }
            
            # Auto-convert mysql:// to mysql+pymysql:// for better compatibility
            if db_url.startswith('mysql://') and '+pymysql' not in db_url:
                db_url = db_url.replace('mysql://', 'mysql+pymysql://', 1)
                print(f"Auto-converted database URL to use pymysql driver")
            
            # Create database engine
            # print(db_url)
            engine = create_engine(db_url)
            # print(engine)
            # Extract database name from database URL
            def _extract_db_name(url):
                if 'mysql' in url.lower():
                    # mysql://user:pass@host:port/dbname
                    parts = url.split('/')
                    if len(parts) > 3:
                        return parts[-1].split('?')[0]  # Remove query parameters
                elif 'postgresql' in url.lower():
                    # postgresql://user:pass@host:port/dbname
                    parts = url.split('/')
                    if len(parts) > 3:
                        return parts[-1].split('?')[0]  # Remove query parameters
                return ""
            
            def _sample_table_data(engine, table_name, columns_info, sample_size=2000):
                """
                Sample row data from table
                
                Strategy: ORDER BY RAND() LIMIT sample_size
                
                Returns:
                    Dict: {column_name: {"sample_values": [], "unique_count": int, "total_count": int}, ...}
                """
                from sqlalchemy import text
                
                result = {}
                result["_row_count"] = 0
                
                try:
                    # Build query, only select needed columns
                    column_names = [col_info["name"] for col_info in columns_info]
                    if not column_names:
                        return result
                    
                    # Build safe SQL query
                    columns_str = ", ".join([f"`{col}`" for col in column_names])
                    query = f"SELECT {columns_str} FROM `{table_name}` ORDER BY RAND() LIMIT {sample_size}"
                    
                    with engine.connect() as conn:
                        db_result = conn.execute(text(query))
                        rows = db_result.fetchall()
                        # print(rows)
                        result["_row_count"] = len(rows)
                        
                        # Get query result column names
                        result_columns = db_result.keys()
                        
                        # Build column name to index mapping, case-insensitive
                        columns_map = {col.lower(): idx for idx, col in enumerate(result_columns)}
                        
                        for col_info in columns_info:
                            col_name = col_info["name"]
                            col_name_lower = col_name.lower()
                            
                            # Try to match column name (case-insensitive)
                            matched_col = None
                            for col in result_columns:
                                if col.lower() == col_name_lower:
                                    matched_col = col
                                    break
                            
                            if not matched_col:
                                continue
                            
                            col_idx = columns_map[col_name_lower]
                            sample_values = []
                            for row in rows:
                                value = row[col_idx]
                                if value is not None:
                                    # Ensure all values can be JSON serialized
                                    if isinstance(value, (datetime, date)):
                                        sample_values.append(str(value))
                                    else:
                                        try:
                                            # Try to convert value to string
                                            sample_values.append(str(value))
                                        except:
                                            # If conversion fails, add empty string
                                            sample_values.append("")
                            
                            # Ensure unique value calculation also handles serialized values
                            unique_values = set()
                            for val in sample_values:
                                unique_values.add(str(val) if isinstance(val, (datetime, date)) else val)
                            
                            result[col_name] = {
                                "sample_values": sample_values if sample_values else [],
                                "unique_count": len(unique_values) if sample_values else 0,
                                "total_count": len(sample_values)
                            }
                except Exception as e:
                    print(f"Failed to get sample data: {str(e)}")
                    # Even if error occurs, add default values for each column
                    for col_info in columns_info:
                        col_name = col_info["name"]
                        result[col_name] = {
                            "sample_values": [],
                            "unique_count": 0,
                            "total_count": 0
                        }
                
                return result
            
            db_name = _extract_db_name(db_url)
            # print(db_name)
            # Get inspector
            inspector = inspect(engine)
            # print(inspector)
            
            # Get all table names
            table_names = inspector.get_table_names()
            # print(table_names)
            # Get structure information for each table
            for table_name in table_names:
                # Normalize table name to "database.table" format
                normalized_table_name = f"{db_name}.{table_name}"
                normalized_table_names.append(normalized_table_name)
                columns = inspector.get_columns(table_name)
                
                # Try to get table comment
                table_comment = ""
                try:
                    # Get table comment (syntax varies by database)
                    if 'mysql' in db_url.lower():
                        result = engine.execute(text(f"SELECT TABLE_COMMENT FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}'"))
                        row = result.fetchone()
                        if row and row[0]:
                            table_comment = row[0]
                    elif 'postgresql' in db_url.lower():
                        result = engine.execute(text(f"SELECT obj_description('{table_name}'::regclass, 'pg_class')"))
                        row = result.fetchone()
                        if row and row[0]:
                            table_comment = row[0]
                except:
                    pass
                
                columns_info = []
                
                # Get all column comments at once
                column_comments = {}
                try:
                    if 'mysql' in db_url.lower():
                        sql = f"""
                            SELECT COLUMN_NAME, COLUMN_COMMENT 
                            FROM INFORMATION_SCHEMA.COLUMNS 
                            WHERE TABLE_NAME = '{table_name}'
                        """
                        # print(sql)
                        with engine.connect() as conn:
                            result = conn.execute(text(sql))
                            rows = result.fetchall()
                            for row in rows:
                                if row and row[1]:
                                    column_comments[row[0]] = row[1]
                    elif 'postgresql' in db_url.lower():
                        with engine.connect() as conn:
                            result = conn.execute(text(f"""
                                SELECT column_name, col_description('{table_name}'::regclass, ordinal_position)
                                FROM information_schema.columns 
                                WHERE table_name = '{table_name}'
                            """))
                            for row in result.fetchall():
                                if row and row[1]:
                                    column_comments[row[0]] = row[1]
                except:
                    pass
                
                # Build column information and add comments
                for column in columns:
                    column_info = {
                        "name": column["name"],
                        "type": str(column["type"]),
                        "nullable": column.get("nullable", True),
                        "default": str(column.get("default", "")) if column.get("default") else "",
                        "primary_key": column.get("primary_key", False),
                        "comment": column_comments.get(column["name"], "")
                    }
                    columns_info.append(column_info)
                # print(columns_info)
                # Get sample data for the table
                sample_data = _sample_table_data(engine, table_name, columns_info)
                
                # Add sample data to column information
                for col_info in columns_info:
                    col_name = col_info["name"]
                    if col_name in sample_data:
                        col_info["sample_values"] = sample_data[col_name]["sample_values"]
                        col_info["unique_count"] = sample_data[col_name]["unique_count"]
                        col_info["total_count"] = sample_data[col_name]["total_count"]
                
                tables_info[normalized_table_name] = {
                    "columns": columns_info,
                    "column_count": len(columns_info),
                    "comment": table_comment,
                    "row_count": sample_data.get("_row_count", 0)
                }
            
            engine.dispose()
            
            # Generate table name file table_info.json
            table_info_data = {
                "success": True,
                "table_count": len(normalized_table_names),
                "table_names": normalized_table_names,
                "message": "Database table names read successfully"
            }
            
            table_info_path = os.path.join(output_dir, "table_info.json")
            with open(table_info_path, 'w', encoding='utf-8') as f:
                json.dump(table_info_data, f, ensure_ascii=False, indent=2)
            
            # Generate column information file column_info.json
            column_info_data = {
                "success": True,
                "source_type": "database",
                "db_url": db_url,
                "db_name": db_name,
                "table_count": len(normalized_table_names),
                "tables": tables_info,
                "table_names": normalized_table_names,
                "message": "Database table structure read successfully"
            }
            
            column_info_path = os.path.join(output_dir, "column_info.json")
            with open(column_info_path, 'w', encoding='utf-8') as f:
                json.dump(column_info_data, f, ensure_ascii=False, indent=2)
            
            print(f"Successfully read database, total {len(normalized_table_names)} tables")
            print(f"Table name information saved to: {os.path.abspath(table_info_path)}")
            print(f"Table structure information saved to: {os.path.abspath(column_info_path)}")
            
            result = {
                "success": True,
                "source_type": "database",
                "db_url": db_url,
                "db_name": db_name,
                "table_count": len(normalized_table_names),
                "tables": tables_info,
                "table_names": normalized_table_names
            }
        
        # 统一调用接口生成知识文件
        # if generate_knowledge:
        try:
            import requests
            
            api_url = "https://asksql.ucap.com.cn/"
            generate_url = f"{api_url.rstrip('/')}/ask/api/generate_database_knowledge"
            
            print(f"Calling API to generate database knowledge...")
            
            if excel_file:
                # Pass excel_file parameter via form_data
                with open(excel_file, 'rb') as f:
                    files = {
                        'excel_file': (os.path.basename(excel_file), f)
                    }
                    data = {
                        'format': 'json',
                        'generate_knowledge': 'true'
                    }
                    
                    response = requests.post(
                        generate_url,
                        files=files,
                        data=data,
                        timeout=120
                    )
            else:
                # Database mode
                column_info = {
                    "tables": tables_info,
                    "source_type": "database",
                    "db_name": db_name
                }
                # print(column_info)
                response = requests.post(
                    generate_url,
                    json={"data": column_info, "format": "json"},
                    timeout=120
                )
            
            if response.status_code == 200:
                knowledge_data = response.json()
                knowledge_data = json.loads(knowledge_data.get("content", "{}"))
                # print(knowledge_data)
                
                # Excel mode: Initialize tables_info from knowledge_data
                if source_type == "excel":
                    old_db_name = "excel"
                    for old_table_name, table_data in knowledge_data.get("tables", {}).items():
                        new_table_name = old_table_name.replace(old_db_name, db_name, 1)
                        fields = table_data.get("fields", [])
                        columns_info = []
                        for field in fields:
                            col_info = {
                                "name": field.get("name", ""),
                                "type": field.get("type", "text"),
                                "nullable": True,
                                "default": "",
                                "primary_key": field.get("primary_key", False),
                                "comment": field.get("description", ""),
                                "ai_type": field.get("ai_context", {}).get("ai_type", ""),
                                "property": field.get("ai_context", {}).get("property", ""),
                                "value_list": field.get("ai_context", {}).get("value_list", []),
                                "is_default": field.get("ai_context", {}).get("is_default", False)
                            }
                            columns_info.append(col_info)

                        tables_info[new_table_name] = {
                            "columns": columns_info,
                            "column_count": len(columns_info),
                            "comment": "",
                            "row_count": 0
                        }
                        normalized_table_names.append(new_table_name)
                
                # First add default values for all columns
                for table_name, table_info in tables_info.items():
                    for col_info in table_info.get("columns", []):
                        col_info["ai_type"] = col_info.get("ai_type", "")
                        col_info["property"] = col_info.get("property", "")
                        col_info["value_list"] = col_info.get("value_list", [])
                
                # Update columns with values
                for table_name, table_info in knowledge_data.get("tables", {}).items():
                    # Try to match table name (may or may not have database name prefix)
                    matched_table_name = None
                    for existing_table_name in tables_info.keys():
                        if existing_table_name == table_name or existing_table_name.endswith("." + table_name):
                            matched_table_name = existing_table_name
                            break
                    
                    if matched_table_name:
                        for field in table_info.get("fields", []):
                            col_name = field.get("name")
                            for col_info in tables_info[matched_table_name].get("columns", []):
                                if col_info.get("name") == col_name:
                                    ai_context = field.get("ai_context", {})
                                    col_info["ai_type"] = ai_context.get("ai_type", "")
                                    col_info["property"] = ai_context.get("property", "")
                                    col_info["value_list"] = ai_context.get("value_list", [])
                                    col_info["is_default"] = ai_context.get("is_default", False)
                                    break
                
                # Execute SELECT DISTINCT query to get all candidate values for enum columns
                if db_url:
                    knowledge_data = enrich_from_database(db_url, knowledge_data)
                    # Sync value_list from knowledge_data["tables"] to tables_info
                    for table_name, table_info in knowledge_data.get("tables", {}).items():
                        # Try to match table name
                        matched_table_name = None
                        for existing_table_name in tables_info.keys():
                            if existing_table_name == table_name or existing_table_name.endswith("." + table_name):
                                matched_table_name = existing_table_name
                                break
                        
                        if matched_table_name:
                            for field in table_info.get("fields", []):
                                col_name = field.get("name")
                                value_list = field.get("ai_context", {}).get("value_list", [])
                                for col_info in tables_info[matched_table_name].get("columns", []):
                                    if col_info.get("name") == col_name:
                                        col_info["value_list"] = value_list
                                        break
                
                # Regenerate column_info.json with ai_type, property, value_list fields
                for k, v in tables_info.items():
                    for col_info in v.get("columns", []):
                        if col_info.get("nullable"):
                            del col_info["nullable"]
                        if col_info.get("sample_values"):
                            del col_info["sample_values"]
                        if col_info.get("type"):
                            column_type = col_info.get("type")
                            column_type = column_type.split(" ")[0].strip()
                            if "(" in column_type:
                                column_type = column_type.split("(")[0].strip()
                            col_info["type"] = column_type

                column_info_data = {
                    "success": True,
                    "source_type": source_type,
                    "db_url": db_url if db_url else "",
                    "db_name": db_name if db_name else "",
                    "table_count": len(normalized_table_names) if 'normalized_table_names' in locals() else 0,
                    "tables": tables_info,
                    "table_names": normalized_table_names if 'normalized_table_names' in locals() else []
                }
                
                column_info_path = os.path.join(output_dir, "column_info.json")
                with open(column_info_path, 'w', encoding='utf-8') as f:
                    json.dump(column_info_data, f, ensure_ascii=False, indent=2)
                
                if 'result' in locals() and isinstance(result, dict):
                    result["message"] = result.get("message", "") + ", knowledge file generated"
                else:
                    result = {
                        "success": True,
                        "message": "Excel file processed successfully, knowledge file generated"
                    }
                
                print(f"Database knowledge generation completed")
                print(f"Table structure information saved to: {os.path.abspath(column_info_path)}")
            else:
                raise Exception(f"API returned error: {response.status_code}")
            
        except Exception as e:
            if 'result' in locals():
                result["knowledge_error"] = str(e)
            print(f"Failed to generate knowledge file: {str(e)}")
        
        return result
    
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to read database table structure: {str(e)}"
        }


def enrich_from_database(db_url: str, knowledge_data: dict) -> dict:
    """
    Get sample data from database and execute SELECT DISTINCT queries
    Logic consistent with DatabaseKnowledgeGenerator.enrich_from_database
    
    Only executed when db_url is not None
    """
    if not db_url:
        return knowledge_data
    
    try:
        from sqlalchemy import create_engine, text
        
        engine = create_engine(db_url)
        # Update both tables and semantic_model parts
        table_info_dict = knowledge_data.get("tables", {})
        
        for table, table_info in table_info_dict.items():
            table_name = table
            table_name_short = table_name.split(".")[-1] if "." in table_name else table_name
            
            try:
                with engine.connect() as conn:
                    for field in table_info.get("fields", []):
                        # Only execute SELECT DISTINCT query for columns with ai_type enum
                        if field.get("ai_context", {}).get("ai_type") == "enum":
                            col_name = field.get("name")
                            distinct_query = f"SELECT DISTINCT `{col_name}` FROM {table_name_short} WHERE `{col_name}` IS NOT NULL"
                            distinct_result = conn.execute(text(distinct_query))
                            distinct_values = [row[0] for row in distinct_result.fetchall()]
                            str_values = [str(v) for v in distinct_values]
                            field["ai_context"]["value_list"] = str_values
                            field["ai_context"]["ai_type"] = "enum"
            except Exception:
                continue
        
        # Also update semantic_model part
        semantic_model = knowledge_data.get("semantic_model", [])
        for table_info in semantic_model:
            table_name = table_info.get("source", table_info.get("name"))
            table_name_short = table_name.split(".")[-1] if "." in table_name else table_name
            
            try:
                with engine.connect() as conn:
                    for field in table_info.get("fields", []):
                        # Only execute SELECT DISTINCT query for columns with ai_type enum
                        if field.get("ai_context", {}).get("ai_type") == "enum":
                            col_name = field.get("name")
                            distinct_query = f"SELECT DISTINCT `{col_name}` FROM {table_name_short} WHERE `{col_name}` IS NOT NULL"
                            distinct_result = conn.execute(text(distinct_query))
                            distinct_values = [row[0] for row in distinct_result.fetchall()]
                            str_values = [str(v) for v in distinct_values]
                            field["ai_context"]["value_list"] = str_values
                            field["ai_context"]["ai_type"] = "enum"
            except Exception:
                continue
        
        engine.dispose()
    except Exception as e:
        print(f"Failed to execute SELECT DISTINCT query: {str(e)}")
    
    return knowledge_data


def main():
    parser = argparse.ArgumentParser(description="Read database table structure and save as JSON files")
    parser.add_argument("--config-file", default="text-to-sql-config.json", 
                       help="Database configuration file path (default: text-to-sql-config.json)")
    parser.add_argument("--excel-file", default=None,
                       help="Excel file path, if provided, ignore db_url operation")
    parser.add_argument("--output-dir", default="./output",
                       help="Output directory path for generated files (default: ./output)")

    args = parser.parse_args()

    result = read_database_tables(args.config_file, True, args.excel_file, args.output_dir)
    
    # Output result (JSON format for programmatic use)
    # print(json.dumps(result, ensure_ascii=False, indent=2))
    
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
