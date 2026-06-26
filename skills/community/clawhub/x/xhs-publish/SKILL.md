---
name: xhs-publish
description: 小红书一键发布 — AI 全流程搞定：自动生成标题 → 撰写正文 → 封面/知识卡片/视频（三种形式） → 一键发布。3 分钟从创意到上线，支持多模型自由切换。触发词：发小红书、发布笔记、小红书发布、发笔记、小红书笔记、写小红书、写笔记。
metadata: {"openclaw": {"emoji": "📕", "requires": {"bins": ["convert"], "anyBins": ["curl"]}}}
---

# 📕 小红书发布助手

**核心能力**：文案创作（标题+正文+封面图）和笔记发布（图文/视频）

**支持三种笔记格式**：
1. **📷 纯封面图** — AI 生成单张封面图 + 正文（最常用）
2. **🖼️ 知识卡片** — 生成精美知识卡片 + 正文（适合教程/长文）
3. **🎬 视频笔记** — AI 生成视频 + 添加字幕 + 正文（适合动态展示）

---

## 一、完整发布流程

```
                       用户请求写笔记/发小红书
                                   │
                                   ▼
                      用户是否提供了主题？
                                   │
                      ┌────────────┴────────────┐
                      │                         │
                    没有                       有
                      │                         │
                      ▼                         │
                 ① 询问主题                     │
                      │                         │
                      └────────────┬────────────┘
                                   │
                                   ▼
                  ② 笔记类型选择
                                   │
                                   ▼
                    生成标题 + 正文（通用）
                                   │
                ┌──────────────────┼──────────────────┐
                │                  │                  │
                ▼                  ▼                  ▼
           📷纯封面图          🖼️知识卡片         🎬视频笔记
                │                  │                  │
                ▼                  ▼                  ▼
           生成封面          生成知识卡片      ③ 视频流程
                │                  │                  │
                └──────────────────┼──────────────────┘
                                   │
                                   ▼
                          ④ 内容确认
                                   │
                          ┌───────┴───────┐
                          │               │
                       满意            不满意
                          │               │
                          ▼               ▼
                      ⑤ 发布流程     重新生成/调整
                          │
                ┌─────────┼─────────┐
                │                   │
                ▼                   ▼
            发布成功           发布失败
                │                   │
                ▼                   ▼
             完成 ✅           ⑥ 登录流程

（注：🎬 视频笔记不需要封面图，小红书会自动从视频中截取）
```

**关键确认节点（AI 执行重点）：**
- **① 询问主题** — 如果用户未提供主题
- **② 笔记类型** — 纯封面图/知识卡片/视频笔记
- **③ 视频流程** — 视频笔记专用（内部包含多个步骤）
- **④ 内容确认** — 最终确认所有内容（标题+正文+封面/视频）
- **⑤ 发布流程** — 调用小红书 MCP 发布
- **⑥ 登录流程** — 发布失败时扫码登录

---

## 🔴 内容禁忌（重要）

**⚠️ 笔记内容禁止出现以下关键词！**

**禁止关键词：**
- ❌ "小红书"
- ❌ "xhs"、"XHS"
- ❌ "红书"
- ❌ xhs 前缀的 skill 名称（如 xhs-publish、xhs-auto-reply、xhs-post-monitor 等）

**原因：**
- 小红书平台禁止自动发布
- 笔记中出现这些关键词可能被判定为违规
- 避免触发平台风控

**替代方案：**
- "小红书" → "这里"、"这个平台"、"某社交平台"
- 如需举例 skill，使用其他热门 skill（如 weather、github、obsidian）

**检查时机：**
- 生成正文后，自动检查是否包含禁忌词
- 如有，自动替换后再展示给用户

---

## 🔴 飞书图片发送规则（最重要）

**⚠️ 永远不要发路径！永远要发图片！**

**正确方式**：
```javascript
// 1. 先把文件复制到 inbound 目录
cp /path/to/file.jpg /root/.openclaw/media/inbound/

// 2. 再用 message 发送
message({
  action: "send",
  channel: "feishu",
  media: "/root/.openclaw/media/inbound/file.jpg",
  filename: "文件名.jpg"
})
```

**✅ 永远用 `media` 参数发送图片，✅ 永远从 `/root/.openclaw/media/inbound/` 目录发送**

**❌ 所有其他方式都不行**：
- ❌ 直接发路径字符串 → 用户看到路径
- ❌ 用 `message` 参数发路径 → 用户看到路径
- ❌ Base64 编码 → 用户收不到
- ❌ file_token → 用户收不到

---

## 📝 文案创作

### 2.1 第一步：确认主题（如需要）

**⚠️ 智能判断是否需要询问主题！**

**判断规则**：

