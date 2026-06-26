import os
import json
import sys
import urllib.request
import urllib.error

# 区域配置表：管理域名映射与 Token 获取链接
REGION_CONFIG = {
    'cn': {
        'base': 'https://api.wucai.site',
        'token_url': 'https://marker.dotalk.cn/#/personSetting/openapi'
    },
    'eu': {
        'base': 'https://eu.wucainote.com',
        'token_url': 'https://eu.wucainote.com/#/personSetting/openapi'
    },
    'us': {
        'base': 'https://us.wucainote.com',
        'token_url': 'https://us.wucainote.com/#/personSetting/openapi'
    }
}

def call_wucai(endpoint, params=None):
    """
    执行五彩 API 请求的核心函数 (原生 urllib 实现)
    """
    # 1. 获取并校验环境变量
    token = os.getenv('WUCAI_API_TOKEN', '').strip()
    region = os.getenv('WUCAI_REGION', 'cn').lower()
    
    config = REGION_CONFIG.get(region, REGION_CONFIG['cn'])
    
    # Token 缺失拦截
    if not token or not token.startswith('wct-'):
        return {
            "code": 10010, 
            "message": f"Missing or invalid WUCAI_API_TOKEN. Please get your OpenClaw Token from: {config['token_url']}"
        }

    # 2. 构造请求地址
    clean_endpoint = endpoint.lstrip('/')
    full_url = f"{config['base']}/apix/openapi/aiagent/{clean_endpoint}"
    
    # 3. 构造 Headers
    headers = {
        "Authorization": token,
        "X-Client-ID": "56",
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "WuCai-OpenClaw-Agent/1.1"
    }

    try:
        # 4. 序列化数据并构建 Request
        data = json.dumps(params or {}).encode('utf-8')
        req = urllib.request.Request(full_url, data=data, headers=headers, method='POST')
        
        # 5. 执行请求，强制 15s 超时
        with urllib.request.urlopen(req, timeout=15) as response:
            res_body = response.read().decode('utf-8')
            try:
                return json.loads(res_body)
            except ValueError:
                return {"code": -1, "message": "Server error (Non-JSON response)."}

    except urllib.error.HTTPError as e:
        # 捕获 4xx/5xx 错误并尝试读取返回内容
        try:
            error_body = e.read().decode('utf-8')
            return json.loads(error_body)
        except:
            return {"code": e.code, "message": f"HTTP Error {e.code}: {e.reason}"}
            
    except urllib.error.URLError as e:
        return {"code": -1, "message": f"Network Error: {str(e.reason)}"}
    except Exception as e:
        return {"code": -1, "message": f"Unexpected Error: {str(e)}"}

if __name__ == "__main__":
    """
    CLI 入口：支持从 Stdin 或 命令行参数读取 JSON
    """
    if len(sys.argv) < 2:
        print(json.dumps({"code": -1, "message": "Usage: echo '<json>' | python wucai_api.py <endpoint>"}, ensure_ascii=False))
        sys.exit(1)
        
    endpoint_arg = sys.argv[1]
    params_data = {}

    # 优先从管道 (Stdin) 读取数据
    try:
        if not sys.stdin.isatty():
            raw_input = sys.stdin.read().strip()
            if raw_input:
                params_data = json.loads(raw_input)
        elif len(sys.argv) > 2:
            params_data = json.loads(sys.argv[2])
    except json.JSONDecodeError:
        print(json.dumps({"code": -1, "message": "Invalid JSON input."}, ensure_ascii=False))
        sys.exit(1)
            
    # 执行并输出结果给 AI (stdout)
    print(json.dumps(call_wucai(endpoint_arg, params_data), ensure_ascii=False))