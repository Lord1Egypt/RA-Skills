import json
import urllib.request
from urllib.error import URLError, HTTPError
import sys
from pathlib import Path
from urllib.parse import urlencode

ENV_FILE = Path(__file__).parent / ".env"

def load_env():
    if not ENV_FILE.exists():
        return {}
    env = {}
    with open(ENV_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                env[key.strip()] = val.strip()
    return env

def save_env(url, token):
    with open(ENV_FILE, "w", encoding="utf-8") as f:
        f.write(f"TRAILSNAP_API_URL={url}\n")
        f.write(f"TRAILSNAP_API_TOKEN={token}\n")
    print(f"配置已保存到 {ENV_FILE}")

def make_request(endpoint, params=None, method="GET", response_type="json"):
    env = load_env()
    base_url = env.get("TRAILSNAP_API_URL")
    token = env.get("TRAILSNAP_API_TOKEN")
    
    if not base_url or not token:
        print("错误: API URL 和 Token 未配置，请先运行 'config' 命令。")
        sys.exit(1)
        
    url = f"{base_url.rstrip('/')}{endpoint}"
    if params:
        # 过滤掉 None 值
        params = {k: v for k, v in params.items() if v is not None}
        if params:
            query_string = urlencode(params, doseq=True)
            url = f"{url}?{query_string}"
            
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            if response_type == "json":
                return json.loads(response.read().decode("utf-8"))
            elif response_type == "text":
                return response.read().decode("utf-8")
            if response_type == "bytes":
                return response.read()
            else:
                print(f"未知的响应类型: {response_type}")
                sys.exit(1)
                return response.read().decode("utf-8")
    except HTTPError as e:
        print(f"HTTP 错误: {e.code} - {e.read().decode('utf-8')}")
        sys.exit(1)
    except URLError as e:
        print(f"URL 错误: {e.reason}")
        sys.exit(1)
    except Exception as e:
        print(f"错误: {str(e)}")
        sys.exit(1)

load_env()