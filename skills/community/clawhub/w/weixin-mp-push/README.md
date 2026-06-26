# 微信公众号图文生成与推送技能

[ClawHub](https://clawhub.ai/skills/weixin-mp-push)

支持通过AI生成符合公众号规范的图文（文章和贴图），并推送到公众号草稿箱，兼容其它SKILL生成的图文、图片进行推送。通过配置向导扫码授权，支持多账号。无需泄露公众号Secret密钥，无需配置公众号IP白名单。

## ✨ 功能特性

- 🔒 **扫码授权** - 通过配置向导扫码授权，支持多账号。无需泄露公众号Secret密钥，无需配置公众号IP白名单
- 📝 **图文生成** - 按照 design.md 规范生成标准的 HTML 文件，会自动适配公众号格式，去除AI味道
- 🚀 **一键推送** - 支持 HTML 与图片链接两种推送方式，推送成功后有服务通知

## 📥 安装

在 AI 对话中发送技能链接，或在终端执行以下命令，安装后即可使用本技能：

- **链接安装**：发送 [https://clawhub.ai/lihengdao/weixin-mp-push](https://clawhub.ai/lihengdao/weixin-mp-push) 给 AI
- **命令行安装**：

```bash
npx skills add lihengdao/weixin-mp-push
```

## 📦 快速开始

### 1. 配置公众号

用户访问配置向导完成公众号配置:

```
https://app.pcloud.ac.cn/design/weixin-mp-push.html
```

1. 用户微信扫码
2. 选择要推送的公众号
3. 复制生成的配置文件发给AI

### 2. 保存配置

AI将用户发送的配置保存到技能目录下的 `config.json` 文件中。

### 3. 写公众号图文

1. 用户发送图文创作要求给AI，AI必须根据 `design.md` 规范生成标准的 HTML 文件。若涉及到文本文章内容生成，AI必须根据 `Humanizer-zh.md` 规范生成文本文章内容，用于去除AI味道。有二种创作类型：
  - **文章**：通用类型，页面默认宽度 677px
  - **贴图**：图文卡片类型（俗称小绿书，类似小红书），页面默认宽度 375px，固定分页比例（默认 3:4）。推送到公众号时， 后台会自动把 HTML 内容转换为图片

2. 生成HTML文件后，若页面中没有引用图片，则需继续使用 `design_cover.md` 规范根据HTML文件的title生成对应的封面HTML文件 

**⚠️ 注意：** 不管是创作 **文章** 还是 **贴图** ，必须先阅读 `design.md`，按其规范生成标准的 HTML 文件。生成主HTML遵循 `design.md` 文件规范，生成封面HTML遵循 `design_cover.md` 文件规范。后续在推送图文过程中，标准的 HTML 会自动适配公众号格式

### 4. 推送到公众号

推送方式：`html` 模式传入生成的 HTML 文件（本技能在第三步生成的主HTML，请不要传入封面HTML，封面HTML会自动通过脚本随主HTML推送。也可以是用户或其它技能提供的HTML，非HTML内容可先按 `design.md` 整理成 HTML）；`img` 模式传入公网可访问的图片 URL 数组及标题、正文。**注意** 此模式仅适合用户或其它技能保证所提供的图片可以直接推送，无需本技能基于提供的内容进行创作

#### 推送 HTML

AI 调用脚本：首参为目标公众号 AppID，第二参为 `html`，再传与脚本同目录下的 HTML 文件名：

```bash
cd weixin-mp-push
node push-to-wechat-mp.js targetAppId html 你的文件.html
```

#### 推送图片链接

AI 调用脚本：首参为目标公众号 AppID，第二参为 `img`，第三参为**图片链接的 JSON 数组字符串**（整段一个参数；Bash 与 PowerShell 都可用单引号包住整段 JSON，例如 `'["https://...","https://..."]'`）。再依次传标题、正文。

```bash
cd weixin-mp-push
node push-to-wechat-mp.js targetAppId img '["https://cdn.example.com/1.png","https://cdn.example.com/2.png"]' "标题" "正文"
```

**标题、正文**（命令行各一个参数，含空格时用英文双引号）：标题和正文可为空。

#### 说明

**目标公众号 AppID**：若用户未声明具体要发送的公众号，则选择 `config.json` 中 `accounts` 中 `selected: true` 的账号。

### 其它功能

#### 清空草稿箱 

发送 POST 请求，`https://api.pcloud.ac.cn/openClawService`，传参数：

```json
{
  "action": "cleanupDrafts",
  "openId": "",
  "appId": ""
}
```
- **超时说明**：草稿箱图文可能较多，若返回「超时」可视为已成功；请用户看在公众号中查看草稿箱情况。

## 📖 详细文档

- **SKILL.md** - 完整技能说明
- **design.md** - HTML格式规范
- **config.example.json** - 配置字段说明与示例

## 🎯 使用场景

- 📰 日常公众号图文创作
- 🤖 兼容搭配其它SKILL使用
- 🗓️ 定期内容推送自动化

## 🔧 配置说明

配置文件 `config.json` 包含以下关键字段:

- `openId` - 微信用户 openId（必填）
- `accounts` - 账号列表（必填）：选平台提供时仅一项平台账号；选自己的公众号时仅为已授权自定义账号列表。

## 🚨 注意事项

- 如需推送到自己的公众号，请授权自己的公众号，不要使用平台提供的公众号
- 推送前请确保运行了配置向导并复制发给了AI
- 推送公众号图文链路较长（转换、平台接口、异步任务等），若返回「超时」可视为成功，无需重复推送，请用户关注微信服务通知或草稿箱

## 📄 许可证

MIT - 免费使用、修改和分发，无需署名

## 🔗 相关链接

- [ClawHub 技能页面](https://clawhub.ai/skills/weixin-mp-push)
- [OpenClaw 官方文档](https://docs.openclaw.ai)

## 👨‍💻 维护者

[@lihengdao](https://clawhub.ai/users/lihengdao)

---

**需要帮助?** 查看 SKILL.md 获取详细使用说明。