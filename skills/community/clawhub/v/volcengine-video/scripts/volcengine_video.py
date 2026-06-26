import json
import sys
import os
import base64
import datetime
import hashlib
import hmac
import requests


def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()


def getSignatureKey(key, dateStamp, regionName, serviceName):
    kDate = sign(key.encode('utf-8'), dateStamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'request')
    return kSigning


def formatQuery(parameters):
    request_parameters_init = ''
    for key in sorted(parameters):
        request_parameters_init += key + '=' + parameters[key] + '&'
    request_parameters = request_parameters_init[:-1]
    return request_parameters


def signV4Request(access_key, secret_key, service, req_query, req_body):
    if access_key is None or secret_key is None:
        print('No access key is available.')
        sys.exit()

    t = datetime.datetime.utcnow()
    current_date = t.strftime('%Y%m%dT%H%M%SZ')
    datestamp = t.strftime('%Y%m%d')  # Date w/o time, used in credential scope
    canonical_uri = '/'
    canonical_querystring = req_query
    signed_headers = 'content-type;host;x-content-sha256;x-date'
    payload_hash = hashlib.sha256(req_body.encode('utf-8')).hexdigest()
    content_type = 'application/json'
    canonical_headers = 'content-type:' + content_type + '\n' + 'host:' + 'visual.volcengineapi.com' + \
                        '\n' + 'x-content-sha256:' + payload_hash + \
                        '\n' + 'x-date:' + current_date + '\n'
    canonical_request = 'POST' + '\n' + canonical_uri + '\n' + canonical_querystring + \
                        '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash
    
    algorithm = 'HMAC-SHA256'
    credential_scope = datestamp + '/' + 'cn-north-1' + '/' + service + '/' + 'request'
    string_to_sign = algorithm + '\n' + current_date + '\n' + credential_scope + '\n' + hashlib.sha256(
        canonical_request.encode('utf-8')).hexdigest()
    
    signing_key = getSignatureKey(secret_key, datestamp, 'cn-north-1', service)
    signature = hmac.new(signing_key, (string_to_sign).encode(
        'utf-8'), hashlib.sha256).hexdigest()

    authorization_header = algorithm + ' ' + 'Credential=' + access_key + '/' + \
                           credential_scope + ', ' + 'SignedHeaders=' + \
                           signed_headers + ', ' + 'Signature=' + signature
    
    headers = {'X-Date': current_date,
               'Authorization': authorization_header,
               'X-Content-Sha256': payload_hash,
               'Content-Type': content_type}
    
    # ************* SEND THE REQUEST *************
    endpoint = 'https://visual.volcengineapi.com'
    request_url = endpoint + '?' + canonical_querystring

    print('\nBEGIN REQUEST++++++++++++++++++++++++++++++++++++')
    print('Request URL = ' + request_url)
    try:
        r = requests.post(request_url, headers=headers, data=req_body)
    except Exception as err:
        print(f'error occurred: {err}')
        raise
    else:
        print('\nRESPONSE++++++++++++++++++++++++++++++++++++')
        print(f'Response code: {r.status_code}\n')
        # 使用 replace 方法将 \u0026 替换为 &
        resp_str = r.text.replace("\\u0026", "&")
        print(f'Response body: {resp_str}\n')
        return r.json()


def generate_video(prompt, frames=241, req_key="jimeng_ti2v_v30_pro", access_key=None, secret_key=None):
    """
    Generate video using VolcEngine's AI video generation API
    
    Args:
        prompt (str): Text prompt for video generation
        frames (int): Number of frames (default: 241)
        req_key (str): Request key for the specific model
        access_key (str): VolcEngine access key
        secret_key (str): VolcEngine secret key
    
    Returns:
        dict: API response
    """
    # 如果没有提供密钥，尝试从环境变量获取
    if access_key is None:
        access_key = os.getenv('VOLCENGINE_ACCESS_KEY')
    if secret_key is None:
        secret_key = os.getenv('VOLCENGINE_SECRET_KEY')
    
    # 请求Query
    query_params = {
        'Action': 'CVSync2AsyncSubmitTask',
        'Version': '2022-08-31',
    }
    formatted_query = formatQuery(query_params)

    # 请求Body
    body_params = {
        "req_key": req_key,
        "prompt": prompt,
        "frames": frames,
    }
    formatted_body = json.dumps(body_params)

    return signV4Request(access_key, secret_key, 'cv', formatted_query, formatted_body)


def load_config():
    """Load configuration from config.json file"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Config file not found: {config_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Invalid JSON in config file: {config_path}")
        return {}


if __name__ == "__main__":
    # 从命令行参数获取提示词
    if len(sys.argv) < 2:
        print("Usage: python volcengine_video.py <prompt> [frames]")
        sys.exit(1)
    
    prompt = sys.argv[1]
    frames = int(sys.argv[2]) if len(sys.argv) > 2 else 241
    
    # 从配置文件加载密钥
    config = load_config()
    access_key = config.get('access_key')
    secret_key = config.get('secret_key')
    
    if not access_key or not secret_key:
        print("Error: Missing access_key or secret_key in config.json")
        sys.exit(1)
    
    result = generate_video(prompt, frames, access_key=access_key, secret_key=secret_key)
    print(json.dumps(result, indent=2))