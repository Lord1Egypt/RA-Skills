# wechat-oa

**微信公众号草稿箱管理工具** · 基于官方微信 API，无需第三方依赖

A WeChat Official Account draft management toolkit built on the official WeChat API. No third-party dependencies required.

---

## 功能 Features

- 📋 查看草稿列表 / List drafts
- ✏️ 创建新草稿（自动生成封面图 + 自动上传正文配图）/ Create new drafts (auto cover + inline images)
- 🔄 更新已有草稿 / Update existing drafts
- 🗑️ 删除草稿 / 批量删除 / Delete drafts
- 🔍 按标题关键词搜索草稿 / Search drafts by keyword
- 🖼️ 独立生成封面图预览 / Generate cover image preview
- 📊 生成正文配图（流程图/对比图/时间线/文字卡片/统计图）/ Generate infographics
- 📦 素材库管理（上传/列表/删除/统计）/ Material library management
- 👥 用户管理（用户列表/用户信息/用户统计）/ User management
- ✨ 去AI味 — 去除文字中的 AI 生成痕迹 / Remove AI-generated flavor
- 🔄 三种推送模式：直连 / 中转 / 混合 / Three push modes: direct / relay / hybrid

---

## 配套公众号 Companion Account

本工具由公众号 **「技术定义未来」** 配套开发。

- 公众号：技术定义未来
- 定位：AI 工具效率提升 + AI 商业化场景探索

---

## 快速开始 Getting Started

### 1. 安装依赖 Install Dependencies

```bash
pip install requests Pillow
```

> 去AI味功能需要额外安装：`pip install fastapi uvicorn`

### 2. 获取 AppID 和 AppSecret Get AppID & AppSecret

