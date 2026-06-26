---
name: xhs-search
description: |
  小红书内容搜索技能。通过 MCP 协议调用 xiaohongshu-mcp 工具，搜索小红书笔记、用户主页、评论等。支持关键词搜索、热度排序、内容详情提取。当用户说"搜一下小红书"、"分析小红书"、"查找小红书帖子"、"生成小红书报告"时触发此技能。
---

# xhs-search

小红书内容搜索技能。使用已登录的小红书账号，通过 MCP 服务搜索和提取小红书内容。

## 前置条件

### 1. 安装 xiaohongshu-mcp

```bash
# 下载 macOS amd64 版本（其他系统替换文件名）
curl -L -o ~/Downloads/xhs-mcp.tar.gz \
  "https://github.com/xpzouying/xiaohongshu-mcp/releases/latest/download/xiaohongshu-mcp-darwin-amd64.tar.gz"

cd ~/Downloads && tar -xzf xhs-mcp.tar.gz
mkdir -p ~/.local/bin
mv xiaohongshu-login xiaohongshu-mcp ~/.local/bin/
chmod +x ~/.local/bin/xiaohongshu-*
```

### 2. 扫码登录（一次性）

在 Mac/有显示器的 Linux 上运行：

```bash
~/.local/bin/xiaohongshu-login -bin "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
```

- 弹出浏览器窗口 → 小红书 App 扫码授权
- 登录状态保存在本地 Cookie 文件中，长期有效

### 3. 启动 MCP 服务

```bash
~/.local/bin/xiaohongshu-mcp -bin "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" -port ":18060"
```

服务常驻后台，开机自动启动（可加入 launchd/systemd）。

---

## 使用方法

### 基本搜索

用户提供关键词 → 调用 MCP search_feeds → 返回结果

### 可用工具（MCP tools）

| 工具名 | 用途 |
|--------|------|
| `check_login_status` | 检查登录状态 |
| `search_feeds` | 关键词搜索笔记 |
| `list_feeds` | 获取首页推荐 |
| `get_feed_detail` | 获取帖子详情（需 feed_id + xsec_token）|
| `user_profile` | 获取用户主页（需 user_id）|
| `like_feed` | 点赞/取消点赞 |
| `favorite_feed` | 收藏/取消收藏 |
| `publish_content` | 发布图文笔记 |

---

## Python 调用示例

```python
import urllib.request, json

MCP_URL = "http://localhost:18060/mcp"

def mcp_init():
    payload = json.dumps({"jsonrpc":"2.0","id":1,"method":"initialize",
        "params":{"protocolVersion":"2024-11-05","capabilities":{},
                  "clientInfo":{"name":"agent","version":"1.0"}}}).encode()
    req = urllib.request.Request(MCP_URL, data=payload,
        headers={"Content-Type":"application/json","Accept":"application/json, text/event-stream"})
    sid = urllib.request.urlopen(req, timeout=30).headers.get("Mcp-Session-Id","")
    
    # 发送 initialized 通知
    notif = json.dumps({"jsonrpc":"2.0","method":"notifications/initialized","params":{}}).encode()
    nr = urllib.request.Request(MCP_URL, data=notif,
        headers={"Content-Type":"application/json","Accept":"application/json, text/event-stream","Mcp-Session-Id":sid})
    urllib.request.urlopen(nr, timeout=10)
    return sid

def mcp_call(tool, args, sid):
    payload = json.dumps({"jsonrpc":"2.0","id":2,"method":"tools/call",
        "params":{"name":tool,"arguments":args}}).encode()
    req = urllib.request.Request(MCP_URL, data=payload,
        headers={"Content-Type":"application/json","Accept":"application/json, text/event-stream","Mcp-Session-Id":sid})
    resp = urllib.request.urlopen(req, timeout=60)
    return json.loads(resp.read().decode())

# 使用
sid = mcp_init()
r = mcp_call("search_feeds", {"keyword":"关键词","filters":{"sort_by":"最新"}}, sid)
feeds = json.loads(r["result"]["content"][0]["text"])["feeds"]
```

---

## 搜索结果字段说明

每个笔记包含：

| 字段 | 说明 |
|------|------|
| `id` | 笔记ID（用于获取详情）|
| `noteCard.displayTitle` | 标题 |
| `noteCard.user.nickName` | 作者昵称 |
| `noteCard.interactInfo.likedCount` | 点赞数 |
| `noteCard.interactInfo.collectedCount` | 收藏数 |
| `noteCard.interactInfo.commentCount` | 评论数 |
| `xsecToken` | 访问令牌（获取详情时需要）|

---

## 注意事项

- 排序选项仅支持 `最新`（其他值会返回错误）
- 部分笔记详情因隐私设置可能不可访问
- 搜索结果每次最多约44条
- Cookie 过期后重新运行登录工具扫码即可

## 免责声明

1. **仅供个人研究学习使用**，不得用于商业数据采集、批量内容抓取，或任何违反小红书平台服务条款的活动。
2. 本技能依赖第三方开源工具 [xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp)，该工具的版权归原作者所有。
3. 用户使用本技能产生的任何行为及后果，由用户自行承担。
4. 本技能发布者与小红书平台无任何关联。
