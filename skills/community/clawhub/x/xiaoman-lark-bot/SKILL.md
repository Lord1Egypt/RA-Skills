---
name: lark-bot
description: "飞书/Lark Bot 完整对接方案 - 所有敏感配置从环境变量读取，支持消息收发、知识库操作、Bitable 任务管理"
metadata: { 
  "openclaw": { 
    "emoji": "🦉", 
    "requires": { 
      "bins": ["python3"], 
      "env": ["LARK_APP_ID", "LARK_APP_SECRET"] 
    } 
  } 
}
---

# Lark Bot 完整对接方案

本 skill 提供飞书 Bot 完整对接方案，包含消息收发、知识库操作、Bitable 任务管理。所有配置均从环境变量读取，确保安全。

## 环境变量配置

在使用本 skill 前，需配置以下环境变量：

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `LARK_APP_ID` | 飞书应用 ID | cli_xxxxxxxx |
| `LARK_APP_SECRET` | 飞书应用密钥 | xxxxxxxxxxxxxx |
| `LARK_APP_TOKEN` | Bitable App Token（可选） | ${LARK_APP_TOKEN} |
| `LARK_TABLE_ID` | Bitable Table ID（可选） | ${LARK_TABLE_ID} |
| `LARK_SPACE_ID` | Wiki 知识库 ID（可选） | 76036636xxxxx |
| `LARK_CHAT_ID` | 群聊 ID（可选） | ${LARK_CHAT_ID} |

## 核心功能

### 1. 获取 Access Token

```python
import os
import json
import urllib.request

APP_ID = os.environ.get("LARK_APP_ID", "")
APP_SECRET = os.environ.get("LARK_APP_SECRET", "")

def get_tenant_access_token():
    url = "https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal"
    data = json.dumps({
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    }).encode()
    
    req = urllib.request.Request(
        url, 
        data=data, 
        headers={'Content-Type': 'application/json'}
    )
    
    with urllib.request.urlopen(req, timeout=10) as resp:
        result = json.loads(resp.read())
        return result.get("tenant_access_token")

token = get_tenant_access_token()
print(f"Token: {token}")
```

### 2. 发送消息到群聊

```python
import os
import json
import urllib.request

APP_ID = os.environ.get("LARK_APP_ID", "")
APP_SECRET = os.environ.get("LARK_APP_SECRET", "")
CHAT_ID = os.environ.get("LARK_CHAT_ID", "")

def get_token():
    url = "https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal"
    data = json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode()
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    return json.loads(urllib.request.urlopen(req).read())['tenant_access_token']

def send_message(text):
    token = get_token()
    url = "https://open.larksuite.com/open-apis/im/v1/messages"
    params = f"?receive_id_type=chat_id"
    data = {
        "receive_id": CHAT_ID,
        "msg_type": "text",
        "content": json.dumps({"text": text})
    }
    
    req = urllib.request.Request(
        url + params,
        data=json.dumps(data).encode(),
        method="POST",
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
    )
    return json.loads(urllib.request.urlopen(req).read())

# 发送消息
result = send_message("Hello from Lark Bot!")
print(result)
```

### 3. 发送富文本卡片消息

```python
import os
import json
import urllib.request

APP_ID = os.environ.get("LARK_APP_ID", "")
APP_SECRET = os.environ.get("LARK_APP_SECRET", "")
CHAT_ID = os.environ.get("LARK_CHAT_ID", "")

def get_token():
    url = "https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal"
    data = json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode()
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    return json.loads(urllib.request.urlopen(req).read())['tenant_access_token']

def send_interactive_card(text, button_text, button_url):
    token = get_token()
    url = "https://open.larksuite.com/open-apis/im/v1/messages"
    params = "?receive_id_type=chat_id"
    
    card = {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": "📢 通知"},
            "template": "blue"
        },
        "elements": [
            {
                "tag": "div",
                "text": {"tag": "plain_text", "content": text}
            },
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {"tag": "plain_text", "content": button_text},
                        "type": "primary",
                        "url": button_url
                    }
                ]
            }
        ]
    }
    
    data = {
        "receive_id": CHAT_ID,
        "msg_type": "interactive",
        "content": json.dumps(card)
    }
    
    req = urllib.request.Request(
        url + params,
        data=json.dumps(data).encode(),
        method="POST",
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
    )
    return json.loads(urllib.request.urlopen(req).read())

result = send_interactive_card("报告已生成", "查看详情", "https://example.com")
print(result)
```

