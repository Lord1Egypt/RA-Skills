import urllib.request
import json

url = 'http://localhost:18060/mcp'
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/event-stream'
}

# Initialize
payload = {
    'jsonrpc': '2.0',
    'method': 'initialize',
    'params': {},
    'id': 1
}
req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode(),
    headers=headers,
    method='POST'
)
with urllib.request.urlopen(req, timeout=10) as resp:
    session_id = resp.headers.get('Mcp-Session-Id')

headers['Mcp-Session-Id'] = session_id

# Publish
title = "宅家氛围感 | 午后窗边的慵懒少年"
content = """最近沉迷这种居家感✨

阳光透过窗户洒进来
配上柔软的毛绒睡袍
一副黑框眼镜
不需要刻意摆pose
松弛感拉满

这样的午后
是属于一个人的安静时光
☕️🪟

#氛围感 #少年感 #居家拍照 #男生穿搭 #斯文败类
#拍照姿势不求人 #宅家摄影 #小红书男神
#氛围感帅哥 #松弛感 #盐系男生"""

payload = {
    'jsonrpc': '2.0',
    'method': 'tools/call',
    'params': {
        'name': 'publish_content',
        'arguments': {
            'title': title,
            'content': content,
            'images': ['/app/images/post1.png'],
            'tags': ['氛围感', '少年感', '居家拍照', '男生穿搭', '斯文败类', '拍照姿势不求人', '宅家摄影', '小红书男神', '氛围感帅哥', '松弛感', '盐系男生']
        }
    },
    'id': 2
}
req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode(),
    headers=headers,
    method='POST'
)
with urllib.request.urlopen(req, timeout=120) as resp:
    result = json.loads(resp.read().decode())

with open(r'C:\Users\15822\.agents\skills\xhsmander\scripts\publish_result.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print('Done')