1. **用户已提供主题**（如「帮我发个小红书，关于 OpenClaw」）→ 直接进入第二步
2. **用户未提供主题**（如「帮我发个小红书」）→ 询问主题

**询问主题的提示**：

> 请选择主题类型：
> 1. **📱 产品/工具分享** — 分享你使用的某个产品或工具
> 2. **📖 教程/攻略** — 教别人如何做某件事
> 3. **🌅 日常分享** — 分享日常生活、旅行、美食等
> 4. **🎁 好物推荐** — 推荐你觉得好用的东西

---

### 2.2 第二步：确认笔记类型和封面方式

**⚠️ 用户确认主题后，询问笔记类型和封面方式！**

> 请选择笔记类型：
> 1. **📷 纯封面图** — AI 生成单张封面图 + 正文（最常用，适合分享/种草）
> 2. **🖼️ 知识卡片** — 生成精美知识卡片 + 正文（适合教程/长文）
> 3. **🎬 视频笔记** — AI 生成视频 + 正文（适合动态展示/教程）

**用户选择纯封面图后，询问封面方式：**

> 请选择封面生成方式：
> 1. **🎨 AI 模型生图** — 使用 AI 模型生成封面图（需要 API Key）
> 2. **📝 MD2Card 一句话封面** — 输入一句话，自动生成精美封面（支持关键字标注）（推荐）

**用户选择知识卡片或视频笔记后，直接进入生成流程。**

---

### 2.3 第三步：生成内容

**⚠️ 不同笔记类型的生成流程不同！**

#### 📷 纯封面图 / 🖼️ 知识卡片

**并行生成，一次性确认**：
1. 生成 5 个标题
2. 生成正文（600-800字）
3. 生成知识卡片内容（仅知识卡片，1500-2000字）
4. 生成封面图
5. 生成知识卡片图（仅知识卡片）
6. 一次性发送给用户确认

#### 🎬 视频笔记

**分步确认，避免浪费资源**：
1. **生成标题+正文**（200-300字）→ 用户确认
2. **询问视频风格**（5个选项）→ 用户选择
3. **生成分镜脚本**（根据正文拆分3-6个镜头）→ 用户确认
4. **生成视频片段**（每个镜头生成视频）
5. **音画同步校验**（配音时长 vs 视频时长）
6. **发送最终确认**（标题+正文+视频预览）

**⚠️ 视频笔记不需要生成封面图！** 小红书会自动从视频中截取。

---

#### 📷 纯封面图 / 🖼️ 知识卡片生成流程

**自动执行流程**（每步完成后发送进度提示）：

1. **生成标题**：自动生成 5 个标题，默认选择第一个
   - 发送进度：`✅ 1/5 标题生成完成`
   
2. **生成正文**：根据主题生成 600-800 字正文
   - 发送进度：`✅ 2/5 正文生成完成`
   
3. **生成知识卡片内容**（仅知识卡片类型）：2000-3000 字
   - 发送进度：`✅ 3/5 知识卡片内容生成完成`
   
4. **生成封面图**：根据类型生成
   - 纯封面图：AI 模型生图
   - 知识卡片：MD2Card API 生成封面
   - 视频笔记：AI 生成视频
   - 发送进度：`✅ 4/5 封面图生成完成`
   
5. **生成知识卡片图**（仅知识卡片类型）：使用 MD2Card MCP
   - 发送进度：`✅ 5/5 知识卡片图生成完成`

**生成完成后，一次性发送给用户确认：**

> 📝 笔记内容已生成！
> 
> **标题**（默认第一个）：
> 1. 标题1
> 2. 标题2
> 3. 标题3
> 4. 标题4
> 5. 标题5
> 
> **正文**：
> [正文内容]
> 
> **封面**：[图片]
> 
> 是否满意？
> 1. 满意，直接发布
> 2. 换个标题
> 3. 重新生成正文
> 4. 重新生成封面
> 5. 全部重新生成

---

### 2.4 标题生成规则

**优先使用当前对话模型**，参考 [references/title-guide.md]({baseDir}/references/title-guide.md) 生成 5 个不同风格的标题。

**核心要求**：

1. 每个标题使用不同风格
2. 20 字以内
3. 含 1-2 个 emoji
4. 禁用平台禁忌词

**5 种标题风格**：

1. **数字悬念型**：【3个方法让你秒懂xxx】
2. **情感共鸣型**：【谁懂啊！这个方法太绝了！】
3. **结果导向型**：【跟着做，7天搞定xxx】
4. **反差对比型**：【从xxx到xxx，我只做了这件事】
5. **价值宣言型**：【2025必学技能，xxx让你更厉害】

---

### 2.5 正文生成规则

**优先使用当前对话模型**，参考 [references/content-guide.md]({baseDir}/references/content-guide.md)。

