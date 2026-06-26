---
name: wechat-md-publish
description: "将 Markdown 文章发布到微信公众号。支持 AI 生成封面图片、HTML 卡片渲染、创建草稿、可选自动发布。当用户说'发公众号'、'发布文章到微信'、'公众号发布'时使用此技能。"
description_zh: "Markdown 文章发布到微信公众号（AI 生成封面、内联样式排版、HTML 卡片渲染、创建草稿、可选发布）"
description_en: "Publish Markdown articles to WeChat Official Account (AI cover, inline styles, HTML card, draft, optional publish)"
version: 0.3.0
allowed-tools: Bash,Read,DeferExecuteTool
metadata:
  clawdbot:
    emoji: "📢"
    requires:
      bins:
        - python
---

# 微信公众号文章发布

将 Markdown 文章发布到微信公众号，支持 AI 生成封面图片。

---

## 首次配置

### 1. 获取公众号 AppID 和 AppSecret

在 [微信公众平台](https://mp.weixin.qq.com/) → 开发 → 基本配置 中获取。

### 2. 设置 IP 白名单

在基本配置页面，将你的出口 IP 加入白名单。查看出口 IP：

```bash
curl -s https://ipinfo.io/ip
```

### 3. 创建配置文件

```bash
mkdir -p ~/.wechat_publish
cat > ~/.wechat_publish/config.json << 'EOF'
{
  "app_id": "你的AppID",
  "app_secret": "你的AppSecret"
}
EOF
```

### 4. 安装依赖

```bash
pip install requests markdown
```

如需使用 HTML 卡片渲染功能，额外安装：

```bash
pip install playwright
playwright install chromium
```

---

## 工作流程

当用户要求发布文章时，按以下步骤执行：

### 步骤 1：AI 总结摘要

阅读文章内容，用 AI 总结一段摘要，不超过 120 字节（中文约 40 字）。

### 步骤 2：判断封面来源

**如果用户已提供封面图片** → 直接使用，跳到步骤 4。

**如果用户未提供封面图片** → 进入步骤 3 用 AI 生成。

### 步骤 3：用 ImageGen 生成封面图片（仅当用户未提供封面时）

根据文章标题和内容，调用 ImageGen 工具生成封面。提示词参考：

```
微信公众号封面图，风格简约专业，比例 16:9，主题：{文章标题关键词}，不要出现文字
```

更多提示词模板见下方"AI 封面生成提示词建议"。

### 步骤 4：（可选）生成 HTML 卡片

如果文章需要插入排版精美的信息卡片（对比图、步骤说明、工具栈展示等），由 AI 生成 HTML 模板，脚本自动渲染为图片插入文章。

微信公众号对 HTML/CSS 支持有限，有些排版效果无法用内联样式实现。HTML 卡片通过 Playwright 将 HTML 渲染为图片，绕过这个限制。

常见卡片类型和 HTML 模板：

**对比卡片**：
```html
<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:system-ui,-apple-system,sans-serif;background:#f5f5f7;padding:30px 20px}
.title{font-size:22px;font-weight:bold;color:#1a1a1a;margin-bottom:20px;text-align:center}
.section{margin-bottom:16px;padding:12px 16px;border-radius:8px}
.green{background:#e8f5e9;border-left:4px solid #4CAF50}
.red{background:#fce4ec;border-left:4px solid #f44336}
.section-title{font-size:15px;font-weight:bold;margin-bottom:8px}
.item{font-size:14px;color:#333;margin-bottom:4px;line-height:1.6}
</style></head><body>
<div class="title">标题</div>
<div class="section green"><div class="section-title">✅ 能做的</div><div class="item">• 内容1</div></div>
<div class="section red"><div class="section-title">❌ 不能做的</div><div class="item">• 内容1</div></div>
</body></html>
```

保存为 `.html` 文件后通过 `--html-card` 参数传入。可同时传入多个卡片文件。

### 步骤 5：运行发布脚本

```bash
# 仅创建草稿
python scripts/wx_publish.py --title "文章标题" --content article.md --digest "AI总结的摘要" --thumb-image <封面图片路径>

# 带 HTML 卡片
python scripts/wx_publish.py --title "文章标题" --content article.md --digest "AI总结的摘要" --thumb-image <封面图片路径> --html-card card.html

# 多个 HTML 卡片
python scripts/wx_publish.py --title "文章标题" --content article.md --digest "AI总结的摘要" --thumb-image <封面图片路径> --html-card card1.html card2.html

# 创建草稿并自动发布
python scripts/wx_publish.py --title "文章标题" --content article.md --digest "AI总结的摘要" --thumb-image <封面图片路径> --publish
```

如果用户提供了封面素材 ID 而非图片文件：

```bash
python scripts/wx_publish.py --title "文章标题" --content article.md --thumb-media-id <素材ID>
```

---

## 完整参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--title` | 是 | 文章标题 |
| `--content` | 是 | Markdown 文件路径 |
| `--thumb-image` | 否 | 封面图片本地路径（AI 生成或用户提供的封面都用此参数） |
| `--thumb-media-id` | 否 | 已上传的封面素材 ID |
| `--html-card` | 否 | HTML 卡片文件路径（可多个），渲染为图片插入文章 |
| `--card-width` | 否 | HTML 卡片渲染宽度（默认 750px） |
| `--author` | 否 | 作者名 |
| `--digest` | 是 | 文章摘要（由 AI 总结，不超过 120 字节/约 40 字） |
| `--upload-thumb` | 否 | 仅上传封面图片，输出 thumb_media_id |
| `--publish` | 否 | 创建草稿后自动发布 |

封面优先级：`--thumb-media-id` > `--thumb-image`。均未指定时会提示提供。

---

## AI 封面生成提示词建议

根据文章类型选择合适的提示词：

| 文章类型 | 提示词模板 |
|---------|-----------|
| 技术教程 | 微信公众号封面，科技感，深蓝配色，简洁图标，无文字 |
| 财经分析 | 微信公众号封面，金融主题，数据图表元素，蓝金配色，无文字 |
| 生活分享 | 微信公众号封面，清新风格，柔和配色，简约图形，无文字 |
| 量化交易 | 微信公众号封面，K线图表元素，深色背景，科技金融感，无文字 |

---

## 常见问题

| 问题 | 解决方案 |
|------|---------|
| 获取 access_token 失败 | 检查 AppID/AppSecret 是否正确，IP 白名单是否已设置 |
| 上传封面失败 | 封面图片需小于 10MB，支持 bmp/png/jpeg/jpg/gif 格式 |
| 草稿创建失败 | 确认公众号已认证，具有草稿接口权限 |
| markdown 模块未找到 | 运行 `pip install markdown` |

---

## 注意事项

- 本工具仅适用于**已认证**的微信公众号（订阅号/服务号均可）
- access_token 有效期 2 小时，脚本自动缓存和刷新
- 文章中的本地图片会自动上传到微信并替换 URL
- 建议先创建草稿确认效果，再加 `--publish` 自动发布
- 用户已提供封面图片时，不要再用 ImageGen 生成
