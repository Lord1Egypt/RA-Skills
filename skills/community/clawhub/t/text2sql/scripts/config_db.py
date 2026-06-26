#!/usr/bin/env python3
"""
Text-to-SQL Database Configuration Script
Function: Save database configuration to local configuration file
"""

import argparse
import sys
import json
import os


def config_database(db_url: str, db_password: str, config_file: str = "./output/text-to-sql-config.json") -> dict:
    """
    Save database configuration to local file
    
    Args:
        db_url: Database connection URL
        db_password: Database password
        config_file: Configuration file path
        
    Returns:
        dict: Dictionary containing configuration result information
    """
    try:
        # Ensure output directory exists
        output_dir = os.path.dirname(config_file)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        # Build configuration data
        config = {
            "db_url": db_url,
            "db_password": db_password,
            "configured_at": None  # Timestamp can be added
        }
        
        # Save to configuration file
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        print(f"Database configuration saved to: {os.path.abspath(config_file)}")
        
        return {
            "success": True,
            "message": "Database configuration saved successfully",
            "config_file": os.path.abspath(config_file)
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to save configuration: {str(e)}"
        }


def main():
    parser = argparse.ArgumentParser(description="Configure Text-to-SQL database connection")
    parser.add_argument("--db-url", required=True, help="Database connection URL")
    parser.add_argument("--db-password", required=True, help="Database password")
    parser.add_argument("--config-file", default="./output/text-to-sql-config.json", 
                       help="Configuration file path (default: ./output/text-to-sql-config.json)")
    
    args = parser.parse_args()
    
    # Execute configuration
    result = config_database(args.db_url, args.db_password, args.config_file)
    
    # Output result (JSON format for programmatic use)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