**字数要求**：

| 笔记类型 | 正文字数 | 知识卡片文字 | 配音文案 | 说明 |
|---------|---------|-------------|---------|------|
| 📷 纯封面图 | 600-800 字 | - | - | 简洁总结 |
| 🖼️ 知识卡片 | 600-800 字 | **2000-3000 字** | - | 正文简洁，知识卡片内容更丰富 |
| 🎬 视频笔记 | 200-300 字 | - | **与正文一致** | 正文即配音文案 |

**知识卡片字数说明**：
- **正文（600-800字）**：发布时显示的正文，简洁总结
- **知识卡片文字（1500-2000字）**：用于生成 MD2Card 知识卡片的内容，比正文更丰富、更详细

**视频笔记字数说明**：
- **正文（200-300字）**：发布时显示的正文，同时也是配音文案的内容
- **配音文案**：与正文内容一致，逐字对应（可微调语气，但核心内容一致）

**格式要求**：

1. 小标题：加合适的图标（如 💡、🔧、📚、🎯 等）
2. 有顺序的内容：加数字图标（如 1️⃣、2️⃣、3️⃣ 或 ①②③）
3. 分段清晰：段落之间用空行分隔

---

## 三、封面生成

### 3.1 AI 模型生图

**适用场景**：需要个性化、创意性强的封面图

**前置条件**：需要配置 AI 生图 API Key（Doubao/Hunyuan）

**自动执行流程**：

1. 生成英文 Prompt：根据文案主题自动生成
2. 调用 AI 生图：优先使用 Doubao（豆包）API
3. 输出封面图：1080x1080 正方形

**Prompt 模板**：

```
cute cartoon illustration style, [场景描述], kawaii anime style, soft pastel [色调] colors, minimal clean background, with Chinese text "[标题]" at top, no watermark, high quality, square format, poster design
```

**生图调用示例**：

```bash
curl -X POST "https://ark.cn-beijing.volces.com/api/v3/images/generations" \
  -H "Authorization: Bearer $DOUBAO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "doubao-seedream-5-0-260128",
    "prompt": "cute cartoon illustration style, ...",
    "size": "2048x2048",
    "n": 1
  }'
```

---

### 3.2 MD2Card 一句话封面

**适用场景**：快速生成精美封面，支持关键字标注

**特点**：
- 纵向小红书风格封面
- 支持关键字高亮标注
- 多种模板可选

**自动执行流程**：

1. **生成封面文案**：根据标题生成一句话描述
2. **调用 MD2Card API**：生成封面图片
3. **下载图片**：保存到本地

**封面文案生成规则**：

- 一句话概括主题（15-30字）
- 可添加副标题（如：3分钟看懂 | 实用技巧 | 效率翻倍）
- 突出核心价值点

**示例**：
```
标题：OpenClaw原理剖析

封面文案：
如何让OpenClaw真的能干活
3分钟看懂 | 实用技巧 | 效率翻倍
```

**⚠️ MD2Card API 调用（推荐）**：

```bash
# 调用 MD2Card API 生成封面
curl -X POST https://md2card.cn/api/generate/cover \
  -H "x-api-key: $MD2CARD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "如何让OpenClaw真的能干活\n3分钟看懂 | 实用技巧 | 效率翻倍",
    "keywords": "OpenClaw",
    "count": 3
  }'

# 响应示例：
{
  "success": true,
  "images": [
    {
      "url": "https://md2card-com.oss-cn-shenzhen.aliyuncs.com/screenshot/xxx.png",
      "fileName": "screenshot/xxx.png",
      "size": 218.88
    }
  ],
  "cost": 2,
  "message": "成功生成 3 张封面图片，消耗 2 积分"
}

# 下载第一张图片
curl -s "图片URL" -o /root/.openclaw/media/inbound/xhs_cover.png
```

**参数说明**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `text` | string | 封面文字（支持换行符 \n） |
| `keywords` | string | 关键词（用于高亮） |
| `count` | number | 生成数量（1-3） |

**返回值说明**：

- `images`：图片数组（最多3张）
- `url`：图片下载链接
- `cost`：消耗积分（通常2分）

---

## 四、知识卡片生成（MD2Card MCP）

**⚠️ 知识卡片需要生成封面 + 知识卡片内容！**

**封面生成位置**：已在「三、封面生成」章节的「3.2 MD2Card 一句话封面」中完成

**本章只负责生成知识卡片内容（MD2Card MCP）**

### 💰 付费说明（重要）

**MD2Card 知识卡片是付费服务！**

| 项目 | 价格 |
|-----|------|
| 封面图 | 约 0.05 元/张 |
| 知识卡片 | 约 **0.1 元/张** |

**充值地址**：https://md2card.cn/zh/login

**积分不足时的处理**：

