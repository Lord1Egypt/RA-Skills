import random
import requests
import sys

# API映射表
API_MAP = {
    "xiaohua": "https://api.pearktrue.cn/api/jdyl/xiaohua.php",
    "duanzi": "https://api.pearktrue.cn/api/random/duanzi/",
    "dujitang": "https://api.pearktrue.cn/api/dujitang"
}

def get_content(api_url):
    response = requests.get(api_url, timeout=3)
    response.raise_for_status()
    return response.text.strip().strip('"')

if __name__ == "__main__":
    # 解析参数
    if len(sys.argv) > 1:
        req_type = sys.argv[1].lower()
        if req_type in API_MAP:
            api_url = API_MAP[req_type]
        else:
            # 无效参数时随机选一个
            api_url = random.choice(list(API_MAP.values()))
    else:
        # 无参数时随机选一个API
        api_url = random.choice(list(API_MAP.values()))
    
    content = get_content(api_url)
    print(content)