### 4. 操作 Bitable（任务管理）

```python
import os
import json
import urllib.request
import time

APP_ID = os.environ.get("LARK_APP_ID", "")
APP_SECRET = os.environ.get("LARK_APP_SECRET", "")
APP_TOKEN = os.environ.get("LARK_APP_TOKEN", "")
TABLE_ID = os.environ.get("LARK_TABLE_ID", "")

_cache = {'token': None, 'exp': 0}

def get_token():
    if _cache['token'] and time.time() < _cache['exp']:
        return _cache['token']
    
    url = "https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal"
    data = json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode()
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    with urllib.request.urlopen(req, timeout=10) as resp:
        result = json.loads(resp.read())
        _cache['token'] = result['tenant_access_token']
        _cache['exp'] = time.time() + result.get('expire', 7200) - 300
        return _cache['token']

def api(method, path, body=None):
    base_url = f"https://open.larksuite.com/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}"
    url = base_url + path
    data = json.dumps(body).encode() if body else None
    
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            'Authorization': f'Bearer {get_token()}',
            'Content-Type': 'application/json'
        }
    )
    return json.loads(urllib.request.urlopen(req, timeout=15).read())

# 列出所有记录
def list_records():
    return api("GET", "/records?page_size=100")

# 创建记录
def create_record(name, status="待办", priority="中"):
    fields = {
        "任务名称": name,
        "状态": status,
        "优先级": priority
    }
    return api("POST", "/records", {"fields": fields})

# 更新记录
def update_record(record_id, fields):
    return api("PUT", f"/records/{record_id}", {"fields": fields})

# 删除记录
def delete_record(record_id):
    return api("DELETE", f"/records/{record_id}")

# 使用示例
records = list_records()
print(f"当前有 {len(records.get('data', {}).get('items', []))} 条任务")
```

### 5. 操作 Wiki 知识库

```python
import os
import json
import urllib.request
import time

APP_ID = os.environ.get("LARK_APP_ID", "")
APP_SECRET = os.environ.get("LARK_APP_SECRET", "")
SPACE_ID = os.environ.get("LARK_SPACE_ID", "")

_cache = {'token': None, 'exp': 0}

def get_token():
    if _cache['token'] and time.time() < _cache['exp']:
        return _cache['token']
    
    url = "https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal"
    data = json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode()
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    with urllib.request.urlopen(req, timeout=10) as resp:
        result = json.loads(resp.read())
        _cache['token'] = result['tenant_access_token']
        _cache['exp'] = time.time() + result.get('expire', 7200) - 300
        return _cache['token']

# 获取知识库列表
def list_spaces():
    url = "https://open.larksuite.com/open-apis/wiki/v2/spaces"
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {get_token()}'})
    return json.loads(urllib.request.urlopen(req).read())

# 获取节点列表
def list_nodes(space_id):
    url = f"https://open.larksuite.com/open-apis/wiki/v2/spaces/{space_id}/nodes"
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {get_token()}'})
    return json.loads(urllib.request.urlopen(req).read())

# 创建文档
def create_doc(space_id, parent_node_id, title, content):
    url = "https://open.larksuite.com/open-apis/docx/v1/documents"
    data = {
        "document_request": {
            "node_type": "docx",
            "parent_node_id": parent_node_id,
            "space_id": space_id,
            "title": title
        }
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode(),
        method="POST",
        headers={
            'Authorization': f'Bearer {get_token()}',
            'Content-Type': 'application/json'
        }
    )
    result = json.loads(urllib.request.urlopen(req).read())
    
    # 写入内容
    doc_token = result['data']['document']['token']
    return write_doc_content(doc_token, content)

# 写入文档内容
def write_doc_content(doc_token, content):
    url = f"https://open.larksuite.com/open-apis/docx/v1/documents/{doc_token}/blocks"
    
    # 构建文本块
    blocks = []
    for line in content.split('\n'):
        if line.strip():
            blocks.append({
                "block_type": "paragraph",
                "paragraph": {
                    "elements": [
                        {
                            "text_element": {
                                "content": line,
                                "type": "text"
                            }
                        }
                    ]
                }
            })
    
    data = {"blocks": blocks}
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode(),
        method="POST",
        headers={
            'Authorization': f'Bearer {get_token()}',
            'Content-Type': 'application/json'
        }
    )
    return json.loads(urllib.request.urlopen(req).read())

# 使用示例
spaces = list_spaces()
print(f"知识库列表: {spaces}")
```

