# SKILL.md - 读取微信公众号文章

## 触发条件
用户要求读取某个公众号的文章列表，或读取某篇文章的正文内容时激活。

## 前置条件
WeWe RSS 服务必须已部署并运行在 `http://localhost:4000`。
- 如果服务未运行或未部署 → 调用 `wewe-rss-deploy` Skill 进行部署
- 部署完成后继续执行以下流程

## 工作流程

### Step 1：获取配置路径

读取工作目录下的 `tools\wewe-rss-config.txt` 获取项目路径：
- 如果文件不存在，使用默认路径：`~/.openclaw/workspace/wewe-rss-main`

### Step 2：检查服务是否运行

```powershell
netstat -ano | Select-String ":4000"
```
- 如果无响应 → 调用 `wewe-rss-deploy` Skill

### Step 3：获取公众号 mp_id

**方式 A：通过公众号名称查询数据库**

数据库路径：`{WEWE_RSS_PATH}/apps/server/data/wewe-rss.db`

```python
import sqlite3
import os

# 读取项目路径配置
config_path = os.path.expanduser("~/.openclaw/workspace/tools/wewe-rss-config.txt")
if os.path.exists(config_path):
    with open(config_path) as f:
        wewe_rss_path = f.read().strip()
else:
    wewe_rss_path = os.path.expanduser("~/.openclaw/workspace/wewe-rss-main")

db_path = os.path.join(wewe_rss_path, "apps/server/data/wewe-rss.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 查找公众号 mp_id
cursor.execute("SELECT mp_id, nickname FROM feeds WHERE nickname LIKE ?", (f'%{公众号名称}%',))
result = cursor.fetchone()
mp_id = result[0] if result else None
```

**方式 B：通过文章链接提取 __biz**

从微信文章链接提取 `__biz` 参数，然后查数据库：
```
文章链接格式：https://mp.weixin.qq.com/s/xxxxxxxxx
__biz 参数：链接中 ?__biz=MTI0OTk2xxx
```

```python
# 查询数据库获取 mp_id
cursor.execute("SELECT mp_id FROM feeds WHERE mp_id LIKE ?", (f'%{biz_str}%',))
```

### Step 4：调用 API 获取文章列表

```bash
GET http://localhost:4000/feeds/{mp_id}.json?limit=10
```

**请求参数：**
| 参数 | 类型 | 说明 |
|------|------|------|
| `mp_id` | string | 公众号 ID，如 `MP_WXS_3223096120` |
| `limit` | int | 返回文章数量，默认 10 |
| `update` | bool | 是否强制从微信读书更新 |

**响应格式：**
```json
[
  {
    "content": "<article HTML content>",
    "url": "https://mp.weixin.qq.com/s/iBCNkORwkff3PL1EZD3zqw",
    "title": "文章标题",
    "image": "https://mmbiz.qpic.cn/...",
    "date_modified": "2026-04-02T02:20:36.000Z"
  }
]
```

**curl 示例（跨平台）：**
```bash
curl -s "http://localhost:4000/feeds/${mp_id}.json?limit=5" --max-time 15
```

### Step 5：解析正文内容

`content` 字段是完整 HTML，提取纯文本：

```python
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip_tags = {'script', 'style', 'nav', 'footer', 'header', 'aside'}
        self.current_tag = None
    
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        if tag in self.skip_tags:
            return
        if tag == 'p':
            self.text.append('\n')
    
    def handle_data(self, data):
        if self.current_tag not in self.skip_tags:
            text = data.strip()
            if text:
                self.text.append(text)
    
    def get_text(self):
        return '\n'.join(self.text)

# 使用
extractor = TextExtractor()
extractor.feed(html_content)
article_text = extractor.get_text()
```

## 数据库信息

| 表名 | 字段 | 说明 |
|------|------|------|
| `feeds` | `mp_id`, `nickname`, `description` | 公众号信息 |
| `articles` | `id`, `mp_id`, `title`, `url`, `publish_time` | 文章元数据 |

## 完整调用示例

```python
import sqlite3
import subprocess
import json
import os
from html.parser import HTMLParser

# 1. 检查服务是否运行
result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
if ':4000' not in result.stdout:
    # CALL: wewe-rss-deploy
    pass

# 2. 获取项目路径
config_path = os.path.expanduser("~/.openclaw/workspace/tools/wewe-rss-config.txt")
if os.path.exists(config_path):
    with open(config_path) as f:
        wewe_rss_path = f.read().strip()
else:
    wewe_rss_path = os.path.expanduser("~/.openclaw/workspace/wewe-rss-main")

db_path = os.path.join(wewe_rss_path, "apps/server/data/wewe-rss.db")

# 3. 获取 mp_id
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT mp_id FROM feeds WHERE nickname LIKE ?", ('%数字生命卡兹克%',))
mp_id = cursor.fetchone()[0]

# 4. 获取文章列表
import urllib.request
url = f"http://localhost:4000/feeds/{mp_id}.json?limit=3"
with urllib.request.urlopen(url, timeout=15) as response:
    articles = json.loads(response.read().decode('utf-8'))

# 5. 提取第一篇文章正文
first = articles[0]
article_title = first['title']
article_url = first['url']
article_content = first['content']

# 6. 解析纯文本
extractor = TextExtractor()
extractor.feed(article_content)
article_text = extractor.get_text()

print(f"标题: {article_title}")
print(f"链接: {article_url}")
print(f"正文（前500字）: {article_text[:500]}")
```

## 注意事项

1. **服务地址**：默认 `http://localhost:4000`
2. **首次使用**：需要先在 Web UI 登录微信读书账号并订阅公众号
3. **更新频率**：微信读书有频率限制，频繁更新可能被限流
4. **AUTH_CODE**：如果 API 返回 401，检查 `.env` 中的 `AUTH_CODE` 配置

## 错误处理

| 错误 | 原因 | 处理方式 |
|------|------|----------|
| `netstat :4000` 无结果 | 服务未运行 | 调用 `wewe-rss-deploy` Skill |
| 数据库为空 | 未添加账号/订阅 | 提示用户在 Web UI 中配置 |
| API 返回 401 | 需要 AUTH_CODE | 在 `.env` 中获取 AUTH_CODE |
| `content` 为空 | 文章未缓存 | 添加 `update=true` 参数强制更新 |
| `mp_id` 为空 | 公众号未订阅 | 提示用户先订阅公众号 |
