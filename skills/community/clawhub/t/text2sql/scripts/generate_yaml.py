#!/usr/bin/env python3
"""
Text-to-SQL Topic Configuration File Generator Script
Function: Generate standard YAML configuration file based on topic name and selected tables
"""

import argparse
import sys
import os
import json
import yaml


def map_column_type(sql_type: str) -> str:
    """
    Map SQL types to standard types
    
    Args:
        sql_type: SQL data type string
        
    Returns:
        str: Standard type (text, number, date, boolean)
    """
    sql_type_lower = sql_type.lower()
    
    if any(t in sql_type_lower for t in ['int', 'integer', 'bigint', 'smallint', 'tinyint', 'decimal', 'numeric', 'float', 'double', 'real']):
        return 'number'
    elif any(t in sql_type_lower for t in ['date', 'time', 'datetime', 'timestamp']):
        return 'date'
    elif any(t in sql_type_lower for t in ['bool', 'boolean', 'bit']):
        return 'boolean'
    else:
        return 'text'


def generate_topic_yaml(
    topic_name: str,
    tables: list,
    tables_info: dict,
    output_path: str,
    knowledge_data: dict = None
) -> dict:
    """
    Generate standard topic configuration YAML file
    
    Args:
        topic_name: Topic name
        tables: List of selected table names, can be specific table names or ["all"] to select all tables
        tables_info: Structure information of all tables (output from read_tables.py)
        output_path: Output directory path
        knowledge_data: Database knowledge JSON data (containing property, ai_type, value_list)
    
    Returns:
        dict: Dictionary containing generation result information
    """
    try:
        # Process "all" special value
        if len(tables) == 1 and tables[0].lower() == "all":
            # Select all tables
            valid_tables = list(tables_info.keys())
            print(f"Auto-selected all tables, total: {len(valid_tables)} tables")
        else:
            # Validate table names
            valid_tables = []
            invalid_tables = []
            
            for table in tables:
                table = table.strip()
                if table in tables_info:
                    valid_tables.append(table)
                else:
                    invalid_tables.append(table)
            
            if invalid_tables:
                print(f"Warning: The following tables do not exist: {', '.join(invalid_tables)}")
        
        if not valid_tables:
            return {
                "success": False,
                "message": "No valid table names"
            }
        
        # Build standard configuration content
        config = {
            "version": "0.0.1",
            "semantic_model": 
                {
                    "name": topic_name,
                    "description": topic_name,
                    "ai_context": {
                        "instructions": f"Use this semantic model to handle data queries and analysis related to {topic_name}."
                    },
                    "datasets": []
                }
            
        }
        
        # Add dataset information
        for table_name in valid_tables:
            table_info = tables_info[table_name]
            table_comment = table_info.get("comment", "")

            # Build dataset
            dataset = {
                "name": table_name.split(".")[-1],
                "source": table_name,  # Use normalized table name format
                "description": table_comment if table_comment else table_name.split(".")[-1],
                "ai_context": {
                    "ai_name": table_comment if table_comment else table_name.split(".")[-1],
                },
                "fields": []
            }
            
            # Add field information
            for col in table_info["columns"]:
                column_comment = col.get("comment", "")
                ai_type = col.get("ai_type", "")
                property = col.get("property", "")
                value_list = col.get("value_list", [])
                is_default = col.get("is_default", False)
                
               
                field = {
                    "name": col["name"],
                    "type": map_column_type(col["type"]),
                    "description": column_comment if column_comment else col['name'].split(".")[-1],
                    "ai_context": {
                        "ai_name": column_comment if column_comment else col["name"].split(".")[-1],
                        "property": property,
                        "ai_type": ai_type,
                        "value_list": value_list,
                        "is_default": is_default,
                    }
                }
                
                if knowledge_data:
                    for know_table in knowledge_data.get("semantic_model", []):
                        for f in know_table.get("fields", []):
                            if f.get("name") == col["name"]:
                                ai_ctx = f.get("ai_context", {})
                                if ai_ctx.get("property"):
                                    field["ai_context"]["property"] = ai_ctx["property"]
                                if ai_ctx.get("ai_type"):
                                    field["ai_context"]["ai_type"] = ai_ctx["ai_type"]
                                if ai_ctx.get("value_list"):
                                    field["ai_context"]["value_list"] = ai_ctx["value_list"]
                                if ai_ctx.get("is_default"):
                                    field["ai_context"]["is_default"] = ai_ctx["is_default"]
                                
                                break
                
                dataset["fields"].append(field)
            
            config["semantic_model"]["datasets"].append(dataset)
        
        # Ensure output directory exists
        os.makedirs(output_path, exist_ok=True)
        
        # Generate YAML file path
        yaml_filename = f"{topic_name}.yaml"
        yaml_filepath = os.path.join(output_path, yaml_filename)
        
        # Write YAML file
        with open(yaml_filepath, 'w', encoding='utf-8') as f:
            # Write header comment
            f.write("# yaml-language-server: $schema=../core-spec/osi-schema.json\n")
            f.write(f"\n# {topic_name} Semantic Model\n\n")
            
            # Write YAML content
            yaml.dump(config, f, allow_unicode=True, default_flow_style=False, sort_keys=False, width=1000)
        
        print(f"Topic configuration file generated: {yaml_filepath}")
        
        return {
            "success": True,
            "yaml_path": os.path.abspath(yaml_filepath),
            "topic": topic_name,
            "table_count": len(valid_tables),
            "tables": valid_tables,
            "message": f"Topic configuration file generated successfully, containing {len(valid_tables)} tables"
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to generate topic configuration file: {str(e)}"
        }


def main():
    parser = argparse.ArgumentParser(description="Generate topic configuration YAML file")
    parser.add_argument("--topic-name", required=True, help="Topic name")
    parser.add_argument("--tables", required=True, help="List of selected table names, comma-separated, or use 'all' to select all tables")
    parser.add_argument("--tables-info-file", default="./output/column_info.json", help="Table structure information JSON file path (generated by read_tables.py, default: ./output/column_info.json)")
    parser.add_argument("--output-path", default="./output/", help="Output directory path (default: ./output/)")
    parser.add_argument("--knowledge-file", help="Database knowledge JSON file path (containing property, ai_type, value_list)")
    
    args = parser.parse_args()
    
    knowledge_data = None
    if args.knowledge_file and os.path.exists(args.knowledge_file):
        try:
            with open(args.knowledge_file, 'r', encoding='utf-8') as f:
                knowledge_data = json.load(f)
        except Exception as e:
            print(f"Warning: Failed to read knowledge file: {e}")
    
    # Check if table structure information file exists
    if not os.path.exists(args.tables_info_file):
        print(f"Error: Table structure information file {args.tables_info_file} does not exist")
        sys.exit(1)
    
    # Read table structure information from file
    try:
        with open(args.tables_info_file, 'r', encoding='utf-8') as f:
            tables_data = json.load(f)
        
        tables_info = tables_data.get("tables", {})
        
        if not tables_info:
            print("Error: No table data in table structure information file")
            sys.exit(1)
            
    except json.JSONDecodeError as e:
        print(f"Error: JSON format error in table structure information file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Failed to read table structure information file: {e}")
        sys.exit(1)
    
    # Parse table name list
    tables_list = [t.strip() for t in args.tables.split(",")]
    
    # Execute generation
    result = generate_topic_yaml(
        args.topic_name,
        tables_list,
        tables_info,
        args.output_path,
        knowledge_data
    )
    
    # Output result (JSON format for programmatic use)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
