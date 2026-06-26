---
name: wechat-md-publisher
description: 发布 Markdown 文章到微信公众号，支持草稿管理、多主题、智能图片处理、自动封面图。推荐与 news-to-markdown-skill 配合使用实现一键转载（支持本地图片）。
version: 1.0.8
author: Ping Si <sipingme@gmail.com>
user-invocable: true
requires:
  runtime:
    - name: node
      version: ">=18.0.0"
    - name: npm
      version: ">=8.0.0"
install:
  type: npm-global
  package: wechat-md-publisher
  version: "1.0.7"
  versionPinning: exact
  execution: "npm install -g wechat-md-publisher@1.0.7"
  global: true
  autoInstall: false
  autoUpdate: false
  riskLevel: low
  riskReason: |
    启动器以 in-process 动态 import 调用本机已安装的 wechat-md-publisher，
    并在 import 之前校验 manifest.name 与 manifest.version 是否精确等于内置 pin。
    解析路径仅包含 Node 全局 node_modules 与 Skill 自身 node_modules；
    当前工作目录 (CWD) 下的 node_modules 已被显式排除，避免被未审计的本地包替身劫持。
    安装前请审计上游源码与凭证加密实现。
  trustedResolutionRoots:
    - "<node-prefix>/lib/node_modules"
    - "<node-prefix>/node_modules (Windows)"
    - "<skill-dir>/node_modules"
  untrustedResolutionRoots:
    - "process.cwd()/node_modules (intentionally excluded)"
  source:
    registry: https://registry.npmjs.org
    repository: https://github.com/sipingme/wechat-md-publisher
    license: Apache-2.0
    audit: https://github.com/sipingme/wechat-md-publisher/blob/main/src/index.ts
    auditCredentials: https://github.com/sipingme/wechat-md-publisher/blob/main/src/services/account.ts
env:
  optional:
    - name: WECHAT_APP_ID
      description: 微信公众号 AppID
      sensitive: false
    - name: WECHAT_APP_SECRET
      description: 微信公众号 AppSecret
      sensitive: true
  note: |
    凭证可通过两种方式提供（二选一）：
    1. 环境变量（推荐，避免凭证暴露在进程列表中）
    2. CLI 命令：`account add --app-id xxx --app-secret xxx`
configPaths:
  - path: ~/.config/wechat-md-publisher-nodejs/
    description: 账号配置和缓存目录
    contains:
      - credentials: true
      - encryption: AES-256
permissions:
  filesystem:
    read:
      - "*.md": "读取用户指定的 Markdown 文件"
      - "*.jpg,*.png,*.gif": "读取文章中引用的本地图片"
    write:
      - "~/.config/wechat-md-publisher-nodejs/": "存储账号配置和缓存（凭证使用 AES-256 加密）"
  network:
    required:
      - "api.weixin.qq.com": "微信公众号 API（发布、草稿、素材管理）"
      - "mp.weixin.qq.com": "微信公众号素材上传"
    optional:
      - "remote-theme-api": "仅当用户使用 theme add-remote 命令时才会访问（⚠️ 需用户明确配置并信任该端点）"
credentials:
  - name: WECHAT_APP_SECRET
    type: api-secret
    storage:
      location: ~/.config/wechat-md-publisher-nodejs/
      encryption: AES-256
      handler: wechat-md-publisher npm 包
      handlerRepo: https://github.com/sipingme/wechat-md-publisher
    consent: 需要用户明确提供，不会自动收集
    securityNote: |
      本 skill 不直接处理凭证加密，安全性依赖上游 npm 包的实现。
      建议在提供凭证前审查 wechat-md-publisher 包的加密实现：
      https://github.com/sipingme/wechat-md-publisher/blob/main/src/services/account.ts
tags:
  - wechat
  - publishing
  - markdown
  - content-management
repository: https://github.com/sipingme/wechat-md-publisher
---

# WeChat Publisher Skill

