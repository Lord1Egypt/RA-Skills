---
name: xiaohongshu
description: 小红书全能助手 — 文案生成、封面制作、内容发布与管理。当用户要求写小红书笔记、生成小红书文案/标题/封面、发小红书、搜索小红书、评论点赞收藏等任何小红书相关操作时使用。支持一站式从文案创作到自动发布的完整流程。封面图使用纯ImageMagick生成，无需API配置。
metadata: {"openclaw": {"emoji": "📕", "requires": {"bins": ["convert"], "anyBins": ["curl"]}}}
---

# 📕 小红书全能助手

两大核心能力：**文案创作**（标题+正文+封面图）和 **平台操作**（发布+搜索+互动）。

文案创作默认使用当前对话的主模型，无需额外配置。

**重要提示**：当使用发布功能时，正文中不要包含以#开头的话题标签，所有话题标签都应通过`tags`参数传递给MCP服务。

---

## 零、查看可用模型（仅当用户询问时）

当用户询问"有哪些模型"、"当前模型"、"可用模型"、"能用什么模型"时，读取配置文件展示：

```bash
# 查看当前主模型
cat ~/.openclaw/openclaw.json | jq -r '.agents.defaults.model.primary // .agents.defaults.model // "未设置"' 2>/dev/null

# 查看所有可用模型（提供商/模型ID - 名称）
cat ~/.openclaw/openclaw.json | jq -r '.models.providers | to_entries[] | .key as $p | .value.models[]? | "\($p)/\(.id) - \(.name)"' 2>/dev/null
```

---

## 一、文案创作流程

当用户要求写笔记、生成文案、创作小红书内容时，按 **标题 → 正文 → 封面图** 三步执行，每步需用户确认后再继续。

### 1.1 生成标题

**优先使用当前对话模型直接生成**，参考 [references/title-guide.md]({baseDir}/references/title-guide.md) 中的规范生成5个不同风格的标题。

核心要求：每个标题使用不同风格，20字以内，含1-2个emoji，禁用平台禁忌词。

**备用方案**：如果用户明确配置了 `XHS_AI_API_KEY` 环境变量并要求使用指定 API，可调用脚本：
```bash
bash {baseDir}/scripts/generate.sh title "内容摘要"
```

**输出后询问用户**：选择哪个标题？可修改或自定义。默认选第一个。

### 1.2 生成正文

**优先使用当前对话模型直接生成**，参考 [references/content-guide.md]({baseDir}/references/content-guide.md) 中的规范，根据选定标题生成正文。

核心要求：600-800字，像朋友聊天的语气，禁用列表/编号，用自然段落呈现，文末5-10个#标签。

**备用方案**：如果用户明确配置了 `XHS_AI_API_KEY` 环境变量并要求使用指定 API，可调用脚本：
```bash
bash {baseDir}/scripts/generate.sh content "完整内容" "选定标题"
```

**输出后询问用户**：是否满意？可要求修改。确认后进入封面图步骤。

### 1.3 生成封面图

封面图使用纯 ImageMagick 生成，无需 API 配置。

#### 封面图特点
- **尺寸**：1080x1440（3:4比例，适合小红书）
- **样式**：纯色背景 + 标题文字
- **字体**：固定 96px 大小，自动换行
- **颜色**：自动选择美观的浅色背景和深色文字组合

#### 使用方法
直接调用 cover.sh 脚本，仅需两个参数：

```bash
bash {baseDir}/scripts/cover.sh "标题文字" [输出路径]
```

**参数说明**：
1. **标题文字**（必填）：封面显示的标题
2. **输出路径**（可选）：封面图保存路径，默认 `/tmp/xhs_cover.png`

**示例**：
```bash
# 基本用法
bash cover.sh "新加坡留学攻略" /tmp/cover.png

# 使用默认输出路径
bash cover.sh "留学费用详解"
```

#### 封面图前置要求
- ImageMagick（`convert` 或 `magick`）
- 中文字体（`fonts-noto-cjk`）

### 1.4 文案完成后

询问用户是否要直接发布到小红书。如果要发布，自动进入下方「平台操作」的发布流程。

---

## 二、平台操作

当用户要求发帖、搜索、评论等小红书操作时使用。所有命令在云服务器本地执行，MCP 服务运行在 `http://localhost:18060/mcp`。

### 2.1 前置检查

每次操作前必须先执行：

```bash
bash {baseDir}/check_env.sh
```

返回码：`0` = 正常已登录 → 调用工具；`1` = 未安装 → 安装 MCP 服务；`2` = 未登录 → 扫码登录流程。

