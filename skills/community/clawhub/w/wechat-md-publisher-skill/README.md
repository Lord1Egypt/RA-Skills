# WeChat MD Publisher - OpenClaw Skill

> 全功能微信公众号 Markdown 发布工具 - OpenClaw Skill 版本

## 🛠️ 前置安装：底层 npm 包

本 Skill 的启动器 (`scripts/run.js`) 通过 in-process 动态 `import` 调用本机已安装的 `wechat-md-publisher`，**不会**通过 `npx` 在运行时从 registry 拉取代码。
因此**必须**在首次使用前显式全局安装底层包，并在安装前完成源码审计。

> ⚠️ **必须使用精确版本（无 caret、无 `@latest`）**。启动器会在 `import` 之前读取已解析包的 `package.json`，校验 `name` 与 `version` 是否与内置 pin（当前 `1.0.7`）精确匹配，任何不匹配都会被拒绝。这是为了防止本地或全局 `node_modules` 中出现的同名替身包被加载。

```bash
# 一次性安装（请先审计源码，详见下方链接）
npm install -g wechat-md-publisher@1.0.7

# 验证可用并精确等于 1.0.7
wechat-pub --version
```

请审计：
- CLI 入口：https://github.com/sipingme/wechat-md-publisher/blob/main/src/index.ts
- 凭证加密：https://github.com/sipingme/wechat-md-publisher/blob/main/src/services/account.ts

> 不要在含有未审计 `node_modules` 的工作目录下运行 Skill。启动器只在受信路径（Node 全局 `node_modules` 与 Skill 自身 `node_modules`）解析包；**当前工作目录（CWD）下的 `node_modules` 已被显式排除**。

## 🚀 快速安装（Skill 本身）

### 方法 1：从 ClawHub 安装（推荐）

```bash
openclaw skills install wechat-md-publisher
```

### 方法 2：从 GitHub 安装

```bash
openclaw skills install https://github.com/sipingme/wechat-md-publisher-skill
```

### 方法 3：手动安装

1. 克隆仓库：
```bash
git clone https://github.com/sipingme/wechat-md-publisher-skill.git
cd wechat-md-publisher-skill
```

2. 复制到 OpenClaw skills 目录：
```bash
cp -r . ~/.openclaw/skills/wechat-md-publisher/
```

3. 验证工具可用：
```bash
wechat-pub --version
```

## ✅ 验证安装

```bash
# 检查 Skill 是否可用
openclaw skills list --eligible

# 查看 Skill 详情
openclaw skills info wechat-md-publisher

# 测试命令
wechat-pub --version
```

## 📋 首次配置

### 1. 获取微信公众号凭证