全功能微信公众号 Markdown 发布工具 - 让 AI 能够直接将内容发布到微信公众号。

## ⚠️ 重要提示

**推荐使用方式**：
- ✅ **最佳实践**：与 `news-to-markdown-skill` 配合使用，实现一键转载新闻到微信公众号
- 🌐 **固定公网 IP**：必须有固定公网 IP 并配置到微信公众平台的 IP 白名单
- 🔑 **必需凭证**：必须配置 `WECHAT_APP_ID` 和 `WECHAT_APP_SECRET` 环境变量或通过命令行配置

**关键要求**：
1. **固定公网 IP**：微信 API 要求服务器 IP 在白名单中，动态 IP 无法使用
2. **微信公众号凭证**：需要从微信公众平台获取 AppID 和 AppSecret
3. **IP 白名单配置**：在微信公众平台「设置与开发」→「基本配置」→「IP 白名单」中添加你的公网 IP

## ⚡ 快速开始

### ⚠️ 安全风险与审计要点

**安装与执行模型（请先阅读）**：
- 本 Skill 的启动器 (`scripts/run.js`) 不会执行任何子进程，也不会通过 `npx` 在运行时从 registry 拉取代码。
- 启动器使用 in-process 动态 `import` 调用 **本机已经全局安装** 的 `wechat-md-publisher` 包。
- 因此，安装步骤是显式的、**必须使用精确版本**：`npm install -g wechat-md-publisher@1.0.7`。
- 启动器在 `import` 之前会读取已解析包的 `package.json`，**校验 `name` 与 `version` 精确等于内置 pin**；任何不匹配（含同名替身、未审计的新版本）都会被拒绝。
- 解析路径限定为 Node 全局 `node_modules` 与 Skill 自身 `node_modules`；**CWD 下的 `node_modules` 已被显式排除**，避免从含未审计依赖的工作目录启动时被恶意本地包劫持。
- 这样可以让用户在安装前完整审计上游源码、签名与版本，避免 "每次运行都从 npm 拉新代码" 的供应链风险面。

**必须审计的上游代码**（首次安装前）：
- **CLI 入口与命令分发**: https://github.com/sipingme/wechat-md-publisher/blob/main/src/index.ts
- **账号 / 凭证加密实现**: https://github.com/sipingme/wechat-md-publisher/blob/main/src/services/account.ts
- 重点关注：AES-256 是否使用 AEAD 模式（如 AES-GCM / AES-CBC + HMAC）、密钥派生方式、是否绑定到当前用户、加密文件权限。

**凭证存储**：账号凭证存储在 `~/.config/wechat-md-publisher-nodejs/`，使用 AES-256 加密。本 skill 不直接处理加密，安全性依赖上游 npm 包的实现 —— 必须在审计上述 `account.ts` 之后再写入真实凭证。

**凭证传递的最佳实践**：
- 推荐使用环境变量 `WECHAT_APP_ID` / `WECHAT_APP_SECRET`，避免 `--app-secret` 出现在 `ps` 进程列表中。
- 任何时候在 shell history、CI 日志、容器元数据中暴露 `AppSecret`，都应立即去微信公众平台重置。

**远程主题风险**：如果使用 `theme add-remote` 添加远程主题，第三方端点可能接收文章正文 / 标题。请只使用受信任的主题源；本 Skill 默认网络白名单**不包含**任意第三方主题端点。

**沙箱建议**：若你无法或不愿审计上游 npm 包，请在隔离环境（专用 VM / 容器 / 沙箱账号）中运行；不要把生产微信公众号的 AppSecret 直接交给未审计的工具链。

### 配置账号

**推荐方式（使用环境变量，避免命令行暴露凭证）**：

```bash
# 设置环境变量（不会出现在进程列表中）
export WECHAT_APP_ID="wx_your_app_id"
export WECHAT_APP_SECRET="your_app_secret"

# 添加账号
wechat-pub account add \
  --name "我的公众号" \
  --default
```