### 2.2 调用工具

**⚠️ 极其重要**：小红书 MCP 使用 Streamable HTTP 模式。每次调用都必须：初始化 → 获取 Session ID → 带 Session ID 调用工具。三步在同一个 exec 中执行。

```bash
MCP_URL="${XHS_MCP_URL:-http://localhost:18060/mcp}"

# 初始化并获取 Session ID
SESSION_ID=$(curl -s -D /tmp/xhs_headers -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"openclaw","version":"1.0"}},"id":1}' > /dev/null && grep -i 'Mcp-Session-Id' /tmp/xhs_headers | tr -d '\r' | awk '{print $2}')

# 确认初始化
curl -s -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}' > /dev/null

# 调用工具（替换 <工具名> 和 <参数>）
curl -s -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"<工具名>","arguments":{<参数>}},"id":2}'
```

注意：每次调用都必须重新初始化获取新 Session ID，三步必须在同一个 exec 中顺序执行。

### 2.3 可用工具

#### 1. check_login_status — 检查登录状态
- **触发词**: "检查登录"、"登录状态"
- **参数**: 无

#### 2. get_login_qrcode — 获取登录二维码
- **触发词**: "获取二维码"、"扫码登录"
- **参数**: 无
- **返回**: Base64 图片和超时时间

#### 3. delete_cookies — 重置登录状态
- **触发词**: "退出登录"、"重新登录"、"清除登录"
- **参数**: 无
- **注意**: 删除后需要重新扫码登录

#### 4. publish_content — 发布图文内容
- **触发词**: "发小红书"、"发布笔记"、"发图文"
- **参数**:
  - `title`: 标题，≤20字（必填）
  - `content`: 正文，≤1000字（必填），**注意：正文中不要包含以#开头的话题标签，所有话题标签都用tags参数来生成和提供即可**
  - `images`: 图片本地绝对路径数组（必填），如 `["/tmp/food1.jpg"]`
  - `tags`: 话题标签数组（可选），如 `["美食", "旅行", "生活"]`
  - `products`: 商品关键词列表（可选），用于绑定带货商品，填写商品名称或商品ID，系统会自动搜索并选择第一个匹配结果。需账号已开通商品功能。示例: ["面膜", "防晒霜SPF50"]
  - `schedule_at`: 定时发布时间（可选），ISO8601格式如 2024-01-20T10:30:00+08:00，支持1小时到14天内。不填则立即发布
  - `visibility`: 可见范围（可选），支持: 公开可见(默认)、仅自己可见、仅互关好友可见。不填则默认公开可见

#### 5. publish_with_video — 发布视频内容
- **触发词**: "发视频"、"发布视频笔记"
- **参数**:
  - `title`: 标题（必填）
  - `content`: 描述（必填），**注意：描述中不要包含以#开头的话题标签，所有话题标签都用tags参数来生成和提供即可**
  - `video`: 视频文件本地绝对路径（必填）
  - `tags`: 话题标签数组（可选），如 `["美食", "旅行", "生活"]`
  - `products`: 商品关键词列表（可选），用于绑定带货商品，填写商品名称或商品ID，系统会自动搜索并选择第一个匹配结果。需账号已开通商品功能。示例: ["面膜", "防晒霜SPF50"]
  - `schedule_at`: 定时发布时间（可选），ISO8601格式如 2024-01-20T10:30:00+08:00，支持1小时到14天内。不填则立即发布
  - `visibility`: 可见范围（可选），支持: 公开可见(默认)、仅自己可见、仅互关好友可见。不填则默认公开可见

#### 6. search_feeds — 搜索内容
- **触发词**: "搜索小红书"、"找笔记"、"搜一下"
- **参数**:
  - `keyword`: 搜索关键词（必填）

#### 7. list_feeds — 获取推荐列表
- **触发词**: "推荐内容"、"首页推荐"
- **参数**: 无

#### 8. get_feed_detail — 获取帖子详情
- **触发词**: "看看这个帖子"、"帖子详情"
- **参数**:
  - `feed_id`: 帖子ID（从搜索/推荐结果获取，必填）
  - `xsec_token`: 安全token（从搜索/推荐结果获取，必填）
  - `load_all_comments`: 是否加载全部评论，默认 false 仅返回前 10 条（可选）
  - `click_more_replies`: 是否展开二级回复，仅 load_all_comments=true 时生效（可选）
  - `limit`: 限制加载的一级评论数量，默认 20（可选）
  - `reply_limit`: 跳过回复数过多的评论，默认 10（可选）
  - `scroll_speed`: 滚动速度 slow/normal/fast（可选）

