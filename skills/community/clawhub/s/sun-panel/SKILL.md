---
name: sun-panel
description: Use this skill when the user wants to add websites, manage shortcuts, create groups, or get icon recommendations for Sun-Panel navigation panel. Keywords: "添加网站", "add website", "sun-panel", "图标推荐", "icon recommend", "快捷方式", "bookmark", "导航面板".
---

# Sun-Panel 导航面板操作指南

Sun-Panel 是一个服务器/NAS导航面板工具。本 skill 帮助 AI Agent 通过 API 操作它。

## 配置文件

配置文件路径：`~/.openclaw/skills/sun-panel/config.json`

### 首次使用流程

1. 检查配置文件是否存在
2. 如果不存在，引导用户创建配置文件
3. 读取配置，登录获取 Token，执行操作

### 配置文件格式

```json
{
  "url": "http://your-sunpanel-host:3002",
  "username": "your_username",
  "password": "your_password"
}
```

### 检查和创建配置

```bash
CONFIG_FILE="$HOME/.openclaw/skills/sun-panel/config.json"

# 检查配置文件是否存在
if [ ! -f "$CONFIG_FILE" ]; then
    echo "首次使用 Sun-Panel 技能，请提供以下信息："
    echo "1. Sun-Panel 服务地址（如 http://192.168.10.3:3002）"
    echo "2. 登录账号"
    echo "3. 登录密码"
    echo ""
    echo "AI Agent 将引导用户输入并创建配置文件"
fi

# 读取配置
SUN_PANEL_URL=$(jq -r '.url' "$CONFIG_FILE")
SUN_PANEL_USERNAME=$(jq -r '.username' "$CONFIG_FILE")
SUN_PANEL_PASSWORD=$(jq -r '.password' "$CONFIG_FILE")
```

### 创建配置文件（AI Agent 执行）

```bash
# 确保目录存在
mkdir -p "$HOME/.openclaw/skills/sun-panel"

# 写入配置文件（使用用户提供的值）
cat > "$HOME/.openclaw/skills/sun-panel/config.json" << 'EOF'
{
  "url": "USER_PROVIDED_URL",
  "username": "USER_PROVIDED_USERNAME",
  "password": "USER_PROVIDED_PASSWORD"
}
EOF

echo "配置已保存到 $HOME/.openclaw/skills/sun-panel/config.json"
```

## 快速开始

### 1. 登录获取 Token

```bash
# 从配置文件读取
CONFIG_FILE="$HOME/.openclaw/skills/sun-panel/config.json"
SUN_PANEL_URL=$(jq -r '.url' "$CONFIG_FILE")
SUN_PANEL_USERNAME=$(jq -r '.username' "$CONFIG_FILE")
SUN_PANEL_PASSWORD=$(jq -r '.password' "$CONFIG_FILE")

# 登录
RESPONSE=$(curl -s -X POST "$SUN_PANEL_URL/api/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$SUN_PANEL_USERNAME\",\"password\":\"$SUN_PANEL_PASSWORD\"}")

# 检查登录结果
if echo "$RESPONSE" | jq -e '.code == 0' > /dev/null; then
    TOKEN=$(echo "$RESPONSE" | jq -r '.data.token')
    echo "登录成功，Token 已获取"
else
    echo "登录失败：$(echo "$RESPONSE" | jq -r '.msg')"
fi
```

## 核心 API

### 获取分组列表

```bash
curl -s -X POST "$SUN_PANEL_URL/api/panel/itemIconGroup/getList" \
  -H "Content-Type: application/json" \
  -H "token: $TOKEN"

# 返回示例：
# {"code":0,"data":{"list":[{"id":1,"title":"开发工具","icon":"","sort":1}]}}
```

### 创建分组

```bash
curl -s -X POST "$SUN_PANEL_URL/api/panel/itemIconGroup/edit" \
  -H "Content-Type: application/json" \
  -H "token: $TOKEN" \
  -d '{"title":"AI工具","icon":"mdi:robot","description":"AI相关工具"}'

# id=0 时创建新分组，返回包含新 id
```

### 批量添加图标

```bash
curl -s -X POST "$SUN_PANEL_URL/api/panel/itemIcon/addMultiple" \
  -H "Content-Type: application/json" \
  -H "token: $TOKEN" \
  -d '[
    {
      "title": "GitHub",
      "url": "https://github.com",
      "lanUrl": "",
      "description": "代码托管平台",
      "icon": {"itemType": 3, "text": "mdi:github"},
      "openMethod": 2,
      "itemIconGroupId": 1
    },
    {
      "title": "ChatGPT",
      "url": "https://chat.openai.com",
      "icon": {"itemType": 3, "text": "mdi:chat"},
      "openMethod": 2,
      "itemIconGroupId": 2
    }
  ]'
```