1. 登录 [微信公众平台](https://mp.weixin.qq.com)
2. 进入 **设置与开发 → 基本设置**
3. 复制 **AppID** 和 **AppSecret**（如未设置需先启用）

### 3. 配置 IP 白名单 Configure IP Whitelist

> ⚠️ **这一步非常重要！不配置 IP 白名单，直连模式所有 API 调用都会失败。**

微信官方 API 要求调用方 IP 必须在白名单中。根据你选择的推送模式（见下方），配置方式不同：

**直连模式 (direct) / 混合模式 (hybrid) 需要配置本机 IP：**

```bash
# 步骤 1：查看本机出口 IP
curl ifconfig.me

# 输出示例：120.79.2.44
```

```
步骤 2：登录微信公众平台
  → 设置与开发 → 安全中心 → IP 白名单 → 点击「配置」

步骤 3：将上一步获取的 IP 填入白名单
  → 多个 IP 用回车分隔
  → 保存
```

**中转模式 (relay) 需要配置服务器 IP：**

如果你使用中转模式，需要将 **中转服务器的公网 IP** 加入白名单（而不是你本机的 IP）。

```bash
# 查看中转服务器 IP（在中转服务器上执行）
curl ifconfig.me
```

> 💡 **不方便配 IP 白名单？** 使用 `hybrid` 或 `relay` 模式即可跳过本机 IP 配置。
> `hybrid` 模式会先尝试直连，IP 白名单失败后自动切换中转。

### 4. 配置凭证 Configure Credentials

```bash
cp config.example.json config.json
# 编辑 config.json，填入你的凭证
```

`config.json` 完整字段说明：

| 字段 | 必填 | 说明 |
|------|------|------|
| `APP_ID` | ✅ | 微信公众号 AppID |
| `APP_SECRET` | ✅ | 微信公众号 AppSecret |
| `author` | ✅ | 默认作者名 |
| `PUSH_MODE` | ❌ | 推送模式：`direct`(默认) / `relay` / `hybrid` |
| `WECHAT_OA_SERVER` | relay/hybrid 必填 | 中转服务器地址，如 `http://120.79.2.44` |
| `WECHAT_OA_SERVER_KEY` | relay/hybrid 必填 | 中转服务器 API Key（服务端分配） |
| `CLAUDE_API_KEY` | 去AI味必填 | Claude API Key（用于去AI味功能） |
| `ALIPAY_AI_PAY_SKILL_ID` | 去AI味必填 | 支付宝 AI 付 Skill ID |

完整示例：

```json
{
  "APP_ID": "wx0000000000000000",
  "APP_SECRET": "00000000000000000000000000000000",
  "author": "你的名字",
  "PUSH_MODE": "hybrid",
  "WECHAT_OA_SERVER": "http://120.79.2.44",
  "WECHAT_OA_SERVER_KEY": "your-server-key-here",
  "CLAUDE_API_KEY": "sk-ant-...",
  "ALIPAY_AI_PAY_SKILL_ID": "your-skill-id-here"
}
```

> ⚠️ `config.json` 包含凭证，**不要提交到 GitHub**！已在 `.gitignore` 中忽略。

---

## 推送模式详解 Push Modes

`config.json` 中 `PUSH_MODE` 支持三种模式，根据你的网络环境选择：

### 模式对比

| 模式 | 说明 | 需配 IP 白名单 | 适用场景 |
|------|------|:-:|----------|
| **direct** | 直连微信官方 API | ✅ 本机 IP | 服务器 IP 固定且可加入白名单 |
| **relay** | 通过公共中转服务器推送 | ❌ | 本机 IP 不固定，或无法配白名单 |
| **hybrid** | 优先 direct，失败自动切换 relay | 自动 | **推荐** — 兼顾速度与兼容性 |

```
direct 模式:
  本机 ──→ 微信官方 API
  （本机 IP 必须在白名单中）

relay 模式:
  本机 ──→ 中转服务器 ──→ 微信官方 API
  （中转服务器 IP 必须在白名单中）

hybrid 模式:
  本机 ──→ 直连微信 API（尝试）
    │
    └─ 失败(IP白名单) ──→ 中转服务器 ──→ 微信官方 API（自动切换）
```

### 各模式配置

#### direct（直连模式）

```json
{
  "PUSH_MODE": "direct"
}
```

- 无需额外配置
- 需要将 **本机出口 IP** 加入微信公众号白名单
- 速度最快，最稳定

#### relay（中转模式）

```json
{
  "PUSH_MODE": "relay",
  "WECHAT_OA_SERVER": "http://120.79.2.44",
  "WECHAT_OA_SERVER_KEY": "联系作者获取"
}
```

- 无需配置本机 IP 白名单
- 通过公共中转服务器（http://120.79.2.44）转发请求
- 适合 IP 不固定的开发环境

#### hybrid（混合模式 — 推荐）

```json
{
  "PUSH_MODE": "hybrid",
  "WECHAT_OA_SERVER": "http://120.79.2.44",
  "WECHAT_OA_SERVER_KEY": "联系作者获取"
}
```

- 先尝试直连，失败自动切换中转
- 最佳兼容性：有白名单时走直连（快），没有时走中转（稳）

---

## 获取中转服务器密钥 Get Relay Server Key

使用 `relay` 或 `hybrid` 模式需要配置 `WECHAT_OA_SERVER_KEY`。

请联系作者获取密钥：
- GitHub Issues：[https://github.com/andy8663/wechat-oa](https://github.com/andy8663/wechat-oa)
- 邮箱：`andy8663@163.com`
- 微信公众号：技术定义未来

获取密钥后，在 `config.json` 中配置：

```json
{
  "PUSH_MODE": "hybrid",
  "WECHAT_OA_SERVER": "http://120.79.2.44",
  "WECHAT_OA_SERVER_KEY": "你获取的密钥"
}
```

验证连通性：

```bash
python relay_client.py info
# 返回服务信息说明配置成功
```

---

## 使用示例 Usage

### 基本操作

```bash
# 查看草稿列表
python wechat_push.py list

# 创建新草稿（自动生成封面 + 自动上传正文配图）
python wechat_push.py create article.html

# 更新已有草稿
python wechat_push.py update <media_id> article.html

# 更新草稿 + 强制重新生成封面
python wechat_push.py update <media_id> article.html --force-cover

# 删除草稿
python wechat_push.py delete <media_id>

# 批量删除草稿
python wechat_push.py batch-del <id1> <id2> <id3>

# 按标题关键词搜索草稿
python wechat_push.py find "关键词"

# 生成封面图预览（不推送到微信）
python wechat_push.py cover "文章标题"
```

### 素材管理

```bash
# 上传图片到永久素材库
python wechat_push.py upload cover.png

# 获取各类永久素材总数
python wechat_push.py materialcount

# 获取素材列表（支持关键词过滤）
python wechat_push.py materials image 20 0 "关键词"

# 交互式删除素材
python wechat_push.py materialdel

# 批量删除素材
python wechat_push.py materialdel <media_id1> <media_id2>
```

### 正文配图生成

```bash
# 流程图
python generate_infographic.py steps output/step.png "步骤1" "步骤2" "步骤3"

# 对比图
python generate_infographic.py comparison output/compare.png "传统方式:慢" "新方式:快"

# 时间线
python generate_infographic.py timeline output/timeline.png "2024:事件1" "2025:事件2"

# 文字卡片
python generate_infographic.py textcard output/quote.png "金句内容"

# 数据统计图
python generate_infographic.py stats output/stats.png "满意度:85" "便利性:90"
```

### 中转模式操作

```bash
# 查看推送服务信息（是否收费、价格）
python relay_client.py info

# 通过中转服务器推送文章
python relay_client.py push article.html

# 通过中转服务器查看草稿列表
python relay_client.py list
```

---

## 去AI味功能 Remove AI Flavor

去除文字中的 AI 生成痕迹（如"综上所述"、"值得注意的是"、"此外"等），让文字更自然。

### 使用方式

```bash
# 命令行调用（按次收费 1 元，通过支付宝 AI 付协议）
python wechat_push.py quaiwei "综上所述，这款产品值得注意的是，此外还有很好的用户体验..."
```

### 工作原理

1. 调用 `quaiwei_server.py` 提供的 HTTP API
2. 服务端返回 HTTP 402 + 支付链接（标准 AI 付协议）
3. 用户扫码支付 1 元
4. 支付成功后，服务端调用 Claude API 进行文字改写
5. 返回去 AI 味后的文字

### 前置条件

- `config.json` 中配置 `CLAUDE_API_KEY` 和 `ALIPAY_AI_PAY_SKILL_ID`
- 安装 `fastapi` 和 `uvicorn`：`pip install fastapi uvicorn`
- 启动去 AI 味服务：`python quaiwei_server.py`

---

## 正文配图自动上传 Inline Image Upload

创建或更新草稿时，系统会自动处理正文中的本地图片：

1. 提取 HTML/MD 中的 `<img src="...">` 或 `![alt](path)`
2. 本地图片自动上传到微信素材库
3. 替换 HTML 中的 `src` 为微信 CDN URL
4. 网络图片（http/https）保留原样
5. 已是微信素材库图片（`mmbiz.qpic.cn`）跳过

```html
<!-- 本地图片：自动上传并替换 URL -->
<img src="./images/diagram.png" alt="架构图">

<!-- 网络图片：保留原样 -->
<img src="https://example.com/external.png">
```

---

## 排版规范 Layout Specification

创建或更新公众号文章前，建议阅读 `design.md` 排版规范，确保 HTML 兼容微信渲染器。

规范涵盖：容器宽度、字体、配色、布局、标题、内容结构、CSS/HTML/JS 限制等。

---

## Troubleshooting 常见问题

### `errcode: 40164` — IP 白名单问题

```
{"errcode": 40164, "errmsg": "invalid ip xxx.xxx.xxx.xxx, not in whitelist"}
```

**原因**：当前 IP 不在微信公众号白名单中。

**解决**：
1. 查看出错信息中的 IP 地址
2. 登录微信公众平台 → 设置与开发 → 安全中心 → IP 白名单
3. 将该 IP 添加到白名单
4. 或切换到 `relay` / `hybrid` 模式

### `errcode: 40125` — AppSecret 错误

```
{"errcode": 40125, "errmsg": "invalid appsecret"}
```

**原因**：`config.json` 中的 `APP_SECRET` 不正确。

**解决**：
1. 登录微信公众平台 → 设置与开发 → 基本设置
2. 检查 AppSecret 是否正确（注意前后空格）
3. 如不确定，可重置 AppSecret 后重新填入

### `errcode: 40001` — access_token 无效

```
{"errcode": 40001, "errmsg": "invalid credential"}
```

**原因**：access_token 过期或获取失败。

**解决**：
1. 检查 AppID 和 AppSecret 是否正确
2. 检查 IP 白名单是否已配置
3. 重新运行命令（系统会自动获取新 token）

### 中转服务器连接失败

```
{"success": false, "error": "网络请求失败: ..."}
```

**原因**：无法连接中转服务器。

**解决**：
1. 检查 `WECHAT_OA_SERVER` 地址是否正确
2. 检查服务器是否运行：`curl http://your-server-ip:8000/`
3. 检查 `WECHAT_OA_SERVER_KEY` 是否正确
4. 检查服务器防火墙是否开放对应端口

### 推送模式如何选择？

| 你的情况 | 推荐模式 |
|---------|---------|
| 服务器 IP 固定，可配白名单 | `direct` |
| 本机 IP 不固定，有公网服务器 | `hybrid`（推荐） |
| 本机 IP 不固定，无公网服务器 | 需先部署中转服务器，再用 `relay` |

---

## 依赖 Dependencies

| 依赖 | 用途 | 必填 |
|------|------|:----:|
| `requests` | HTTP 请求 | ✅ |
| `Pillow` | 封面图/配图生成 | ✅ |
| `fastapi` | 去AI味服务 | ❌（仅去AI味功能需要） |
| `uvicorn` | 去AI味服务 | ❌（仅去AI味功能需要） |

```bash
# 基础安装
pip install requests Pillow

# 完整安装（含去AI味功能）
pip install requests Pillow fastapi uvicorn
```

---

## 问题反馈 Feedback

- GitHub Issues：[https://github.com/andy8663/wechat-oa](https://github.com/andy8663/wechat-oa)
- 邮箱：`andy8663@163.com`
- 微信公众号：技术定义未来

---

## License

MIT
