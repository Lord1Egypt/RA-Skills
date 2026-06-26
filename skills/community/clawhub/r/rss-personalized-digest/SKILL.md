# RSS 个性化追踪摘要系统

## 功能概述

每天自动抓取多个 RSS 源，根据用户设定的关键词权重筛选内容，生成带有点击追踪中转链接的个性化摘要。用户点击链接后自动记录并加权相关关键词，下次摘要优先推送相关类容。

**核心流程：**
```
RSS抓取 → 关键词打分 → 生成中转URL → 用户点击阅读 → 自动加权 → 下次优先推送
```

---

## 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    公网用户点击                          │
└───────────→ serveo.net 隧道 ────────────────────────────→┘
                                                 │
                                                 ▼
┌─────────────────────────────────────────────────────────┐
│         localhost:7890  (Node.js 中转服务器)            │
│  1. 记录点击到 /tmp/rss-clicks.log                    │
│  2. 返回 302 跳转到原文                                │
└─────────────────────────────────────────────────────────┘
                     ▲
                     │ SSH 隧道 (serveo.net)
                     │ Port 7890 → 公网
                     │
┌─────────────────────────────────────────────────────────┐
│         RSS 摘要生成脚本 (rss_summary.py)               │
│  1. 读取 rss-weights.json 配置                         │
│  2. 生成带中转URL的摘要                                │
│  3. 查询点击日志，加权被点关键词                       │
└─────────────────────────────────────────────────────────┘
```

---

## 核心文件

| 文件 | 用途 |
|------|------|
| `rss-weights.json` | 关键词权重配置（初始权重+历史加权记录） |
| `rss-redirect-server.js` | Node.js 中转服务器（点击记录+302跳转） |
| `start.sh` | 一键启动脚本（服务器+隧道） |
| `/tmp/rss-clicks.log` | 点击日志（时间戳 + 来源IP + 目标URL） |

---

## 快速启动

### 1. 启动中转服务器

```bash
# 启动 Node.js 中转服务器
node /tmp/rss-redirect-server.js &

# 等待2秒，确认端口监听
sleep 2 && ss -tlnp | grep 7890
```

### 2. 建立 SSH 隧道（serveo.net）

```bash
# 后台运行 serveo.net 隧道
ssh -o StrictHostKeyChecking=no \
    -o ServerAliveInterval=30 \
    -R 80:localhost:7890 \
    serveo.net > /tmp/serveo.log 2>&1 &

# 等待6秒，提取公网URL
sleep 6 && cat /tmp/serveo.log | grep "Forwarding HTTP" | awk '{print $NF}'
```

**输出示例：**
```
https://ec850a76c13b9d96-123-234-101-41.serveousercontent.com
```

### 3. 更新配置

```python
# 更新 rss-weights.json 中的 redirect_base
python3 -c "
import json
with open('/root/.openclaw/workspace/rss-weights.json') as f:
    w = json.load(f)
w['redirect_base'] = 'https://ec850a76c13b9d96-123-234-101-41.serveousercontent.com'
with open('/root/.openclaw/workspace/rss-weights.json', 'w') as f:
    json.dump(w, f, ensure_ascii=False, indent=2)
"
```

---

## 中转 URL 格式

**格式：**
```
{redirect_base}/go/{base64url_safe编码的原文URL}
```

**生成示例（Python）：**
```python
import base64