1. **检测方法**：调用 MD2Card API 时返回 402 错误或"积分不足"提示
2. **处理流程**：
   - 告知用户当前积分已用完
   - 提供充值地址：https://md2card.cn/zh/login
   - 建议用户改用「📷 纯封面图」模式（封面 API 可能还有额度）

**检测积分的 API 调用**：
```bash
# 检测 MD2Card 积分（可选，提前检测）
curl -s https://md2card.cn/api/user/info \
  -H "x-api-key: $MD2CARD_API_KEY"

# 响应示例：
{
  "success": true,
  "data": {
    "balance": 50,  # 剩余积分
    "used": 100     # 已用积分
  }
}

# 如果 balance < 10，建议充值
```

**错误提示模板**：
> ⚠️ **MD2Card 积分不足**
>
> 知识卡片生成需要 MD2Card 积分（约 0.1 元/张）。
>
> 当前账户积分已用完，请充值后继续：
> 👉 充值地址：https://md2card.cn/zh/login
>
> 或者改用「📷 纯封面图」模式发布笔记？

---

**自动执行流程**：

1. **生成封面**：使用 MD2Card API 生成封面图（已在 3.2 章节完成）
2. **转换格式**：将**知识卡片文字**（1500-2000字）转换为 Markdown 格式
3. **生成知识卡片**：使用 MD2Card MCP 生成知识卡片图片
4. **自动拆分**：MCP 会自动将长内容拆分为多张卡片图片
5. **发送确认**：将所有图片发送给用户确认（封面图 + 多张知识卡片图片）

**⚠️ 封面生成位置**：封面已在「三、封面生成」章节生成，这里只生成知识卡片内容！

---

**🔴 重要：知识卡片必须使用 API 方式，并设置自动拆分参数！**

**关键参数**：`splitMode: "autoSplit"`（不是 `"auto"`，不是 `"noSplit"`）

**完整 API 调用示例**：

```bash
source /etc/environment && timeout 120 npx -y md2card-mcp-server@latest << 'EOFMCP'
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"openclaw","version":"1.0.0"}}}
{"jsonrpc":"2.0","method":"notifications/initialized"}
{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"md2card_api","arguments":{
  "markdown": "## 标题\n\n内容...",
  "type": "小红书",
  "theme": "apple-notes",
  "splitMode": "autoSplit"
}}}
EOFMCP
```

**入参 JSON 示例**：

```json
{
  "markdown": "## 🎯 OpenClaw 是什么？\n\nOpenClaw 是一个 AI 助手框架...\n\n---\n\n## 💎 5 大核心玩法\n\n### 1️⃣ 小红书一键发布\n...",
  "type": "小红书",
  "theme": "apple-notes",
  "splitMode": "autoSplit",
  "width": 440,
  "height": 586,
  "mdxMode": false,
  "overHiddenMode": false
}
```

**参数说明**：

| 参数 | 值 | 说明 |
|-----|-----|------|
| `markdown` | 字符串 | Markdown 格式的知识卡片内容（1500-2000字） |
| `type` | `"小红书"` | 卡片类型，使用小红书尺寸（440x586） |
| `theme` | `"apple-notes"` | 主题风格（推荐苹果备忘录） |
| **`splitMode`** | **`"autoSplit"`** | **🔴 关键！自动拆分参数，必须是这个值！** |
| `width` | 440 | 卡片宽度（小红书默认） |
| `height` | 586 | 卡片高度（小红书默认） |

**返回结果示例（多张图片）**：

```json
{
  "result": {
    "content": [{
      "type": "text",
      "text": "**下载图片**\n[screenshot/xxx_1.png](https://...)\n图片大小：120 KB\n[screenshot/xxx_2.png](https://...)\n图片大小：95 KB\n[screenshot/xxx_3.png](https://...)\n图片大小：85 KB\n...\n\n**在线编辑**\n[点击在线编辑](https://...)\n\n- 本次消耗积分：10"
    }]
  }
}
```

**⚠️ 消耗积分**：每张卡片消耗 1 积分（10 张卡片 = 10 积分）

**⚠️ 图片尺寸**：自动拆分后的卡片尺寸为 **880 x 1172**（小红书标准尺寸）

**⚠️ 用户确认时必须展示所有拆分后的图片！**

```bash
# 发送封面图
openclaw message send --channel feishu --media /root/.openclaw/media/inbound/md2card_cover.png --message "📷 封面预览"

# 发送知识卡片
openclaw message send --channel feishu --media /root/.openclaw/media/inbound/md2card_content.png --message "🖼️ 知识卡片预览"
```

### 4.1 生成知识卡片内容（MD2Card MCP）

**⚠️ 优先使用 MD2Card MCP 生成知识卡片！**

