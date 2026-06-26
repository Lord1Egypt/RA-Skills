---
name: xhs-download
description: 小红书笔记批量下载。通过已登录 Chrome 的 DevTools Protocol 自动化下载小红书笔记（图片+文字）到本地。
---

# 小红书笔记批量下载

通过 Chrome DevTools Protocol (CDP) 批量下载小红书笔记到本地文件夹。

## 前置条件

1. **Chrome 已登录小红书**（任何方式启动均可）
2. **Chrome 开启远程调试**：启动时加 `--remote-debugging-port=9222`
3. **Python3 环境**：`pip3 install websocket-client requests`

> 如果 Chrome 已启动但没开调试端口，关闭后重启即可。

## 使用方法（4步）

### 第1步：找到目标账号的 profile_id

打开小红书网页版，进入目标账号主页，复制 URL 最后一段：

```
https://www.xiaohongshu.com/user/profile/64902d2d000000001c0294eb
                                                 ↑ 这个就是 profile_id
```

### 第2步：获取 Chrome tab_id

在终端运行：
```bash
curl -s http://127.0.0.1:9222/json | python3 -m json.tool | grep -E '"id"|"url"'
```

找到包含 `xiaohongshu.com` 的那条记录，复制其 `id` 值。

### 第3步：修改脚本配置

将下方脚本开头的三个变量改成你的值：

| 变量 | 填什么 | 示例 |
|------|--------|------|
| `PROFILE_ID` | 第1步获取的账号ID | `"64902d2d000000001c0294eb"` |
| `TAB_ID` | 第2步获取的tab ID | `"4C23291E2F8B1524..."` |
| `SAVE_DIR` | 你想保存到的文件夹 | `"~/Downloads/我的笔记/"` |

### 第4步：运行脚本

把脚本保存为 `download.py`，然后运行：
```bash
python3 download.py
```

## 完整脚本