#### 9. like_feed — 点赞/取消点赞
- **触发词**: "点赞"、"取消点赞"、"喜欢这个"
- **参数**:
  - `feed_id`: 帖子ID（必填）
  - `xsec_token`: 安全token（必填）
  - `unlike`: 是否取消点赞，true=取消，默认 false=点赞（可选）

#### 10. favorite_feed — 收藏/取消收藏
- **触发词**: "收藏"、"取消收藏"、"收藏这个"
- **参数**:
  - `feed_id`: 帖子ID（必填）
  - `xsec_token`: 安全token（必填）
  - `unfavorite`: 是否取消收藏，true=取消，默认 false=收藏（可选）

#### 11. post_comment_to_feed — 发表评论
- **触发词**: "评论这个"、"发表评论"
- **参数**:
  - `feed_id`: 帖子ID（必填）
  - `xsec_token`: 安全token（必填）
  - `content`: 评论内容（必填）

#### 12. reply_comment_in_feed — 回复评论
- **触发词**: "回复评论"、"回复这条"
- **参数**:
  - `feed_id`: 帖子ID（必填）
  - `xsec_token`: 安全token（必填）
  - `content`: 回复内容（必填）
  - `comment_id`: 目标评论ID，从评论列表获取（可选）
  - `user_id`: 目标评论用户ID，从评论列表获取（可选）

#### 13. user_profile — 获取用户主页
- **触发词**: "看看这个博主"、"用户主页"
- **参数**:
  - `user_id`: 用户ID（必填）
  - `xsec_token`: 安全token（必填）

### 2.4 使用示例

**搜索**：
```bash
MCP_URL="http://localhost:18060/mcp"
SESSION_ID=$(curl -s -D /tmp/xhs_headers -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"openclaw","version":"1.0"}},"id":1}' > /dev/null && grep -i 'Mcp-Session-Id' /tmp/xhs_headers | tr -d '\r' | awk '{print $2}')
curl -s -X POST "$MCP_URL" -H "Content-Type: application/json" -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}' > /dev/null
curl -s -X POST "$MCP_URL" -H "Content-Type: application/json" -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"search_feeds","arguments":{"keyword":"美食探店"}},"id":2}'
```

**发布图文内容（带tags参数）**：
```bash
MCP_URL="http://localhost:18060/mcp"
SESSION_ID=$(curl -s -D /tmp/xhs_headers -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"openclaw","version":"1.0"}},"id":1}' > /dev/null && grep -i 'Mcp-Session-Id' /tmp/xhs_headers | tr -d '\r' | awk '{print $2}')
curl -s -X POST "$MCP_URL" -H "Content-Type: application/json" -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}' > /dev/null
curl -s -X POST "$MCP_URL" -H "Content-Type: application/json" -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"publish_content","arguments":{"title":"新加坡私立大学留学指南","content":"分享新加坡私立大学的申请流程和注意事项，包括学校选择、申请材料准备、签证办理等实用信息。","images":["/path/to/image1.jpg","/path/to/image2.jpg"],"tags":["新加坡留学","新加坡私立大学","留学申请","国际教育","海外学习"]}},"id":2}'
```

**重要**：正文中不要包含以#开头的话题标签，所有话题标签都通过`tags`参数传递。

---

## 三、登录流程

当前置检查返回 `2`（未登录）时，询问用户选择登录方式：

> 需要登录小红书，请选择登录方式：
> 1. **快捷扫码** — 直接获取二维码图片（推荐同城/常用设备）
> 2. **截图扫码** — 通过登录工具截屏获取（推荐异地登录，支持短信验证码）
> 3. **手动Cookie** — 直接粘贴浏览器Cookie字符串（推荐已在浏览器登录的用户）

### 方式一：快捷扫码（get_login_qrcode）

通过 MCP 工具直接获取二维码 Base64 图片，流程简洁，但**不支持输入验证码**。异地登录可能触发短信验证，此时需切换为方式二。

#### 步骤 1: 调用 get_login_qrcode 获取二维码

```bash
MCP_URL="${XHS_MCP_URL:-http://localhost:18060/mcp}"
SESSION_ID=$(curl -s -D /tmp/xhs_headers -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"openclaw","version":"1.0"}},"id":1}' > /dev/null && grep -i 'Mcp-Session-Id' /tmp/xhs_headers | tr -d '\r' | awk '{print $2}')
curl -s -X POST "$MCP_URL" -H "Content-Type: application/json" -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}' > /dev/null
curl -s -X POST "$MCP_URL" -H "Content-Type: application/json" -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"get_login_qrcode","arguments":{}},"id":2}'
```

