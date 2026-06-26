import http.client
import json
import argparse
import os
import sys

def get_config():
    """
    加载配置文件
    """
    config_path = os.path.join(os.path.dirname(__file__), "../assets/config.json")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Failed to load config from {config_path}: {e}")
        return {}

def main():
    parser = argparse.ArgumentParser(description='Modify a proposal task.')
    parser.add_argument('--prompt', type=str, required=True, help='The modification instruction')
    parser.add_argument('--taskid', type=str, required=True, help='The ID of the task to modify')
    parser.add_argument('--seko_api_key', type=str, help='The Seko API key (optional)')

    args = parser.parse_args()

    # Determine API key
    api_key = args.seko_api_key
    if not api_key:
        api_key = os.environ.get('SEKO_API_KEY')
    
    if not api_key:
        print("Error: Seko-API-Key not found. Please provide it via --seko_api_key or as an environment variable.", file=sys.stderr)
        sys.exit(1)

    # Load config
    config = get_config()
    api_base_url = config.get("api_base_url")
    if not api_base_url:
        print("Error: api_base_url not found in assets/config.json", file=sys.stderr)
        sys.exit(1)

    # Prepare HTTP POST Request
    conn = http.client.HTTPSConnection(api_base_url)
    payload = json.dumps({
        "input": args.prompt,
        "updateCtx": {
            "taskId": args.taskid
        }
    })
    headers = {
        'Seko-API-Key': api_key,
        'Content-Type': 'application/json',
        'Accept': '*/*',
    }

    try:
        conn.request("POST", "/seko-api/openapi/v1/plan-tasks", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
    except Exception as e:
        print(f"Error making request: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