```python
import json, time, requests, os, subprocess, websocket, re

# ===== 改这里 =====
PROFILE_ID = "你的目标账号ID"
TAB_ID = "你的Chrome tab_id"
SAVE_DIR = "~/Downloads/你的文件夹/"
# =================

SAVE_DIR = os.path.expanduser(SAVE_DIR)
os.makedirs(SAVE_DIR, exist_ok=True)

def send(ws, method, params={}):
    """CDP 命令发送。3个参数：ws连接对象, 方法名, 参数字典"""
    msg_id = int(time.time()*1000) % 100000
    msg = {"id": msg_id, "method": method, "params": params}
    ws.send(json.dumps(msg))
    while True:
        resp = json.loads(ws.recv())
        if resp.get("id") == msg_id:
            return resp

def download_image(url, path):
    """下载图片，必须带 Referer"""
    r = requests.get(url, headers={"Referer": "https://www.xiaohongshu.com/"}, timeout=30)
    if len(r.content) > 100:
        with open(path, 'wb') as f:
            f.write(r.content)
        return True
    return False

# 1. 连接 Chrome
ws = websocket.create_connection(
    f"ws://127.0.0.1:9222/devtools/page/{TAB_ID}", timeout=30)
print(f"已连接 Chrome tab: {TAB_ID}")

# 2. 导航到目标主页
url = f"https://www.xiaohongshu.com/user/profile/{PROFILE_ID}"
send(ws, "Page.navigate", {"url": url})
time.sleep(6)
print(f"已导航到: {url}")

# 3. 滚动加载所有笔记（30次，覆盖绝大多数账号）
print("滚动加载中...")
for i in range(30):
    send(ws, "Input.synthesizeScrollGesture", {
        "x": 500, "y": 600,
        "xDistance": 0, "yDistance": -800,
        "speed": 2000
    })
    time.sleep(2)
    if (i + 1) % 10 == 0:
        print(f"  已滚动 {i+1}/30 次")

# 4. 从 DOM 提取笔记列表
result = send(ws, "Runtime.evaluate", {"expression": """
(() => {
    const cards = document.querySelectorAll(".feeds-container .note-item");
    return JSON.stringify(Array.from(cards).map(c => {
        const a = c.querySelector("a[href*='/explore/']");
        return {
            href: a ? a.getAttribute("href") : "",
            title: a ? a.innerText.trim().substring(0, 60) : ""
        };
    }));
})()
"""})
notes = json.loads(result["result"]["result"]["value"])
print(f"\n找到 {len(notes)} 篇笔记\n")

# 5. 从 __INITIAL_STATE__ 获取所有笔记的 xsecToken
state_result = send(ws, "Runtime.evaluate", {"expression": """
(() => {
    const state = window.__INITIAL_STATE__ || {};
    const user = state.user || {};
    const notes = user.notes || {};
    const items = (notes._value && notes._value.items) ? notes._value.items : [];
    return JSON.stringify(items.map(n => ({
        id: (n.note && n.note.id) || '',
        xsecToken: (n.note && n.note.xsecToken) || ''
    })));
})()
"""})
token_map = {}
for item in json.loads(state_result["result"]["result"]["value"]):
    if item["id"]:
        token_map[item["id"]] = item["xsecToken"]

# 6. 逐篇下载
downloaded = 0
skipped = 0
for note in notes:
    href = note.get("href", "")
    title = note.get("title", "").strip()
    if not href or not title:
        continue

    note_dir = os.path.join(SAVE_DIR, title)
    if os.path.exists(note_dir):
        print(f"⏭ 跳过（已存在）: {title[:30]}")
        skipped += 1
        continue

    os.makedirs(note_dir, exist_ok=True)

    # 提取 note_id
    m = re.search(r'/explore/([a-f0-9]+)', href)
    note_id = m.group(1) if m else ""
    if not note_id:
        continue

    xsec_token = token_map.get(note_id, "")

    # 导航到详情页
    if xsec_token:
        detail_url = f"https://www.xiaohongshu.com/explore/{note_id}?xsec_token={xsec_token}"
    else:
        detail_url = f"https://www.xiaohongshu.com/explore/{note_id}"
    send(ws, "Page.navigate", {"url": detail_url})
    time.sleep(4)

    # 提取图片列表
    img_result = send(ws, "Runtime.evaluate", {"expression": """
    (() => {
        const swiper = document.querySelector('.swiper-wrapper');
        const imgs = swiper ? swiper.querySelectorAll('img') : [];
        return JSON.stringify(Array.from(imgs).map((img, i) => ({
            i, src: img.src
        })));
    })()
    """})
    images = json.loads(img_result["result"]["result"]["value"])

    # 下载图片
    img_count = 0
    for img in images:
        src = img.get("src", "")
        if src:
            path = os.path.join(note_dir, f"{img['i']+1}.jpg")
            if download_image(src, path):
                img_count += 1

    # 提取正文
    text_result = send(ws, "Runtime.evaluate", {"expression": """
    (() => {
        const desc = document.querySelector('.note-content .desc');
        return desc ? desc.innerText : document.title || '';
    })()
    """})
    text = text_result["result"]["result"].get("value", "")
    with open(os.path.join(note_dir, "内容.txt"), "w", encoding="utf-8") as f:
        f.write(text)

    downloaded += 1
    print(f"✅ {title[:30]}... ({img_count}张图)")

ws.close()
print(f"\n{'='*40}")
print(f"完成！下载 {downloaded} 篇，跳过 {skipped} 篇")
print(f"保存位置: {SAVE_DIR}")
```

## 输出格式

每篇笔记一个文件夹：
```
~/Downloads/你的文件夹/
├── 笔记标题1/
│   ├── 内容.txt
│   ├── 1.jpg
│   ├── 2.jpg
│   └── 3.jpg
└── 笔记标题2/
    ├── 内容.txt
    └── 1.jpg
```

## 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| `Connection refused` | Chrome 没开调试端口 | 加 `--remote-debugging-port=9222` 重启 |
| 图片下载失败/403 | 缺少 Referer | 脚本已自带，别删 headers |
| 笔记数量比预期少 | 滚动次数不够 | 把 30 改成 50 |
| `send()` 不返回 | 参数不对 | 必须是 3 个参数：`send(ws, method, params={})` |
| `websocket` 模块找不到 | 没装依赖 | `pip3 install websocket-client` |

## 注意事项

- 脚本会自动跳过已下载的笔记（文件夹已存在）
- 每次导航详情页需要 4 秒等待加载
- 图片下载必须带 `Referer` 头，否则 403
- 大批量下载建议分段运行（避免被限流）