**前置条件：**
1. 安装 MCP 服务：`npm install -g md2card-mcp-server@latest`
2. 申请 API 密钥：https://md2card.cn/zh/login
3. 配置环境变量：`export MD2CARD_API_KEY="您的密钥"`

**检测 MCP 是否已安装：**
```bash
# 检查环境变量
echo $MD2CARD_API_KEY && echo "✅ MCP 已配置" || echo "❌ MCP 未配置"
```

**如果 MCP 已配置，使用 MCP 生成：**

```bash
# 启动 MCP 服务（后台运行）
MD2CARD_API_KEY="您的密钥" npx -y md2card-mcp-server@latest &
```

**MCP 调用示例（JSON-RPC 2.0 批量请求）：**

```bash
export MD2CARD_API_KEY="您的密钥"

# 调用 MCP 生成小红书知识卡片
cat << 'EOF' | timeout 30 npx -y md2card-mcp-server@latest
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"openclaw","version":"1.0.0"}}}
{"jsonrpc":"2.0","method":"notifications/initialized"}
{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"md2card_api","arguments":{"markdown":"## 标题\n\n内容","type":"小红书","theme":"apple-notes"}}}
EOF
```

**MCP 参数说明：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `markdown` | string | Markdown 格式内容 |
| `type` | string | 卡片类型：小红书、正方形、手机海报、A4纸打印 |
| `theme` | string | 主题风格（见下方列表） |
| `themeMode` | string | 主题模式（可选） |

**可用主题列表（theme）：**
- `apple-notes` - 苹果备忘录（推荐）
- `xiaohongshu` - 紫色小红书
- `darktech` - 暗黑科技
- `glassmorphism` - 玻璃拟态
- `minimal` - 简约高级灰
- `dreamy` - 梦幻渐变
- `typewriter` - 复古打字机
- 更多主题：见 MCP 文档

**返回结果格式：**

```json
{
  "result": {
    "content": [{
      "type": "text",
      "text": "**下载图片**\n[图片链接](https://...)\n图片大小：XX KB\n\n**在线编辑**\n[点击在线编辑](https://...)"
    }]
  }
}
```

**下载所有拆分后的图片**：

```bash
# MCP 返回结果示例（多张图片）：
{
  "result": {
    "content": [{
      "type": "text",
      "text": "**下载图片**\n[图片1](https://...)\n[图片2](https://...)\n[图片3](https://...)\n\n**在线编辑**\n[点击在线编辑](https://...)"
    }]
  }
}

# 提取所有图片 URL 并下载
# 使用 grep 提取所有图片链接
urls=$(echo "$result" | grep -o 'https://[^)]*\.png')

# 创建保存目录
mkdir -p /root/.openclaw/media/inbound/xhs_cards

# 下载所有图片
i=1
for url in $urls; do
  curl -s "$url" -o "/root/.openclaw/media/inbound/xhs_cards/card_$i.png"
  echo "✅ 已下载第 $i 张卡片"
  i=$((i+1))
done

# 发送所有图片给用户确认
for file in /root/.openclaw/media/inbound/xhs_cards/card_*.png; do
  openclaw message send --channel feishu --media "$file" --message "🖼️ 知识卡片"
done
```

**⚠️ 注意**：每张卡片消耗 1 积分，下载前确认积分充足！

**如果 MCP 未配置，提示用户安装（必装）：**

> ⚠️ **MD2Card MCP 未安装！**
>
> MD2Card MCP 是知识卡片的**必装组件**，请先安装：
>
> **安装步骤：**
> 1. 访问 https://md2card.cn/zh/login 申请 API 密钥
> 2. 复制 API 密钥
> 3. 发送给我，格式：`MD2CARD_API_KEY=sk-xxx`
> 4. 我会自动配置环境变量
>
> 配置完成后，即可生成知识卡片。

---

## 五、视频生成

**⚠️ 视频笔记采用多镜头方式，需要用户多次确认！**

**⚠️ 视频笔记不需要生成封面图！** 小红书会自动从视频中截取。

---

### 5.1 视频风格选择

**⚠️ 用户确认内容后，询问视频风格！**

**5 个视频风格选项**：

| 序号 | 风格 | 描述 | 适合场景 |
|-----|------|------|---------|
| 1 | 🎨 **卡通可爱** | 卡通角色，明亮色彩，轻松有趣 | 日常分享、趣味内容 |
| 2 | 🔬 **科技简约** | 简洁线条，科技蓝，专业感 | 技术讲解、工具介绍 |
| 3 | 🌙 **暗黑科技** | 深色背景，霓虹光效，未来感 | 高端产品、极客内容 |
| 4 | 🌈 **梦幻渐变** | 柔和渐变，温暖色调，治愈系 | 情感分享、生活记录 |
| 5 | 📰 **商务专业** | 简洁大气，商务配色，正式感 | 职场干货、商业内容 |