#### 步骤 2: 将 Base64 转为图片文件

从返回结果中提取 Base64 字符串（去掉 `data:image/png;base64,` 前缀），保存为图片：

```bash
# 假设 BASE64_STR 为提取到的 Base64 内容（不含 data:image/png;base64, 前缀）
echo "$BASE64_STR" | base64 -d > /tmp/xhs_qr.png
```

#### 步骤 3: 发送二维码给用户

#### 步骤 4: 等待扫码并验证

告知用户扫码，扫码后用 `check_login_status` 工具验证是否登录成功。二维码过期则重新执行步骤 1-3。

---

### 方式二：截图扫码（登录工具 + Xvfb 截屏）

通过 GUI 登录工具获取二维码，**支持异地登录时输入短信验证码**。

#### 步骤 1: 启动登录工具

所有命令必须用 nohup 后台运行，否则会因超时被中断。

```bash
pkill -f xiaohongshu-login 2>/dev/null
sleep 1
cd ~/xiaohongshu-mcp && DISPLAY=:99 nohup ./xiaohongshu-login-linux-amd64 > login.log 2>&1 &
sleep 5
```

#### 步骤 2: 截取二维码

```bash
DISPLAY=:99 import -window root /tmp/xhs_qr.png
```

#### 步骤 2.1: 检测截图内是否有二维码

```bash
zbarimg -q /tmp/xhs_qr.png
```
- 无输出：二维码未加载，等待 5 秒后重新截图
- 有输出：二维码已生成，继续发送

#### 步骤 3: 发送二维码给用户

#### 步骤 4: 等待扫码

告知用户"已发送二维码，请用小红书APP扫码登录"，等待用户确认。

#### 步骤 4.1: 如提示输入验证码（异地登录常见）

```bash
export DISPLAY=:99
WIN_ID=$(xdotool search --onlyvisible --name '小红书|xiaohongshu|Xiaohongshu' | head -n1)
xdotool type --window "$WIN_ID" --delay 50 '<CODE>'
xdotool key --window "$WIN_ID" Return
```

#### 步骤 5: 验证登录并启动 MCP

```bash
cat ~/xiaohongshu-mcp/login.log | tail -5
# 如果显示 "Login successful"：
pkill -f xiaohongshu 2>/dev/null
cd ~/xiaohongshu-mcp && DISPLAY=:99 nohup ./xiaohongshu-mcp-linux-amd64 > mcp.log 2>&1 &
```

#### 二维码过期

如用户反馈扫码失败，重复步骤 1-3 获取新二维码。

---

### 方式三：手动Cookie登录

当用户提供浏览器复制的 Cookie 字符串时，将其转换为 JSON 数组格式并保存到 `~/xiaohongshu-mcp/cookies.json`。

#### 步骤 1: 接收用户的 Cookie 字符串

用户会提供类似这样的字符串（从浏览器开发者工具复制）：

```
a1=19c464ed2df...; webId=807ede65b...; web_session=040069b4...; xsecappid=xhs-pc-web
```

#### 步骤 2: 转换并保存

将用户提供的 Cookie 字符串按 `;` 分割每个键值对，转换为如下 JSON 数组格式，保存到 `~/xiaohongshu-mcp/cookies.json`：

```python
python3 -c "
import json, sys

cookie_str = sys.argv[1].strip()
cookies = []
for pair in cookie_str.split(';'):
    pair = pair.strip()
    if '=' not in pair:
        continue
    name, value = pair.split('=', 1)
    cookies.append({
        'name': name.strip(),
        'value': value.strip(),
        'domain': '.xiaohongshu.com',
        'path': '/',
        'expires': -1,
        'httpOnly': name.strip() in ('web_session', 'id_token', 'acw_tc'),
        'secure': name.strip() in ('web_session', 'id_token'),
        'session': False,
        'priority': 'Medium',
        'sameParty': False,
        'sourceScheme': 'Secure',
        'sourcePort': 443
    })

with open('$HOME/xiaohongshu-mcp/cookies.json', 'w') as f:
    json.dump(cookies, f, ensure_ascii=False)
print(f'✅ 已保存 {len(cookies)} 个 Cookie 到 cookies.json')
" "用户提供的cookie字符串"
```

#### 步骤 3: 重启 MCP 服务使 Cookie 生效