original = "https://www.highsnobiety.com/p/adidas-tokyo-mj-snakeskin/"
encoded = base64.b64encode(original.encode()).decode()
encoded = encoded.replace('+', '-').replace('/', '_').rstrip('=')
redirect_url = f"{redirect_base}/go/{encoded}"
# https://xxx.serveousercontent.com/go/aHR0cHM6Ly93d3cuaGlnaHNub2JpZXR5LmNvbS9wL2FkaWRhcy10b2t5by1tai1zbmFrZXNraW4v
```

---

## 点击日志格式

**日志文件：** `/tmp/rss-clicks.log`

**格式：**
```
[YYYY-MM-DD HH:MM:SS] FROM:<来源IP> -> <目标URL>
```

**示例：**
```
[2026-04-18 13:46:00] FROM:127.0.0.1 -> https://www.highsnobiety.com/p/adidas-tokyo-mj-snakeskin/
```

**关键词匹配规则：**
- 精确匹配标题/摘要中的关键词
- 大小写不敏感
- 每命中一次，关键词权重 +1

---

## 关键词权重配置

**文件：** `/root/.openclaw/workspace/rss-weights.json`

**结构：**
```json
{
  "version": "1.1",
  "last_updated": "2026-04-18",
  "redirect_base": "https://xxx.serveousercontent.com",
  "server_url": "http://localhost:7890",
  "keywords": {
    "Nike": 4,
    "Adidas": 4,
    "耐克": 4,
    "阿迪达斯": 4,
    "运动鞋服": 3
  },
  "base_weights": {
    "Nike": 4,
    "Adidas": 4,
    "耐克": 4
  },
  "history": [
    {
      "date": "2026-04-18 13:46",
      "source": "click",
      "url": "https://www.highsnobiety.com/...",
      "incremented": ["Adidas: 3 -> 4", "球鞋: 2 -> 3"]
    }
  ]
}
```

**手动加权命令：**
```python
python3 << 'PYEOF'
import json

with open('/root/.openclaw/workspace/rss-weights.json') as f:
    w = json.load(f)

target_kws = ['Nike', 'Adidas', '耐克', '阿迪达斯']
updated = []

for kw, wgt in w['keywords'].items():
    if kw in target_kws:
        w['keywords'][kw] = wgt + 1
        updated.append(f"{kw}: {wgt} -> {wgt+1}")

w['history'].append({
    'date': '2026-04-18 14:00',
    'source': 'manual',
    'incremented': updated
})

with open('/root/.openclaw/workspace/rss-weights.json', 'w') as f:
    json.dump(w, f, ensure_ascii=False, indent=2)

print("已更新:", updated)
PYEOF
```

---

## 服务管理

### 查看服务状态
```bash
# 中转服务器
ss -tlnp | grep 7890

# serveo 隧道
ps aux | grep serveo.net | grep -v grep

# 点击日志
cat /tmp/rss-clicks.log | tail -10
```

### 重启中转服务器
```bash
# 杀掉旧进程
kill $(ps aux | grep "rss-redirect-server" | grep -v grep | awk '{print $2}') 2>/dev/null

# 重启
node /tmp/rss-redirect-server.js &
```

### 重启隧道
```bash
# 杀掉旧隧道
kill $(ps aux | grep "serveo.net" | grep -v grep | awk '{print $2}') 2>/dev/null
sleep 1

# 启动新隧道
ssh -o StrictHostKeyChecking=no \
    -o ServerAliveInterval=30 \
    -R 80:localhost:7890 \
    serveo.net > /tmp/serveo.log 2>&1 &
```

### 健康检查
```bash
curl -s "http://localhost:7890/health"
# 输出: OK
```

---

## RSS 摘要生成流程

### 触发时机
- 手动触发：用户说"做一次摘要"或"发摘要"
- 自动触发：每日定时（通过 cron 配置）

### 生成步骤

```
1. 读取 rss-weights.json 中的关键词权重
2. 抓取所有配置的 RSS 源
3. 对每条内容计算权重得分：
   score = Σ(命中关键词的权重)
4. 按 score 降序排列
5. 生成带中转 URL 的摘要
6. 输出格式：
   序号：中文内容概要
   [点击查看详情](中转URL)
```

### 输出格式
```
**📡 今日热讯 · YYYY-MM-DD（个性化加权版）**

**1. [标题]**
[中文摘要，不超过100字]
[点击查看详情](中转URL)