### 单个添加/编辑图标

```bash
curl -s -X POST "$SUN_PANEL_URL/api/panel/itemIcon/edit" \
  -H "Content-Type: application/json" \
  -H "token: $TOKEN" \
  -d '{
    "title": "Google",
    "url": "https://google.com",
    "icon": {"itemType": 3, "text": "mdi:google"},
    "openMethod": 2,
    "itemIconGroupId": 1
  }'

# id=0 时创建，有 id 时更新
```

### 自动获取网站 Favicon

```bash
curl -s -X POST "$SUN_PANEL_URL/api/panel/itemIcon/getSiteFavicon" \
  -H "Content-Type: application/json" \
  -H "token: $TOKEN" \
  -d '{"url":"https://github.com"}'

# 返回：{"code":0,"data":{"iconUrl":"/uploads/xxx.png"}}
# 使用此路径作为 itemType=2 的 src
```

## 图标类型说明

| itemType | 说明 | 必填字段 |
|----------|------|----------|
| 1 | 文字图标 | `text`（显示的文字） |
| 2 | 图片图标 | `src`（图片路径，可从 favicon API 获取） |
| 3 | Iconify图标 | `text`（图标ID，如 `mdi:github`） |

## openMethod 说明

| 值 | 说明 |
|----|------|
| 1 | 当前页面打开 |
| 2 | 新窗口打开 |
| 3 | 小窗打开（iframe） |

## 图标推荐表

### 常用网站图标

| 网站 | 推荐 Iconify 图标 |
|------|------------------|
| github.com | `mdi:github` |
| google.com | `mdi:google` |
| youtube.com | `mdi:youtube` |
| twitter.com / x.com | `mdi:twitter` |
| facebook.com | `mdi:facebook` |
| instagram.com | `mdi:instagram` |
| reddit.com | `mdi:reddit` |
| linkedin.com | `mdi:linkedin` |
| stackoverflow.com | `mdi:stack-overflow` |
| notion.so | `mdi:notion` |
| figma.com | `mdi:figma` |
| slack.com | `mdi:slack` |
| discord.com | `mdi:discord` |
| spotify.com | `mdi:spotify` |
| twitch.tv | `mdi:twitch` |
| pinterest.com | `mdi:pinterest` |
| medium.com | `mdi:medium` |
| dribbble.com | `mdi:dribbble` |
| behance.net | `mdi:behance` |
| trello.com | `mdi:trello` |
| jira.atlassian.com | `mdi:jira` |
| bitbucket.org | `mdi:bitbucket` |
| gitlab.com | `mdi:gitlab` |
| docker.com | `mdi:docker` |
| kubernetes.io | `mdi:kubernetes` |
| aws.amazon.com | `mdi:aws` |
| azure.microsoft.com | `mdi:azure` |
| cloud.google.com | `mdi:google-cloud` |
| digitalocean.com | `mdi:digital-ocean` |
| vercel.com | `mdi:vercel` |
| netlify.com | `mdi:netlify` |
| heroku.com | `mdi:heroku` |

### AI 相关网站

| 网站 | 推荐 Iconify 图标 |
|------|------------------|
| chat.openai.com | `mdi:chat` 或 `mdi:robot` |
| claude.ai | `mdi:robot-outline` |
| gemini.google.com | `mdi:sparkles` |
| copilot.microsoft.com | `mdi:robot-happy` |
| huggingface.co | `mdi:face-man-hug` |
| replicate.com | `mdi:content-copy` |
| perplexity.ai | `mdi:magnify` |
| midjourney.com | `mdi:palette` |
| stability.ai | `mdi:creation` |
| anthropic.com | `mdi:brain` |
| openai.com | `mdi:robot` |

### 开发工具

| 类型 | 推荐 Iconify 图标 |
|------|------------------|
| Git | `mdi:git` |
| VS Code | `mdi:visual-studio-code` |
| JetBrains | `mdi:intellij` |
| Terminal/SSH | `mdi:console` |
| Database | `mdi:database` |
| API | `mdi:api` |
| Docker | `mdi:docker` |
| Kubernetes | `mdi:kubernetes` |
| Server | `mdi:server` |
| Nginx | `mdi:web` |
| Redis | `mdi:flash` |
| PostgreSQL | `mdi:database-postgre` |
| MySQL | `mdi:database-mysql` |
| MongoDB | `mdi:leaf` |