**询问提示**：
> 🎬 **请选择视频风格**：
> 
> 1. 🎨 **卡通可爱** — 卡通角色，明亮色彩，轻松有趣
> 2. 🔬 **科技简约** — 简洁线条，科技蓝，专业感（推荐）
> 3. 🌙 **暗黑科技** — 深色背景，霓虹光效，未来感
> 4. 🌈 **梦幻渐变** — 柔和渐变，温暖色调，治愈系
> 5. 📰 **商务专业** — 简洁大气，商务配色，正式感
> 
> 请回复数字 1-5，或直接说风格名称。

**默认风格**：如果用户跳过或不确定，默认使用「科技简约」

---

### 5.2 第二步：生成分镜脚本和配音文案

**⚠️ 用户选择风格后，生成分镜脚本 + 配音文案！**

**🔴 文案-语音-视频三同步规则（最重要！）**

**三要素必须完全一致**：
1. **文案**：正文内容（200-300字）
2. **语音**：配音文案（逐字对应文案）
3. **视频**：画面内容（视觉呈现文案描述的场景）

**同步要求**：
- 文案说"让AI帮你整理文件，它说无法访问" → 配音必须读这句话 → 视频必须展示这个场景
- **禁止**：文案说A、配音说B、视频展示C
- **强制**：三者内容必须一一对应

**分镜规则**：

1. **文案拆分**：将正文内容按段落/句子拆分为 3-6 个镜头
2. **配音生成**：每个镜头的配音文案 = 对应的正文片段（可微调语气，但核心内容一致）
3. **视频生成**：视频 Prompt 必须准确描述配音文案的场景
4. 每个镜头 3-6 秒
5. 总时长 15-35 秒

**分镜脚本模板**：

```json
{
  "style": "科技简约",
  "total_duration": 30,
  "shots": [
    {
      "id": 1,
      "duration": 5,
      "narration": "你有没有遇到过，让AI帮你整理文件，它说无法访问？",
      "prompt": "User typing on phone asking AI chatbot, error message appears, frustrated expression, clean tech UI, blue and white colors, 4K quality"
    }
  ]
}
```

**Prompt 生成规则（根据风格调整）**：

| 风格 | Prompt 关键词 |
|-----|-------------|
| 卡通可爱 | `cartoon style, cute characters, bright colors, kawaii, playful` |
| 科技简约 | `clean minimal design, tech blue, simple lines, professional, modern UI` |
| 暗黑科技 | `dark background, neon glow, cyberpunk, futuristic, holographic` |
| 梦幻渐变 | `soft gradient, pastel colors, dreamy, warm tones, ethereal` |
| 商务专业 | `clean corporate design, professional colors, business style, formal` |

---

### 5.3 第三步：发送分镜确认

**⚠️ 生成分镜后，必须发送给用户确认！**

**确认提示**：
> 🎬 **分镜脚本已生成！**
> 
> **视频风格**：[用户选择的风格]
> **总时长**：约 XX 秒
> 
> **镜头 1**（0-5秒）
> - 配音："[配音文案]"
> - 画面：[画面描述]
> 
> **镜头 2**（5-10秒）
> - 配音："[配音文案]"
> - 画面：[画面描述]
> 
> ...（所有镜头）
> 
> ---
> 
> 分镜满意吗？
> 1. ✅ 满意，开始生成视频
> 2. 调整配音文案
> 3. 调整画面风格
> 4. 重新生成分镜

---

### 5.4 第四步：生成视频

**⚠️ 用户确认分镜后，才开始生成视频！**

**生成流程**：

1. **生成配音**：使用 Edge TTS 生成完整配音
2. **生成视频片段**：为每个镜头生成视频（带进度反馈）
3. **合并视频**：将所有片段合并
4. **添加配音和字幕**：合成最终视频

**进度反馈**：
> 🎬 视频生成中...
> 
> ✅ 1/5 配音生成完成
> ✅ 2/5 视频片段 1/4 完成
> ✅ 3/5 视频片段 2/4 完成
> ...

---

### 5.5 视频生成 API

**豆包 Seedance API**（当前使用）：

```bash
# 提交视频生成任务
curl -X POST "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks" \
  -H "Authorization: Bearer $DOUBAO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "doubao-seedance-1-5-pro-251215",
    "content": [{"type": "text", "text": "[Prompt]"}]
  }'

# 查询任务状态
curl -s "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/[task_id]" \
  -H "Authorization: Bearer $DOUBAO_API_KEY"
```

**环境变量**（存储在 /etc/environment）：
```bash
export DOUBAO_API_KEY="919ec537-6d4d-43c4-a5ce-a90a17673bbb"
```

