#!/usr/bin/env python3
"""
Text-to-SQL SQL Generation Script
Function: Call generate_sql API via API to convert natural language to SQL
"""

import argparse
import sys
import os
import json
import urllib.request
import urllib.error


def generate_sql(api_url: str, question: str, config_file: str, timeout: int = 90) -> dict:
    """
    Generate SQL by calling generate_sql API
    
    Args:
        api_url: API base URL
        question: User's natural language question
        config_file: Topic configuration YAML file path
        timeout: Request timeout (seconds)
        
    Returns:
        dict: Dictionary containing generated SQL and metadata
    """
    try:
        # Check if configuration file exists
        if not os.path.exists(config_file):
            return {
                "success": False,
                "message": f"Configuration file {config_file} does not exist"
            }
        
        # Build complete API URL
        generate_url = f"{api_url.rstrip('/')}/ask/api/sql_for_skill"
        
        # Debug: Print complete URL
        print(f"Request URL: {generate_url}")
        
        # Prepare form_data
        # Read YAML file content
        with open(config_file, 'rb') as f:
            yaml_file_content = f.read()
        
        # Build form-data
        form_data = {
            'question': question,
            'yaml_file': yaml_file_content
        }
        
        # Encode form-data
        boundary = b'----WebKitFormBoundary7MA4YWxkTrZu0gW'
        lines = []
        
        for key, value in form_data.items():
            lines.append(b'--' + boundary)
            lines.append(b'Content-Disposition: form-data; name="%s"' % key.encode('utf-8'))
            
            if isinstance(value, bytes):
                # File content
                filename = os.path.basename(config_file)
                lines[-1] += b'; filename="%s"' % filename.encode('utf-8')
                lines.append(b'Content-Type: application/octet-stream')
            else:
                # Regular field
                lines.append(b'Content-Type: text/plain; charset=utf-8')
            
            lines.append(b'')
            
            if isinstance(value, bytes):
                lines.append(value)
            else:
                lines.append(value.encode('utf-8'))
        
        lines.append(b'--' + boundary + b'--')
        lines.append(b'')
        
        body = b'\r\n'.join(lines)
        
        # Create request object
        req = urllib.request.Request(
            generate_url,
            data=body,
            headers={
                'Content-Type': f'multipart/form-data; boundary={boundary.decode("utf-8")}',
                'Accept': 'application/json'
            },
            method='POST'
        )
        
        print(f"Generating SQL: {os.path.basename(config_file)}")
        
        # Send request
        with urllib.request.urlopen(req, timeout=timeout) as response:
            response_data = response.read()
            response_text = response_data.decode('utf-8')
            
            # Debug: Print raw response
            print(f"Response status code: {response.status}")
            print(f"Response content: {response_text[:500]}")  # Print first 500 characters
            
            # Try to parse JSON
            try:
                result_list = json.loads(response_text)
            except json.JSONDecodeError as e:
                return {
                    "success": False,
                    "message": f"Failed to parse response: {str(e)}. Response content: {response_text[:500]}"
                }
            
            # Check return result
            if isinstance(result_list, list) and len(result_list) > 0:
                result = result_list[0]
                
                if result.get("STATUS") == "ok":
                    sql_query = result.get("SQL", "")
                    question_from_api = result.get("QUESTION", "")
                    
                    print(f"SQL generated successfully")
                    
                    return {
                        "success": True,
                        "sql": sql_query,
                        "question": question_from_api,
                        "message": "SQL generated successfully"
                    }
                else:
                    message = result.get("MESSAGE", "SQL generation failed")
                    print(f"SQL generation failed: {message}")
                    return {
                        "success": False,
                        "message": message
                    }
            else:
                print(f"SQL generation failed: Invalid return data format")
                return {
                    "success": False,
                    "message": "Invalid return data format"
                }
                
    except urllib.error.HTTPError as e:
        error_msg = f"HTTP error: {e.code} - {e.reason}"
        try:
            error_data = json.loads(e.read().decode('utf-8'))
            if isinstance(error_data, list) and len(error_data) > 0:
                error_msg = error_data[0].get("MESSAGE", str(e.reason))
        except:
            pass
        return {
            "success": False,
            "message": error_msg
        }
    except urllib.error.URLError as e:
        return {
            "success": False,
            "message": f"Unable to connect to API service: {e.reason}"
        }
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "message": f"Failed to parse response: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to generate SQL: {str(e)}"
        }


def main():
    parser = argparse.ArgumentParser(description="Convert natural language to SQL")
    parser.add_argument("--api-url", default="https://asksql.ucap.com.cn/", 
                       help="API service URL (default: https://asksql.ucap.com.cn/)")
    parser.add_argument("--question", required=True, help="User's natural language question")
    parser.add_argument("--config", required=True, help="Topic configuration YAML file path")
    
    args = parser.parse_args()
    
    # Execute SQL generation
    result = generate_sql(args.api_url, args.question, args.config)
    
    # Output result (JSON format for programmatic use)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