### 通用图标（按用途）

| 用途 | 推荐 Iconify 图标 |
|------|------------------|
| 文档/笔记 | `mdi:file-document`, `mdi:notebook`, `mdi:book-open` |
| 搜索 | `mdi:magnify`, `mdi:search-web` |
| 邮件 | `mdi:email`, `mdi:mail` |
| 云存储 | `mdi:cloud`, `mdi:folder-cloud` |
| 音乐 | `mdi:music`, `mdi:playlist-music` |
| 视频 | `mdi:video`, `mdi:play-circle` |
| 图片 | `mdi:image`, `mdi:camera` |
| 下载 | `mdi:download`, `mdi:cloud-download` |
| 设置 | `mdi:cog`, `mdi:settings` |
| 监控 | `mdi:monitor`, `mdi:chart-line` |
| 安全 | `mdi:shield`, `mdi:lock` |
| 日历 | `mdi:calendar` |
| 聊天 | `mdi:chat`, `mdi:message` |
| 书签 | `mdi:bookmark`, `mdi:star` |
| 首页 | `mdi:home`, `mdi:house` |

## 分组推荐表

| 网站类型 | 推荐分组名 | 推荐分组图标 |
|----------|-----------|-------------|
| GitHub, GitLab, Bitbucket | 开发工具 | `mdi:code` |
| ChatGPT, Claude, Gemini | AI工具 | `mdi:robot` |
| YouTube, Netflix, Spotify | 视频娱乐 | `mdi:play-circle` |
| Twitter, Facebook, Discord | 社交媒体 | `mdi:account-group` |
| Google, Bing, DuckDuckGo | 搜索引擎 | `mdi:magnify` |
| Notion, Trello, Jira | 效率工具 | `mdi:clipboard-check` |
| Gmail, Outlook, ProtonMail | 邮件服务 | `mdi:email` |
| AWS, Azure, GCP | 云服务 | `mdi:cloud` |
| Plex, Jellyfin, Emby | 媒体服务器 | `mdi:server-network` |
| Grafana, Prometheus | 监控工具 | `mdi:chart-areaspline` |
| Portainer, Dockge | 容器管理 | `mdi:docker` |
| Nextcloud, Syncthing | 文件同步 | `mdi:folder-sync` |

## 操作流程示例

### AI Agent 标准工作流程

```bash
# Step 1: 检查配置文件
CONFIG_FILE="$HOME/.openclaw/skills/sun-panel/config.json"

if [ ! -f "$CONFIG_FILE" ]; then
    # 引导用户创建配置
    echo "首次使用 Sun-Panel 技能"
    echo "请提供 Sun-Panel 的配置信息："
    echo "- URL: Sun-Panel 服务地址"
    echo "- Username: 登录账号"
    echo "- Password: 登录密码"
    # 等待用户提供信息后，创建配置文件
    exit 0
fi

# Step 2: 读取配置
SUN_PANEL_URL=$(jq -r '.url' "$CONFIG_FILE")
SUN_PANEL_USERNAME=$(jq -r '.username' "$CONFIG_FILE")
SUN_PANEL_PASSWORD=$(jq -r '.password' "$CONFIG_FILE")

# Step 3: 登录获取 Token
RESPONSE=$(curl -s -X POST "$SUN_PANEL_URL/api/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$SUN_PANEL_USERNAME\",\"password\":\"$SUN_PANEL_PASSWORD\"}")

if ! echo "$RESPONSE" | jq -e '.code == 0' > /dev/null; then
    echo "登录失败，请检查配置文件中的账号密码"
    exit 1
fi

TOKEN=$(echo "$RESPONSE" | jq -r '.data.token')

# Step 4: 执行用户请求的操作
# （添加网站、创建分组等）
```

### 添加一批 AI 工具网站