**付费说明**：约 0.1 元/5秒视频

**充值入口**：https://console.volcengine.com/finance/recharge

---

### 5.6 配音生成（Edge TTS）

**使用 Edge TTS 生成中文配音**：

```bash
# 生成配音
edge-tts --text "配音文案内容" --voice zh-CN-XiaoxiaoNeural --write-media output.mp3
```

**可用中文语音**：
- `zh-CN-XiaoxiaoNeural` — 温柔女声（推荐）
- `zh-CN-YunxiNeural` — 阳光男声
- `zh-CN-YunyangNeural` — 专业男声

---

### 5.7 视频合并和字幕

**合并视频片段**：

```bash
# 创建合并列表
cat > concat_list.txt << 'EOF'
file 'shot_1.mp4'
file 'shot_2.mp4'
file 'shot_3.mp4'
EOF

# 合并
ffmpeg -f concat -safe 0 -i concat_list.txt -c copy merged.mp4
```

**添加配音**：

```bash
ffmpeg -i merged.mp4 -i narration.mp3 \
  -c:v copy -c:a aac \
  -map 0:v:0 -map 1:a:0 \
  final_with_audio.mp4
```

**添加字幕**：

```bash
ffmpeg -i final_with_audio.mp4 \
  -vf "subtitles=subtitle.srt:force_style='FontName=Noto Sans CJK SC,Fontsize=24,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,Outline=2'" \
  -c:a copy final_video.mp4
```

---

### 5.8 音画同步校验（重要！）

**⚠️ 视频生成完成后，必须进行音画同步校验！通过后才能发送给用户确认！**

**校验步骤**：

```bash
# 1. 获取配音时长
audio_duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 narration.mp3)

# 2. 获取视频时长
video_duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 merged_video.mp4)

# 3. 计算差值
diff=$(echo "$audio_duration - $video_duration" | bc)
abs_diff=${diff#-}

# 4. 判断是否通过
if (( $(echo "$abs_diff < 1" | bc -l) )); then
  echo "✅ 音画同步校验通过"
else
  echo "❌ 音画不同步，差值: ${abs_diff}秒"
fi
```

**调整方案**：

```bash
# 如果配音更长 → 视频放慢
speed_ratio=$(echo "scale=2; $video_duration / $audio_duration" | bc)
setpts_value=$(echo "scale=2; 1 / $speed_ratio" | bc)
ffmpeg -i video.mp4 -filter:v "setpts=${setpts_value}*PTS" -an slowed_video.mp4

# 如果视频更长 → 视频加速
speed_ratio=$(echo "scale=2; $video_duration / $audio_duration" | bc)
ffmpeg -i video.mp4 -filter:v "setpts=${speed_ratio}*PTS" -an faster_video.mp4
```

**示例**：
- 视频 25 秒，配音 32 秒
- 速度比 = 25/32 ≈ 0.78
- setpts = 1/0.78 ≈ 1.28
- 命令：`ffmpeg -i video.mp4 -filter:v "setpts=1.28*PTS" -an output.mp4`

**⚠️ 校验不通过时**：
1. 自动调整视频速度
2. 重新校验
3. 如果仍不通过，提示用户并询问是否继续

---
  ]
}
```

---

## 六、发布流程

**⚠️ 用户确认内容后，立即发布，不需要询问！**

### 6.1 立即发布

#### 前置检查

**⚠️ 小红书 MCP 是必装项，无法发布笔记！**

执行环境检查：

```bash
bash {baseDir}/check_env.sh
```

**返回码说明**：

| 返回码 | 状态 | 处理方式 |
|-------|------|---------|
| `0` | ✅ 正常已登录 | 继续发布 |
| `1` | ❌ 未安装 MCP | 告知用户必须安装（见「八、安装 MCP 服务」）|
| `2` | ⚠️ 未登录 | 进入「七、登录流程」|

**如果返回码为 1（未安装），提示用户：**

> ⚠️ **小红书 MCP 未安装，无法发布笔记！**
>
> 小红书 MCP 是发布笔记的**必装组件**，请先安装：
>
> **安装步骤：**
> 1. 安装依赖：`sudo apt install -y xvfb imagemagick zbar-tools xdotool fonts-noto-cjk`
> 2. 下载 MCP：`cd ~/xiaohongshu-mcp && wget https://github.com/xpzouying/xiaohongshu-mcp/releases/latest/download/xiaohongshu-mcp-linux-amd64.tar.gz`
> 3. 解压并启动：`tar xzf xiaohongshu-mcp-linux-amd64.tar.gz && DISPLAY=:99 nohup ./xiaohongshu-mcp-linux-amd64 -port :18060 > mcp.log 2>&1 &`
>
> 详细安装步骤见「八、安装 MCP 服务」

