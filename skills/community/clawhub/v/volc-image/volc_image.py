import os
import sys
import time
import json
import requests

# 检查ARK_API_KEY
api_key = os.environ.get('ARK_API_KEY')
if not api_key:
    # 尝试从参数获取
    for arg in sys.argv[1:]:
        if arg.startswith('ARK_API_KEY='):
            api_key = arg.split('=', 1)[1]
            os.environ['ARK_API_KEY'] = api_key
            break

if not api_key:
    print("Error: ARK_API_KEY not found. Please set ARK_API_KEY environment variable.")
    sys.exit(1)

# 从参数获取提示词
prompt = None
for arg in sys.argv[1:]:
    if not arg.startswith('ARK_API_KEY=') and not arg.startswith('--'):
        prompt = arg
        break

if not prompt:
    print("Error: Please provide a prompt for image generation.")
    print("Usage: python script.py <prompt>")
    sys.exit(1)

print(f"Generating image with prompt: {prompt}")

# 调用火山引擎API
url = 'https://ark.cn-beijing.volces.com/api/v3/images/generations'
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}
data = {
    'model': 'doubao-seedream-5-0-260128',
    'prompt': prompt,
    'sequential_image_generation': 'disabled',
    'response_format': 'url',
    'size': '2K',
    'stream': False,
    'watermark': True
}

try:
    response = requests.post(url, headers=headers, json=data, timeout=120)
    result = response.json()
    
    if 'data' in result and len(result['data']) > 0:
        img_url = result['data'][0]['url']
        print(f"Image generated successfully!")
        print(f"URL: {img_url}")
        
        # 下载图片
        img_response = requests.get(img_url)
        if img_response.status_code == 200:
            # 保存到当前目录
            timestamp = int(time.time())
            filename = f'volc_image_{timestamp}.jpg'
            with open(filename, 'wb') as f:
                f.write(img_response.content)
            print(f"Image saved to: {filename}")
            print(f"MEDIA:{os.path.abspath(filename)}")
        else:
            print(f"Failed to download image: {img_response.status_code}")
    else:
        print(f"Error: {json.dumps(result, indent=2)}")
        
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