```bash
# 1. 检查是否存在 "AI工具" 分组
GROUPS=$(curl -s -X POST "$SUN_PANEL_URL/api/panel/itemIconGroup/getList" \
  -H "token: $TOKEN")
AI_GROUP_ID=$(echo "$GROUPS" | jq -r '.data.list[] | select(.title=="AI工具") | .id')

# 2. 如果不存在，创建分组
if [ -z "$AI_GROUP_ID" ] || [ "$AI_GROUP_ID" == "null" ]; then
  curl -s -X POST "$SUN_PANEL_URL/api/panel/itemIconGroup/edit" \
    -H "Content-Type: application/json" \
    -H "token: $TOKEN" \
    -d '{"title":"AI工具","icon":"mdi:robot"}'
  GROUPS=$(curl -s -X POST "$SUN_PANEL_URL/api/panel/itemIconGroup/getList" -H "token: $TOKEN")
  AI_GROUP_ID=$(echo "$GROUPS" | jq -r '.data.list[] | select(.title=="AI工具") | .id')
fi

# 3. 批量添加图标
curl -X POST "$SUN_PANEL_URL/api/panel/itemIcon/addMultiple" \
  -H "Content-Type: application/json" \
  -H "token: $TOKEN" \
  -d "[
    {
      \"title\": \"ChatGPT\",
      \"url\": \"https://chat.openai.com\",
      \"description\": \"OpenAI ChatGPT\",
      \"icon\": {\"itemType\": 3, \"text\": \"mdi:chat\"},
      \"openMethod\": 2,
      \"itemIconGroupId\": $AI_GROUP_ID
    },
    {
      \"title\": \"Claude\",
      \"url\": \"https://claude.ai\",
      \"description\": \"Anthropic Claude AI\",
      \"icon\": {\"itemType\": 3, \"text\": \"mdi:robot-outline\"},
      \"openMethod\": 2,
      \"itemIconGroupId\": $AI_GROUP_ID
    },
    {
      \"title\": \"Gemini\",
      \"url\": \"https://gemini.google.com\",
      \"description\": \"Google Gemini AI\",
      \"icon\": {\"itemType\": 3, \"text\": \"mdi:sparkles\"},
      \"openMethod\": 2,
      \"itemIconGroupId\": $AI_GROUP_ID
    }
  ]"
```

### 添加单个网站（智能推荐图标）

当用户说"帮我添加 xxx 网站"时：

1. 根据网站 URL 或名称，从推荐表选择图标
2. 根据网站类型，推荐或创建分组
3. 调用 API 添加

**示例：用户说"添加 bilibili"**

```bash
# bilibili 不在预设表中，但属于视频娱乐类
# 推荐: icon=mdi:video, group=视频娱乐

# 1. 获取/创建分组
# 2. 添加图标
curl -X POST "$SUN_PANEL_URL/api/panel/itemIcon/edit" \
  -H "Content-Type: application/json" \
  -H "token: $TOKEN" \
  -d '{
    "title": "Bilibili",
    "url": "https://www.bilibili.com",
    "description": "哔哩哔哩视频网站",
    "icon": {"itemType": 3, "text": "mdi:video"},
    "openMethod": 2,
    "itemIconGroupId": 3
  }'
```

### 使用自动获取 Favicon

```bash
# 获取网站 favicon
ICON_RESP=$(curl -s -X POST "$SUN_PANEL_URL/api/panel/itemIcon/getSiteFavicon" \
  -H "Content-Type: application/json" \
  -H "token: $TOKEN" \
  -d '{"url":"https://example.com"}')

ICON_URL=$(echo $ICON_RESP | jq -r '.data.iconUrl')

# 使用获取到的 favicon 作为图标
curl -X POST "$SUN_PANEL_URL/api/panel/itemIcon/edit" \
  -H "Content-Type: application/json" \
  -H "token: $TOKEN" \
  -d '{
    "title": "Example",
    "url": "https://example.com",
    "icon": {"itemType": 2, "src": "'$ICON_URL'"},
    "openMethod": 2,
    "itemIconGroupId": 1
  }'
```

## Iconify 图标搜索

如果推荐表中没有对应图标，可以搜索：

- **图标库地址**: https://icon-sets.iconify.design/
- **常用图标集**: `mdi` (Material Design Icons), `fa` (Font Awesome), `carbon`, `tabler`

搜索格式：
```
# Material Design Icons 示例
mdi:github    → GitHub
mdi:home      → 首页图标
mdi:cog       → 设置图标

# Font Awesome 示例
fa:github
fa:home
```

## 常见问题

### 配置文件不存在
AI Agent 引导用户创建配置文件，收集 URL、账号、密码信息。

### Token 过期
重新登录获取新 token。

### 分组不存在
先调用 `itemIconGroup/edit` 创建分组，再添加图标。

### 图标不显示
- itemType=3 时确保 icon ID 正确（带前缀如 `mdi:xxx`）
- itemType=2 时确保 src 路径正确
- 可调用 `getSiteFavicon` 自动获取网站图标

### 登录失败
检查配置文件中的账号密码是否正确，提示用户更新配置。