**备选方式（命令行传参，注意：可能暴露在进程列表中）**：

```bash
# ⚠️ 警告：--app-secret 会出现在 ps 进程列表中
wechat-pub account add \
  --name "我的公众号" \
  --app-id "wx_your_app_id" \
  --app-secret "your_app_secret" \
  --default
```

### 发布文章

```bash
wechat-pub publish create \
  --file article.md \
  --theme orangesun
```

### 与 news-to-markdown 配合使用

```bash
# 一键转载新闻到微信公众号（推荐：下载图片到本地）
# news-to-markdown 会自动下载图片到本地，避免远程 URL 过期问题
convert-url --url "https://www.toutiao.com/article/123" \
  --output /tmp/article.md \
  --download-images \
  --output-dir /tmp/article

# wechat-md-publisher 会自动读取本地图片并上传
wechat-pub publish create --file /tmp/article/article.md --theme orangesun
```

**图片处理最佳实践**（v0.8.3+）：
- ✅ **推荐**：使用 `--download-images` 下载图片到本地
  - 避免远程 URL 签名过期（如头条图片）
  - 避免防盗链问题
  - 提高发布成功率
- news-to-markdown 自动提取封面图（og:image > twitter:image > 第一张图片）
- 图片保存到 `./images/` 目录，Markdown 使用相对路径
- wechat-md-publisher 自动上传本地图片到微信素材库
- 完全自动化，无需手动处理

---

## 🎯 何时使用此 Skill

当用户需要以下操作时，应触发此 Skill：

- ✅ 发布文章到微信公众号
- ✅ 创建微信公众号草稿
- ✅ 管理微信公众号账号
- ✅ 查看已发布的文章列表
- ✅ 删除草稿或已发布文章
- ✅ 使用不同主题渲染 Markdown
- ✅ 在文章开头/结尾添加固定图文（Wrapper 功能）
- ✅ 查看或回滚 Wrapper 历史版本

**触发关键词**：
- "发布到微信公众号"
- "创建微信草稿"
- "配置微信公众号"
- "查看微信文章"
- "使用 [主题名] 主题发布"
- "文章开头结尾固定内容"
- "Wrapper"

## 📋 前置要求

### 1. 系统要求
- Node.js >= 18.0.0
- npm 或 pnpm 包管理器
- 网络连接（访问微信 API）

### 2. 微信公众号配置
用户必须拥有微信公众号并获取：
- **AppID**：开发者 ID
- **AppSecret**：开发者密码
- **IP 白名单**：必须配置（重要！）