## 消息接收（Webhook）

如需接收群消息，需配置 Webhook 回调：

1. 在飞书开放平台配置事件回调 URL
2. 使用内网穿透工具（如 cloudflared）暴露本地服务
3. 处理飞书推送的事件消息

示例 Webhook 服务：

```python
#!/usr/bin/env python3
"""
Lark Webhook 消息接收服务
"""
import os
import json
import hmac
import hashlib
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

APP_SECRET = os.environ.get("LARK_APP_SECRET", "")
PORT = int(os.environ.get("LARK_WEBHOOK_PORT", "19800"))

def verify_signature(timestamp, nonce, signature):
    """验证飞书签名"""
    string = f"{timestamp}{nonce}{APP_SECRET}"
    h = hashlib.sha1(string.encode()).hexdigest()
    return h == signature

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode()
        
        # 解析请求体
        data = json.loads(body)
        
        # 处理消息事件
        if data.get("type") == "url_verification":
            # 验证 URL
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "challenge": data.get("challenge")
            }).encode())
            return
        
        if data.get("type") == "event_callback":
            event = data.get("event", {})
            msg_type = event.get("msg_type")
            
            if msg_type == "text":
                text = event.get("message", {}).get("text", "")
                print(f"收到消息: {text}")
                
                # TODO: 处理消息逻辑
        
        self.send_response(200)
        self.end_headers()
    
    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {format % args}")

if __name__ == '__main__':
    server = HTTPServer(('', PORT), Handler)
    print(f"Lark Webhook 服务启动于端口 {PORT}")
    server.serve_forever()
```

## 完整工作流示例

### 场景：定时发送报告到群聊

```python
import os
import json
import urllib.request
import time

# 配置
APP_ID = os.environ.get("LARK_APP_ID", "")
APP_SECRET = os.environ.get("LARK_APP_SECRET", "")
CHAT_ID = os.environ.get("LARK_CHAT_ID", "")
APP_TOKEN = os.environ.get("LARK_APP_TOKEN", "")
TABLE_ID = os.environ.get("LARK_TABLE_ID", "")

# 获取 token
def get_token():
    url = "https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal"
    data = json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode()
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    return json.loads(urllib.request.urlopen(req).read())['tenant_access_token']

# 发送消息
def send_message(text):
    token = get_token()
    url = "https://open.larksuite.com/open-apis/im/v1/messages?receive_id_type=chat_id"
    data = {
        "receive_id": CHAT_ID,
        "msg_type": "text",
        "content": json.dumps({"text": text})
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode(),
        method="POST",
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
    )
    return urllib.request.urlopen(req).read()

# 读取 Bitable 任务
def get_tasks():
    url = f"https://open.larksuite.com/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records?page_size=10"
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {get_token()}'})
    return json.loads(urllib.request.urlopen(req).read())

# 定时执行
def main():
    tasks_data = get_tasks()
    items = tasks_data.get('data', {}).get('items', [])
    
    task_list = "\n".join([
        f"- {item['fields'].get('任务名称', '未命名')}" 
        for item in items[:5]
    ])
    
    message = f"📋 今日任务概览\n\n{task_list}\n\n更多任务请查看 Bitable"
    send_message(message)
    print("报告已发送")

if __name__ == '__main__':
    main()
```

## API 文档

- [飞书开放平台](https://open.larksuite.com/)
- [应用权限配置](https://open.larksuite.com/document/server-docs/getting-started/overview)
- [IM 消息 API](https://open.larksuite.com/document/server-docs/im-v1/message-content-description)
- [Bitable API](https://open.larksuite.com/document/server-docs/bitable-v1)
- [Wiki API](https://open.larksuite.com/document/server-docs/wiki-v2)
- [Webhooks](https://open.larksuite.com/document/server-docs/getting-started/using-webhooks)

## 注意事项

1. **Token 有效期**：tenant_access_token 有效期 2 小时，需缓存复用
2. **频率限制**：API 有调用频率限制，批量操作需加延时
3. **权限配置**：需在飞书开放平台给应用开通相应权限
4. **签名验证**：接收消息时需验证签名确保安全