```bash
pkill -f xiaohongshu-mcp-linux 2>/dev/null
sleep 1
cd ~/xiaohongshu-mcp && DISPLAY=:99 nohup ./xiaohongshu-mcp-linux-amd64 > mcp.log 2>&1 &
sleep 3
```

#### 步骤 4: 验证登录状态

用 `check_login_status` 工具验证是否登录成功。如果失败，提示用户 Cookie 可能已过期，建议重新从浏览器获取或改用扫码登录。

**注意事项**：
- Cookie 中最关键的字段是 `web_session` 和 `a1`，缺少这两个会导致登录失败
- 浏览器登录状态和 MCP 登录状态会互相覆盖，导入后建议不要在浏览器再登录同一账号

---

## 四、安装 MCP 服务（仅首次）

当前置检查返回 `1` 时执行。

### 确认系统环境

```bash
hostnamectl
```

根据 `Operating System` 确定包管理器（apt/yum/dnf），根据 `Architecture` 确定二进制版本（x86_64=amd64, aarch64=arm64）。

### 安装依赖

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install -y xvfb imagemagick zbar-tools xdotool fonts-noto-cjk

# CentOS/RHEL
sudo yum install -y xorg-x11-server-Xvfb ImageMagick zbar xdotool
```

### 启动虚拟显示

```bash
# 快速启动
Xvfb :99 -screen 0 1920x1080x24 &

# 或 systemd 服务（推荐，开机自启）
cat > /etc/systemd/system/xvfb.service << 'EOF'
[Unit]
Description=X Virtual Frame Buffer
After=network.target

[Service]
ExecStart=/usr/bin/Xvfb :99 -screen 0 1920x1080x24
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable xvfb && sudo systemctl start xvfb
```

### 下载 MCP 服务

项目地址：https://github.com/xpzouying/xiaohongshu-mcp/releases

```bash
mkdir -p ~/xiaohongshu-mcp && cd ~/xiaohongshu-mcp

# 根据架构选择（云服务器通常是 x86_64 = amd64）
ARCH="amd64"  # 如果是 ARM 服务器改为 arm64
wget https://github.com/xpzouying/xiaohongshu-mcp/releases/latest/download/xiaohongshu-mcp-linux-${ARCH}.tar.gz
tar xzf xiaohongshu-mcp-linux-${ARCH}.tar.gz
chmod +x xiaohongshu-*
```

### 启动 MCP 服务

**推荐使用 systemd 守护（崩溃自动重启 + 开机自启）：**

```bash
cat > /etc/systemd/system/xhs-mcp.service << 'EOF'
[Unit]
Description=Xiaohongshu MCP Service
After=network.target xvfb.service
Requires=xvfb.service

[Service]
Environment=DISPLAY=:99
WorkingDirectory=/root/xiaohongshu-mcp
ExecStart=/root/xiaohongshu-mcp/xiaohongshu-mcp-linux-amd64
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable xhs-mcp && sudo systemctl start xhs-mcp
systemctl status xhs-mcp
```

**或手动启动（不推荐，进程退出不会自动恢复）：**

```bash
cd ~/xiaohongshu-mcp
DISPLAY=:99 nohup ./xiaohongshu-mcp-linux-amd64 > mcp.log 2>&1 &
sleep 3
pgrep -f xiaohongshu-mcp && echo "✅ 启动成功" || echo "❌ 启动失败，查看 mcp.log"
```

安装完成后，回到登录流程完成首次登录。

---

## 五、响应处理

成功：解析 `result.content[0].text` 获取数据。
错误：
- `Not logged in`: 未登录，走扫码流程
- `Session expired`: 会话过期，重新登录
- `Rate limited`: 频率限制，稍后重试

## 六、注意事项

1. 标题不超过 **20 字**，正文不超过 **1000 字**
2. 图片/视频必须使用**服务器上的本地绝对路径**
3. 小红书**不支持多设备同时登录**，登录后不要在浏览器再登录
4. 评论间隔建议 > 30 秒，避免频率限制
5. 所有带 GUI 的进程（login、mcp）**必须用 nohup 后台运行**，否则会被 exec 超时中断

## 七、故障排查

```bash
# MCP 服务是否运行
pgrep -f xiaohongshu-mcp-linux

# Xvfb 是否运行
pgrep -x Xvfb

# 查看 MCP 日志
tail -20 ~/xiaohongshu-mcp/mcp.log

# 查看登录日志
tail -20 ~/xiaohongshu-mcp/login.log

# 检查端口
lsof -i :18060
```