获取方式：
1. 登录 [微信公众平台](https://mp.weixin.qq.com/)
2. 进入「设置与开发」→「基本配置」
3. 获取「开发者ID(AppID)」和「开发者密码(AppSecret)」
4. **配置 IP 白名单**（必须！）：
   - 获取当前 IP：`curl ifconfig.me`
   - 在「IP白名单」中添加该 IP
   - 详细指南：[IP 白名单配置指南](./references/ip-whitelist-guide.md)

### 3. 安装方式

本 Skill 要求在首次使用前**显式全局安装**底层 npm 包，以便用户审计源码并避免运行时从 registry 拉代码：

```bash
# 一次性安装（请先阅读上文 "安全风险与审计要点" 完成审计；必须使用精确版本）
npm install -g wechat-md-publisher@1.0.7

# 验证可用且版本精确等于 1.0.7
wechat-pub --version

# 查看帮助
wechat-pub --help
```

> ⚠️ 不要在含有未审计 `node_modules` 的工作目录下运行 Skill。启动器只在受信路径解析包；CWD 下的 `node_modules` 已被显式排除。

安装完成后，Skill 启动器（`scripts/run.js`）会通过 in-process 动态 `import` 调用本机已安装的 `wechat-md-publisher`，不再触发任何 `npx` 网络请求或子进程。

## 🚀 标准操作流程 (SOP)

### ⚠️ AI 自动化必须遵守：草稿优先 + 人工确认

`publish create` 与 `publish submit` 会让文章对公众号粉丝**立即可见**。错误的标题、抓取错误的正文、未压缩的图片，或被远程主题污染的渲染，一旦发布即对外暴露，可能造成公众号违规、品牌或合规风险。

因此当此 Skill 在 AI / 自动化流程中被调用时，**默认行为**必须是：

1. 调用 `draft create`（不是 `publish create`），把内容创建为草稿。
2. 向用户回报：标题、所用主题、首图/封面来源、图片是否已上传到微信素材库。
3. 等待用户在微信公众平台后台或预览中**明确确认**后，再调用 `publish create` 或 `publish submit`。
4. 任何 `delete`、`wrapper set`、`account add` 等会改变线上或本地状态的操作，同样要求用户明确确认。

直接 `publish create` 仅在用户**显式要求"立即发布"**且 AI 已经完整复述（标题/主题/正文要点/图片）并获得"确认发布"回复后才允许执行。

---

### 操作 1：配置微信公众号账号

**场景**：首次使用或添加新账号

**步骤**：

1. 收集用户提供的账号信息（AppID 和 AppSecret）
2. 执行命令添加账号：

```bash
wechat-pub account add \
  --name "账号名称" \
  --app-id "wx_your_app_id" \
  --app-secret "your_app_secret" \
  --default
```

3. 验证账号添加成功：

```bash
wechat-pub account list
```

**输出示例**：
```
┌────────────┬──────────────┬────────────────┬─────────┐
│ ID         │ 名称         │ AppID          │ 默认    │
├────────────┼──────────────┼────────────────┼─────────┤
│ acc_xxx    │ 我的公众号   │ wx123456       │ ✓       │
└────────────┴──────────────┴────────────────┴─────────┘
```

**异常处理**：
- 如果 AppID/AppSecret 错误，会提示"认证失败"
- 如果网络问题，会提示"无法连接到微信服务器"
- 解决方案：检查凭证是否正确，确认 IP 在白名单中

---

### 操作 2：创建并发布文章（一步到位）

**场景**：用户提供 Markdown 内容，并**已明确要求立即发布**到公众号（如果未明确要求，请走"操作 3：创建草稿"）

**步骤**：

1. 将用户的 Markdown 内容保存到临时文件：

```bash
cat > /tmp/article.md << 'EOF'
---
title: 文章标题
author: 作者名
---

# 文章内容

这里是正文...
EOF
```

2. 执行发布命令：

```bash
wechat-pub publish create \
  --file /tmp/article.md \
  --theme orangesun
```

3. 解析输出，提取 `publish_id`

**输出示例**：
```
✓ 渲染完成
✓ 图片处理完成
✓ 创建草稿成功
✓ 发布成功

发布 ID: 2247483647_1
```

4. 向用户报告成功，并提供发布 ID

**可用主题**：
- `default` - 默认主题（简洁清爽）
- `orangesun` - Orange Sun（温暖明亮）
- `redruby` - Red Ruby（优雅醒目）
- `greenmint` - Green Mint（清新舒适）
- `purplerain` - Purple Rain（梦幻柔和）
- `blackink` - Black Ink（深色模式）

**异常处理**：
- 图片上传失败：检查图片路径和网络
- Token 过期：自动刷新，无需手动处理
- 内容违规：微信会返回错误码，提示用户修改内容

---

### 操作 3：创建草稿（不立即发布）

**场景**：用户想先创建草稿，稍后再发布

**步骤**：

1. 保存 Markdown 内容到文件
2. 执行草稿创建命令：

```bash
wechat-pub draft create \
  --file /tmp/article.md \
  --theme default
```

3. 记录返回的 `media_id`

**输出示例**：
```
✓ 草稿创建成功

Media ID: 3_abcdefghijk123456
```

4. 告知用户草稿已创建，可以在微信公众平台查看

**后续操作**：
- 用户可以在微信公众平台编辑草稿
- 需要发布时，使用 `wechat-pub publish submit <media-id>`

---

### 操作 4：查看草稿列表

**场景**：用户想查看所有草稿

**命令**：

```bash
wechat-pub draft list --page 1 --size 10
```

**输出示例**：
```
共 15 个草稿

┌──────────────────┬────────────────┬────────────────┐
│ Media ID         │ 标题           │ 更新时间       │
├──────────────────┼────────────────┼────────────────┤
│ 3_abc123         │ 测试文章       │ 2026-03-19     │
│ 3_def456         │ 产品介绍       │ 2026-03-18     │
└──────────────────┴────────────────┴────────────────┘
```

---

### 操作 5：查看已发布文章

**场景**：用户想查看已发布的文章

**命令**：

```bash
wechat-pub publish list --page 1 --size 10
```

**输出示例**：
```
共 8 篇已发布文章

┌──────────────┬────────────────┬────────────────┬──────────────────┐
│ Article ID   │ 标题           │ 发布时间       │ URL              │
├──────────────┼────────────────┼────────────────┼──────────────────┤
│ 2247483647_1 │ 最新文章       │ 2026-03-19     │ https://mp.we... │
└──────────────┴────────────────┴────────────────┴──────────────────┘
```

---

### 操作 6：删除草稿或文章

**删除草稿**：

```bash
wechat-pub draft delete <media-id>
```

**删除已发布文章**：

```bash
wechat-pub publish delete <article-id>
```

---

### 操作 7：查看可用主题

**命令**：

```bash
wechat-pub theme list
```

**输出示例**：
```
可用主题：

┌─────────────┬──────────────┬────────────────────┐
│ ID          │ 名称         │ 描述               │
├─────────────┼──────────────┼────────────────────┤
│ default     │ 默认主题     │ 简洁清爽风格       │
│ orangesun   │ Orange Sun   │ 温暖明亮风格       │
│ redruby     │ Red Ruby     │ 优雅醒目风格       │
│ greenmint   │ Green Mint   │ 清新舒适风格       │
│ purplerain  │ Purple Rain  │ 梦幻柔和风格       │
│ blackink    │ Black Ink    │ 深色模式风格       │
└─────────────┴──────────────┴────────────────────┘
```


---

## 🔧 高级用法

### Wrapper 功能：文章开头/结尾固定图文

在发布文章时自动在开头和结尾添加固定的图文内容（如关注引导、底部二维码等）。

**开启功能**：
```bash
wechat-pub wrapper on
```

**设置内容**：
```bash
wechat-pub wrapper set \
  --header "<div>欢迎关注我们的公众号</div>" \
  --footer "<div>觉得有帮助请点赞+收藏</div>"
```

**查看状态**：
```bash
wechat-pub wrapper status
```

**查看历史版本**：
```bash
wechat-pub wrapper history
```

**回滚到指定版本**：
```bash
wechat-pub wrapper rollback 1
```

**关闭功能**：
```bash
wechat-pub wrapper off
```

**注意事项**：
- 功能默认关闭，需要手动开启
- 每次 `set` 会创建新版本，支持历史回滚
- 图片处理：目前直接存储原始 HTML，需要公网可访问的图片 URL
- 数据库文件：`data/wmp.db`

---

### 使用编程 API

如果需要在代码中集成：

```javascript
const { container } = require('wechat-md-publisher');

async function publishArticle(markdown, theme) {
  await container.initialize();
  
  const publishService = await container.getPublishService();
  const result = await publishService.createAndPublish({
    markdown: markdown,
    theme: theme || 'default',
  });
  
  return result.publish_id;
}
```

### 批量发布

```bash
# 批量创建草稿
for file in articles/*.md; do
    wechat-pub draft create --file "$file" --theme default
done
```

---

## 📊 输入输出规范

### 输入格式

**Markdown 文件格式**：

```markdown
---
title: 文章标题（必需）
author: 作者名（可选）
cover: ./cover.jpg（可选，封面图路径）
---

# 正文标题

正文内容...

![图片描述](./image.jpg)
```

**支持的图片格式**：
- 本地图片：相对路径或绝对路径
- 网络图片：HTTP/HTTPS URL
- 微信图片：微信 CDN URL（自动识别）

### 输出格式

**成功响应**：
```json
{
  "success": true,
  "publish_id": "2247483647_1",
  "message": "发布成功"
}
```

**错误响应**：
```json
{
  "success": false,
  "error": "错误信息",
  "code": "ERROR_CODE"
}
```

---

## ⚠️ 常见问题和解决方案

### 问题 1：Token 过期

**症状**：提示"access_token 无效"

**解决**：Token 会自动刷新，如果仍有问题，重新配置账号

### 问题 2：图片上传失败

**症状**：提示"图片上传失败"

**原因**：
- 图片路径错误
- 图片大小超限（微信限制 10MB）
- 服务器 IP 不在白名单

**解决**：
- 检查图片路径
- 压缩图片
- 在微信公众平台添加 IP 到白名单

### 问题 3：找不到主题

**症状**：提示"主题不存在"

**解决**：使用 `wechat-pub theme list` 查看可用主题

### 问题 4：权限不足

**症状**：提示"没有权限"

**原因**：AppID/AppSecret 错误或权限不足

**解决**：
- 确认凭证正确
- 确认公众号类型支持该功能（服务号 vs 订阅号）

---

## 🔒 安全性说明

### 敏感信息处理

- AppID 和 AppSecret 存储在本地配置文件中
- 配置文件位置：
  - macOS: `~/Library/Preferences/wechat-md-publisher-nodejs/config.json`
  - Linux: `~/.config/wechat-md-publisher-nodejs/config.json`
  - Windows: `%APPDATA%\wechat-md-publisher-nodejs\Config\config.json`

### 权限要求

- 读取本地文件（Markdown 和图片）
- 网络访问（微信 API）
- 写入配置文件

### 数据隐私与运维要点

- ✅ 默认不会上传任何数据到第三方服务器；所有通信仅限于微信官方 API（`api.weixin.qq.com` / `mp.weixin.qq.com`）。
- ✅ 图片缓存仅在本地。
- ✅ 建议把 `~/.config/wechat-md-publisher-nodejs/` 权限设为 `0700`，并排除在备份/容器镜像/同步盘之外。
- ✅ 使用环境变量（`WECHAT_APP_ID` / `WECHAT_APP_SECRET`）而非 `--app-secret` 命令行参数，避免出现在 `ps`、shell history、CI 日志中。
- ✅ 优先使用最小权限或测试公众号验证流程后再切到生产账号；如怀疑泄露，立即在公众平台重置 `AppSecret` 并删除本地缓存目录。
- ⚠️ 例外：如果用户主动启用 `theme add-remote`，会把文章正文 / 标题 / 图片 URL 发送到该第三方端点，构成新的数据边界，请仅使用受信任的主题源；AI 自动化流程不应在未经用户授权的情况下启用远程主题。

---

## 📚 参考资料

- [项目 GitHub](https://github.com/sipingme/wechat-md-publisher)
- [微信公众平台文档](https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html)
- [完整 API 文档](https://github.com/sipingme/wechat-md-publisher/blob/main/docs/API.md)

---

## 🎓 示例对话

**用户**：帮我把这篇文章发布到微信公众号

**AI**：好的，我来帮你发布。请提供文章的 Markdown 内容。

**用户**：[提供内容]

**AI**：收到！我将使用 orangesun 主题发布。正在处理...

[执行命令]

**AI**：✅ 文章已成功发布到微信公众号！
- 发布 ID: 2247483647_1
- 你可以在微信公众平台查看和管理这篇文章

---

## 📝 维护说明

- **版本**: 1.0.8
- **最后更新**: 2026-05-11
- **更新内容（1.0.8 — 安全加固版）**:
  - **供应链加固**：启动器 (`scripts/run.js`) 在 `import` 之前读取已解析包的 `package.json`，**校验 `name` 与 `version` 精确等于内置 pin（当前 `1.0.7`）**，否则拒绝加载。可阻止同名替身包 / 未审计的新版本静默接管 WeChat 凭证。
  - **关闭 CWD 解析后门**：包解析路径**显式排除 `process.cwd()/node_modules`**，只在 Node 全局 `node_modules` 与 Skill 自身 `node_modules` 中解析；从含未审计依赖的目录启动 Skill 不再可能被恶意本地包劫持。
  - **精确版本钉死**：所有安装命令与依赖元数据从 `^1.0.7` / 未版本化的 `npm install` 改为 `wechat-md-publisher@1.0.7`（含 `references/quick-start.md`、`ip-whitelist-guide.md`）。
  - **草稿优先 SOP**：新增 "AI 自动化必须遵守：草稿优先 + 人工确认" 章节；`config.json` 标记 `permissions.publishing.autoPublishWithoutConfirmation: false`，明确 AI 默认走 `draft create` + 人工确认路径。
  - **凭证最佳实践**：补充环境变量优先、`~/.config/wechat-md-publisher-nodejs/` 目录权限收紧、最小权限/测试公众号、泄露应急流程。
  - **远程主题数据边界**：强化 `theme add-remote` 警告 — 内置/本地主题为默认，AI 不应在未授权情况下启用远程主题。
- **更新内容（1.0.7）**:
  - 明确内置主题为 6 个自定义主题（default, blackink, orangesun, redruby, greenmint, purplerain）
  - 移除历史遗留的 wenyan-core 主题注册（lapis, maize 等），避免加载不存在的主题
  - 更新 THEMES.md 文档与实际可用主题保持一致
- **维护者**: Ping Si <sipingme@gmail.com>
- **许可证**: Apache-2.0

---

## ✅ 首次成功检查清单

新用户应该能在 5 分钟内完成：

- [ ] 验证工具可用：`wechat-pub --version`
- [ ] 配置账号：`wechat-pub account add ...`
- [ ] 创建测试文章
- [ ] 发布成功：`wechat-pub publish create --file test.md --theme default`
- [ ] 在微信公众平台看到文章

如果以上步骤都能顺利完成，说明 Skill 已正确配置！

---

## 🔗 与其他 Skills 配合使用

### 与 news-to-markdown-skill 组合使用

**推荐组合**：`news-to-markdown-skill` + `wechat-md-publisher-skill` = 一键转载新闻到微信公众号

#### 使用场景

将网络上的新闻文章快速转载到微信公众号，实现内容聚合和分发。

#### 完整工作流

**场景 1：转载单篇新闻（推荐方式）**

```bash
# 步骤 1: 使用 news-to-markdown 提取新闻并下载图片
convert-url --url "https://www.toutiao.com/article/123" \
  --output /tmp/article/article.md \
  --download-images \
  --output-dir /tmp/article \
  --verbose

# 步骤 2: 使用 wechat-md-publisher 发布到微信
wechat-pub publish create \
  --file /tmp/article/article.md \
  --theme orangesun
```

**为什么要下载图片到本地？**
- 头条图片 URL 包含签名和过期时间，几小时后会失效
- 本地图片更可靠，不受网络波动影响
- 避免防盗链导致的图片加载失败

**场景 2：批量转载新闻**

```bash
# 新闻 URL 列表
urls=(
  "https://www.toutiao.com/article/123"
  "https://mp.weixin.qq.com/s/abc"
  "https://www.xiaohongshu.com/explore/xyz"
)

# 批量处理
for i in "${!urls[@]}"; do
  url="${urls[$i]}"
  output_dir="/tmp/article-$i"
  
  # 提取新闻并下载图片
  convert-url --url "$url" \
    --output "$output_dir/article.md" \
    --download-images \
    --output-dir "$output_dir"
  
  # 发布到微信（创建草稿）
  wechat-pub draft create \
    --file "$output_dir/article.md" \
    --theme default
  
  echo "✓ 已处理: $url"
done
```

**场景 3：AI 自动化工作流**

用户对 AI 说：
> "帮我把这篇头条文章转载到我的微信公众号"

AI 执行流程：
1. 使用 `news-to-markdown-skill` 提取文章内容
2. 自动检测平台（头条/微信/小红书）
3. 使用 `wechat-md-publisher-skill` 发布到微信
4. 返回发布结果和链接

#### 优势

✅ **智能内容提取**
- 自动识别新闻正文，过滤广告和噪音
- 保留文章结构和格式
- 提取标题、作者、发布时间等元数据

✅ **多平台支持**
- 头条：优化标题层级、列表、代码块
- 微信：提取 `#js_content` 区域
- 小红书：处理 `.note-content` 内容

✅ **三层抓取策略**
- curl → wget → Playwright
- 确保动态页面也能正确抓取

✅ **精美主题渲染**
- 6 个精选内置主题可选
- 自动处理图片上传
- 保持排版美观

#### 最佳实践

**1. 内容审核**
```bash
# 先创建草稿，人工审核后再发布
convert-url --url "$news_url" --output /tmp/article.md
wechat-pub draft create --file /tmp/article.md --theme default

# 审核通过后发布
wechat-pub publish submit <media-id>
```

**2. 添加来源声明**
```bash
# 提取时保留元数据
convert-url --url "$news_url" --output /tmp/article.md

# 元数据会自动包含在 Markdown 中：
# ---
# title: 文章标题
# author: 原作者
# 来源: https://...
# ---
```

**3. 选择合适主题**
- 科技类文章：`default`、`blackink`（深色模式）
- 生活类文章：`orangesun`（橙色阳光）、`greenmint`（薄荷绿）
- 教程类文章：`default`、`greenmint`
- 文艺情感：`purplerain`（紫色雨）、`orangesun`
- 品牌时尚：`redruby`（宝石红）
- 夜间阅读：`blackink`

#### 示例对话

**用户**：把这篇头条文章转到我的微信公众号
https://www.toutiao.com/article/7000000000000000000/

**AI**：好的，我来帮你处理：

1. 正在提取文章内容...
   ```
   [INFO] 开始抓取: https://www.toutiao.com/article/...
   [INFO] 检测到平台: toutiao
   [INFO] 提取成功
   ```

2. 正在发布到微信公众号...
   ```
   ✓ 渲染完成
   ✓ 图片处理完成
   ✓ 创建草稿成功
   ✓ 发布成功
   ```

✅ **完成！**
- 文章标题：《xxx》
- 发布 ID: 2247483647_1
- 使用主题: orangesun
- 你可以在微信公众平台查看

#### 相关资源

- **news-to-markdown-skill**: https://github.com/sipingme/news-to-markdown-skill
- **news-to-markdown 核心库**: https://github.com/sipingme/news-to-markdown
- **npm 包**: `npm install -g news-to-markdown`

#### 技术栈

```
新闻网站
    ↓
news-to-markdown (提取 + 转换)
    ↓
Markdown 文件
    ↓
wechat-md-publisher (渲染 + 发布)
    ↓
微信公众号
```

---

## 💡 更多组合可能

### 与内容管理工具配合
- 配合 Git 进行版本管理
- 配合 CI/CD 实现自动发布
- 配合数据库存储发布记录

### 与 AI 工具配合
- AI 生成内容 → wechat-md-publisher 发布
- AI 润色文章 → wechat-md-publisher 发布
- AI 翻译文章 → wechat-md-publisher 发布