**2. [标题]**
...
```

---

## RSS 源配置

**默认 RSS 源：**

| 源 | URL | 类型 |
|----|-----|------|
| IT之家 | https://www.ithome.com/rss/ | 科技 |
| 钛媒体 | https://www.tmtpost.com/rss | 科技 |
| 36kr | https://36kr.com/feed | 科技/商业 |
| 爱范儿 | https://www.ifanr.com/feed | 科技 |
| Highsnobiety | https://www.highsnobiety.com/feed/ | 潮流 |
| Complex | https://www.complex.com/feed | 潮流/音乐 |
| The Decoder | https://the-decoder.com/feed/ | AI/科技 |
| Mashable | https://mashable.com/feed | 科技 |

---

## 故障排查

### serveo 隧道断开
**症状：** 用户点击链接无响应

**排查：**
```bash
ps aux | grep serveo | grep -v grep
# 如果没有输出，隧道已断开
```

**解决：**
```bash
kill $(ps aux | grep "rss-redirect" | grep -v grep | awk '{print $2}') 2>/dev/null
sleep 1
node /tmp/rss-redirect-server.js &
sleep 1
ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=30 -R 80:localhost:7890 serveo.net > /tmp/serveo.log 2>&1 &
sleep 6
cat /tmp/serveo.log
```

### 中转服务器崩溃
**症状：** `curl localhost:7890` 无响应

**解决：**
```bash
node /tmp/rss-redirect-server.js &
```

### 点击未记录
**排查：**
```bash
cat /tmp/rss-clicks.log | tail -5
```

**可能原因：**
1. 用户未完成 interstitial 确认页（serveo 免费版限制）
2. 隧道超时断开
3. 用户点击的是原文 URL 而不是中转 URL

### base64 解码错误
**症状：** 日志中出现 `(decode error)`

**排查：**
```python
# 测试编码
import base64
url = "https://example.com"
enc = base64.b64encode(url.encode()).decode()
print(f"Encoded: {enc}")
print(f"Decoded: {base64.b64decode(enc).decode()}")
```

---

## 局限性

1. **serveo.net 免费版**：跳转前需点 interstitial 确认页，无法绕过
2. **SSH 隧道稳定性**：长时间运行可能断开，需配置自动重连
3. **点击归属**：依赖 IP 和 User-Agent，不保证100%准确
4. **服务器在国外**：国内访问 Cloudflare 可能不稳定

## 使用方法

**首次启动：**
```bash
cd /root/.openclaw/workspace/skills/rss-personalized-digest
bash start.sh
```

**生成摘要：**
1. 运行 `feed fetch -o wide` 获取最新内容
2. 根据权重筛选生成带中转 URL 的摘要
3. 发送前查询 `/tmp/rss-clicks.log` 对被点关键词 +1

**查看点击日志：**
```bash
curl -s http://localhost:7890/clicks
# 或
cat /tmp/rss-clicks.log
```

**手动加权：**
修改 `rss-weights.json` 中 `keywords` 字典对应关键词的值，+1 累加。

---

## 扩展方案

### 方案一：Cloudflare Workers（推荐）
- 优点：无拦截跳转，永久固定域名，全球 CDN
- 缺点：需用户手动部署 Worker 代码
- 部署：见下方附录

### 方案二：自建 VPS
- 在有公网 IP 的服务器上运行中转服务
- 优点：完全可控，无第三方限制
- 配置：Nginx 反向代理 + 固定域名

---

## 附录：Cloudflare Workers 部署代码

```javascript
export default {
  async fetch(request) {
    const url = new URL(request.url);
    const path = url.pathname;

    if (path.startsWith('/go/')) {
      let b64 = path.slice(4).replace(/-/g, '+').replace(/_/g, '/');
      while (b64.length % 4) b64 += '=';
      let originalUrl;
      try {
        originalUrl = atob(b64);
      } catch (e) {
        return new Response('Invalid URL', { status: 400 });
      }

      // 发送点击日志到中转服务器
      fetch('http://YOUR_TUNNEL_URL/log?url=' + encodeURIComponent(originalUrl), {
        method: 'GET',
        mode: 'no-cors'
      }).catch(() => {});

      return Response.redirect(originalUrl, 302);
    }

    return new Response('RSS Click Logger\nUsage: /go/<base64url>', { status: 200 });
  }
};
```

**部署步骤：**
1. 登录 https://dash.cloudflare.com
2. Workers 和 Pages → 创建应用程序 → 创建 Worker
3. 粘贴代码，Deploy
4. 将返回的域名填入 `rss-weights.json` 的 `redirect_base`