1. 登录 [微信公众平台](https://mp.weixin.qq.com/)
2. 进入「设置与开发」→「基本配置」
3. 获取「开发者ID(AppID)」和「开发者密码(AppSecret)」
4. 将服务器 IP 添加到「IP白名单」

### 2. 配置账号

```bash
# 推荐：使用环境变量（避免命令行暴露凭证）
export WECHAT_APP_ID="wx_your_app_id"
export WECHAT_APP_SECRET="your_app_secret"

wechat-pub account add \
  --name "我的公众号" \
  --default
```

### 3. 测试发布

```bash
# 创建测试文章
cat > test.md << 'EOF'
---
title: 测试文章
---
# Hello World
这是一篇测试文章。
EOF

# 发布
wechat-pub publish create --file test.md --theme default
```

## 🎯 使用方式

### 在 OpenClaw 对话中使用

**示例 1：发布文章**

```
用户: 帮我把这篇文章发布到微信公众号

[提供 Markdown 内容]

AI: 好的，我来帮你发布。正在使用 orangeheart 主题...
✓ 文章已成功发布！发布 ID: 2247483647_1
```

**示例 2：创建草稿**

```
用户: 先创建一个草稿，不要立即发布

AI: 明白，我会先创建草稿。
✓ 草稿创建成功，Media ID: 3_abc123
你可以在微信公众平台查看和编辑。
```

**示例 3：查看文章列表**

```
用户: 查看我已发布的微信文章

AI: 正在获取列表...
共 8 篇已发布文章：
1. 最新文章 (2026-03-19)
2. 产品介绍 (2026-03-18)
...
```

### 手动调用 Skill

```bash
# 使用 OpenClaw 命令
openclaw run wechat-md-publisher publish article.md orangeheart

# 或直接使用工具
wechat-pub publish create --file article.md --theme orangeheart
```

## � 与 news-to-markdown-skill 组合使用

**推荐组合**：一键转载新闻到微信公众号

### 快速示例

```bash
# 1. 提取新闻文章
convert-url --url "https://www.toutiao.com/article/123" \
  --output /tmp/article.md \
  --platform toutiao

# 2. 发布到微信公众号
wechat-pub publish create \
  --file /tmp/article.md \
  --theme orangeheart
```

### AI 自动化工作流

用户说：
> "帮我把这篇头条文章转载到我的微信公众号"

AI 自动执行（**默认走"草稿优先 + 人工确认"路径**）：
1. 使用 `news-to-markdown-skill` 提取文章
2. 使用 `wechat-md-publisher-skill` **创建草稿**（`draft create`），并向用户回报标题、主题、图片处理结果
3. 等待用户明确确认后，再使用 `publish create` / `publish submit` 正式发布
4. 返回发布结果

> ⚠️ **不要在没有用户明确确认的情况下直接发布**。错误的文章、主题或抓取结果一旦 `publish create` 即对粉丝可见，可能产生公众号违规、品牌或合规风险。AI 应默认创建草稿，由用户在微信公众平台后台或预览中复核后再决定是否发布或删除。

### 优势

✅ **智能提取** - 自动识别正文，过滤广告  
✅ **多平台支持** - 头条、微信、小红书  
✅ **精美渲染** - 8+ 主题可选  
✅ **一键发布** - 无需手动复制粘贴

详见 [SKILL.md](./SKILL.md) 中的完整集成指南。

---

## �📚 文档

- **[SKILL.md](./SKILL.md)** - 完整的 SOP 和使用指南（含 news-to-markdown 集成）
- **[quick-start.md](./references/quick-start.md)** - 5 分钟快速上手
- **[themes.md](./references/themes.md)** - 主题使用指南
- **[ip-whitelist-guide.md](./references/ip-whitelist-guide.md)** - IP 白名单配置指南 ⚠️ 重要

## 🎨 可用主题

- `default` - 简洁经典
- `orangeheart` - 温暖优雅 ⭐ 推荐
- `rainbow` - 活泼清爽
- `lapis` - 清新极简 ⭐ 推荐
- `pie` - 现代锐利
- `maize` - 柔和舒适
- `purple` - 简约文艺
- `phycat` - 薄荷清新
- `sport` - 运动风 🏃 活力动感

## 🔧 高级配置

### 环境变量（可选）

```bash
# 在 ~/.bashrc 或 ~/.zshrc 中添加
export WECHAT_APP_ID="wx_your_app_id"
export WECHAT_APP_SECRET="your_app_secret"
```

### 自定义主题

```bash
# 添加本地主题（推荐）
wechat-pub theme add-local --name my-theme --path ./my-theme.css

# 添加远程主题 API（⚠️ 见下方安全警告）
wechat-pub theme add-remote --name md2wechat --url https://api.md2wechat.cn --key xxx
```

> ⚠️ **远程主题安全警告**：
> - 使用 `theme add-remote` 会把文章正文 / 标题 / 图片 URL 等内容发送到第三方端点，构成一个**新的数据边界**，超出本 Skill 默认（仅微信官方 API）的网络权限范围。
> - 默认请使用内置主题（`default` / `orangesun` / `redruby` / `greenmint` / `purplerain` / `blackink`）或本地 CSS 主题（`theme add-local`），无需任何外发请求。
> - 仅在你完全信任并已审计目标主题服务的隐私与安全策略时再使用 `theme add-remote`；不要把生产公众号的文章正文发送给来源不明的渲染服务。
> - AI 自动化场景下，不应自动启用远程主题；必须由用户明确配置并承担风险。

## ⚠️ 常见问题

### 问题 1：Skill 未被识别

**解决**：
```bash
openclaw skills refresh
openclaw skills info wechat-md-publisher
```

### 问题 2：权限错误

**解决**：
```bash
chmod +x ~/.openclaw/skills/wechat-md-publisher/scripts/publish.js
```

### 问题 3：找不到命令

**解决**：确认底层 npm 包已用**精确版本**全局安装：
```bash
npm install -g wechat-md-publisher@1.0.7
wechat-pub --version
```

### 问题 4：Token 过期

Token 会自动刷新，如仍有问题：
```bash
wechat-pub account remove <account-id>
wechat-pub account add --name "新账号" --default
```

### 问题 5：升级到新版本

本 Skill 不会自动升级底层包。**升级流程必须显式**：

1. 重新审计上游变更（CLI 入口与 `account.ts` 凭证加密）。
2. 在 `config.json` 与 `scripts/run.js` 中将 `REQUIRED_VERSION` 显式改为新的精确版本号（不要使用 caret/range/`@latest`）。
3. 在受信主机上执行精确安装并验证：

```bash
# 将 <NEW_VERSION> 替换为新审计通过的版本号
npm install -g wechat-md-publisher@<NEW_VERSION>
wechat-pub --version
```

> 启动器会在 `import` 前比对 `manifest.version` 与 `REQUIRED_VERSION`；如果两者不一致，调用会被拒绝。这是有意为之，避免静默吞下未经审计的新版本。

## 🔒 安全性

### 权限要求

- ✅ 读取本地 Markdown 和图片文件
- ✅ 网络访问（微信官方 API）
- ✅ 写入配置文件到 `~/.config/wechat-md-publisher-nodejs/`
- ⚠️ 可选：远程主题 API（仅当用户使用 `theme add-remote` 时）

### 数据隐私与最佳实践

- ✅ 默认情况下，所有通信仅限于微信官方 API（`api.weixin.qq.com` / `mp.weixin.qq.com`）。
- ✅ 配置与凭证存储在本地 `~/.config/wechat-md-publisher-nodejs/`；凭证加密由 [wechat-md-publisher](https://github.com/sipingme/wechat-md-publisher) npm 包处理（请审计 `src/services/account.ts` 后再写入真实 `AppSecret`）。
- ✅ **推荐使用环境变量** 传递 `WECHAT_APP_ID` / `WECHAT_APP_SECRET`，避免凭证出现在 `ps` 进程列表、shell history、CI 日志中。
- ✅ **推荐使用最小权限或测试公众号**，先验证流程后再切换到生产账号。
- ✅ **AI 自动发布默认走草稿路径**：让 AI 调用 `draft create`，由人工在公众平台预览/确认后再决定 `publish create` 或 `publish submit`。
- ❌ 本 Skill 不会自动收集用户信息或回传任何文章内容。
- ⚠️ **例外**：如果用户主动配置了远程主题（`theme add-remote`），会把文章正文发送到该第三方端点。请见上文"远程主题安全警告"。

### 安全检查

```bash
# 使用 skill-vetter 检查（如果可用）
openclaw skills vet wechat-md-publisher
```

## 📊 Skill 评分

根据 OpenClaw 社区标准：

- ✅ **规范清晰度**: 5/5 - SKILL.md 结构完整
- ✅ **首次成功时间**: 5/5 - 5 分钟内可完成
- ✅ **实用性**: 5/5 - 解决实际发布需求
- ✅ **安全性**: 5/5 - 权限合理，无恶意代码

## 🤝 贡献

欢迎贡献！

- 报告问题：[GitHub Issues](https://github.com/sipingme/wechat-md-publisher/issues)
- 提交改进：[Pull Requests](https://github.com/sipingme/wechat-md-publisher/pulls)
- 讨论交流：[GitHub Discussions](https://github.com/sipingme/wechat-md-publisher/discussions)

## 📜 许可证

Apache-2.0 License

## 👤 作者

**Ping Si** <sipingme@gmail.com>

- GitHub: [@sipingme](https://github.com/sipingme)
- 项目主页: [wechat-md-publisher](https://github.com/sipingme/wechat-md-publisher)

## 🙏 致谢

- [@wenyan-md/core](https://github.com/caol64/wenyan-core) - 提供精美主题和渲染引擎
- OpenClaw 社区 - 提供优秀的 AI Agent 框架

---

**让 AI 能够直接发布内容到微信公众号！** 🚀