#### 发布纯封面图笔记

```python
{
    "name": "publish_content",
    "arguments": {
        "title": "标题",
        "content": "正文",
        "images": ["/path/to/cover.jpg"],
        "tags": ["标签1", "标签2"]
    }
}
```

#### 发布知识卡片笔记

```python
{
    "name": "publish_content",
    "arguments": {
        "title": "标题",
        "content": "正文",
        "images": ["/path/to/cover.jpg", "/path/to/content.jpg"],
        "tags": ["标签1", "标签2"]
    }
}
```

#### 发布视频笔记

```python
{
    "name": "publish_with_video",
    "arguments": {
        "title": "标题",
        "content": "正文",
        "video": "/path/to/video.mp4"
    }
}
```

#### 超时处理

**MCP 发布超时设置为 180 秒（3 分钟）**

**发布失败自动重试机制**：

1. 第一次发布：调用 MCP 发布笔记
2. 如果失败：自动重试 1 次
3. 如果仍然失败：自动获取登录二维码

---

## 七、登录流程

### 7.1 扫码登录

**⚠️ 小红书需要扫码两次**：
1. 第一次：验证账号
2. 第二次：确认登录设备

**获取二维码**：

```bash
MCP_URL="http://localhost:18060/mcp"

SESSION_ID=$(curl -s -D /tmp/headers -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{}},"id":1}' \
  > /dev/null && grep -i 'Mcp-Session-Id' /tmp/headers | awk '{print $2}')

curl -s --max-time 30 -X POST "$MCP_URL" -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"get_login_qrcode","arguments":{}},"id":2}'
```

---

### 7.2 Cookie 登录

当扫码登录失败时使用。

**获取 Cookie**：
1. 打开浏览器，访问 https://www.xiaohongshu.com 并登录
2. 按 F12 → Application → Cookies
3. 复制 Cookie 值：`a1`、`web_session`、`websectiga`、`id_token`

**更新 Cookie 文件**：
```bash
nano ~/xiaohongshu-mcp/cookies.json
```

**重启 MCP 服务**：
```bash
pkill -f xiaohongshu-mcp && sleep 3
cd ~/xiaohongshu-mcp && export DISPLAY=:99
nohup ./xiaohongshu-mcp-linux-amd64 -port :18060 > mcp.log 2>&1 &
```

---

## 八、安装 MCP 服务

### 8.1 安装依赖

```bash
sudo apt update && sudo apt install -y xvfb imagemagick zbar-tools xdotool fonts-noto-cjk
```

### 8.2 启动虚拟显示

```bash
Xvfb :99 -screen 0 1920x1080x24 &
```

### 8.3 下载并启动 MCP

```bash
mkdir -p ~/xiaohongshu-mcp && cd ~/xiaohongshu-mcp
wget https://github.com/xpzouying/xiaohongshu-mcp/releases/latest/download/xiaohongshu-mcp-linux-amd64.tar.gz
tar xzf xiaohongshu-mcp-linux-amd64.tar.gz
chmod +x xiaohongshu-*

export ROD_DEFAULT_TIMEOUT=10m
DISPLAY=:99 nohup ./xiaohongshu-mcp-linux-amd64 -port :18060 > mcp.log 2>&1 &
```

---

## 🔴 强制规则

### ✅ 正确做法

图片/视频必须使用服务器本地绝对路径：

```python
"images": ["{baseDir}/media/inbound/cover.jpg"]
"video": "{baseDir}/media/inbound/video.mp4"
```

### ❌ 错误做法

不要用 base64 编码（会导致上传超时）：

```python
"images": ["data:image/jpeg;base64,..."]
```

**⚠️ 永远用文件路径，永远不要用 base64！**

---

## 九、故障排查

### 9.1 诊断命令

```bash
pgrep -f xiaohongshu-mcp           # MCP 是否运行
pgrep -x Xvfb                      # Xvfb 是否运行
tail -20 ~/xiaohongshu-mcp/mcp.log # 查看日志
lsof -i :18060                     # 检查端口
```

### 9.2 常见错误

**1. 发布失败（已重试）**
- 原因：登录状态失效
- 解决：自动获取二维码，扫码重新登录

**2. `context deadline exceeded`**
- 原因：rod 库超时
- 解决：设置 `ROD_DEFAULT_TIMEOUT=10m`

**3. 图片上传超时**
- 原因：使用 base64 编码
- 解决：改用文件路径

---

## 十、参考文档

- 标题创作指南：[references/title-guide.md]({baseDir}/references/title-guide.md)
- 正文创作指南：[references/content-guide.md]({baseDir}/references/content-guide.md)
- 封面图生成指南：[references/cover-guide.md]({baseDir}/references/cover-guide.md)
