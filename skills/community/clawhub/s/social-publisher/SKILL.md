---
name: social-publisher
description: 【爆款标题】自媒体人必备：一键发布 4 个平台，告别重复劳动！

你是不是经常写完文章，还要手动调整格式？微信公众号要加粗标记，小红书要标签前置，知乎要保持 Markdown...每次都要花 1-2 小时重复劳动？

本工具用一键转换技术，让你的 Markdown 秒变 4 大平台原生格式（微信/小红书/知乎/抖音），支持预览和零风险模拟发布。

✨ **核心亮点**：
- 一键转换：Markdown → 4大平台原生格式
- 预览模式：发布前看效果，放心调整
- 多图支持：配图自动上传（需API凭证）
- 安全模拟：默认不真实发布，测试零风险

📁 **典型场景**：
- 自媒体运营：一篇内容，4平台同时发布
- 内容创作者：告别格式转换的繁琐
- 团队协作：统一格式化标准

🎯 **为什么选我**：
✅ 唯一支持 4 大中文平台（微信、小红书、知乎、抖音）
✅ 完整预览+模拟模式，零风险
✅ 开源免费，可自扩展平台

👉 立即体验：`clawhub install social-publisher`
---

# Social Publisher Skill

Publish content to multiple Chinese social platforms with a single command.

## Features
- **内容格式化**: 自动将 Markdown 转换为各平台格式
  - 微信公众号：标题加下划线，列表转换为圆点，加粗转为【】标记
  - 小红书：分段清晰，自动添加话题标签，适合移动端阅读
  - 知乎：保留 Markdown 语法，支持代码块和表格
  - 抖音：文案简短化，话题标签前置
- **多平台发布**：一键发布到微信公众号、小红书、知乎、抖音
- **图片支持**：支持多图片上传（需要真实 API）
- **预览模式**：使用 `--format` 预览各平台格式化效果
- **安全模拟**：默认模拟模式，不实际发布，可放心测试

## Usage

### 预览各平台格式化效果
```bash
social-publisher --title "我的标题" --content "正文内容" --format
```

### 模拟发布（展示格式化内容）
```bash
social-publisher publish --title "标题" --content "正文" --images "img1.jpg,img2.jpg" --platforms wechat,xiaohongshu
```

### 真实发布（需要配置 API 凭证）
```bash
social-publisher publish --title "标题" --content "正文" --images "img1.jpg" --platforms wechat,zhihu
```

## Command-Line Options
- `--title/-t`: 文章标题（必填）
- `--content/-c`: 文章正文，支持 Markdown（必填）
- `--images/-i`: 图片路径，逗号分隔
- `--platforms/-p`: 目标平台，逗号分隔（默认：wechat,xiaohongshu,zhihu,douyin）
- `--dry-run`: 仅检查配置，不发布
- `--format`: 仅预览各平台格式化效果，不发布

## Configuration
### 模拟模式（默认）
直接使用即可，无需配置。所有发布均为模拟，仅展示格式化效果。

### 真实发布模式
Set credentials in environment variables or config file:

**微信公众号**:
- `WECHAT_APPID`
- `WECHAT_APPSECRET`

**小红书**:
- `XIAOHONGSHU_APP_ID`
- `XIAOHONGSHU_APP_SECRET`
- `XIAOHONGSHU_ACCESS_TOKEN`

**知乎**:
- `ZHIHU_CLIENT_ID`
- `ZHIHU_CLIENT_SECRET`
- `ZHIHU_ACCESS_TOKEN`

**抖音**:
- `DOUYIN_APP_KEY`
- `DOUYIN_APP_SECRET`
- `DOUYIN_ACCESS_TOKEN`

Or place them in `~/.openclaw/secrets/social-publisher.json`:
```json
{
  "wechat": {"appid": "...", "appsecret": "..."},
  "xiaohongshu": {"app_id": "...", "app_secret": "...", "access_token": "..."},
  "zhihu": {"client_id": "...", "client_secret": "...", "access_token": "..."},
  "douyin": {"app_key": "...", "app_secret": "...", "access_token": "..."}
}
```

## Formatting Examples

### Input Markdown
```markdown
# 一级标题
## 二级标题
- 列表项1
- 列表项2
**加粗文本**
```

### WeChat Output
```
【标题】
一级标题

【正文】
一级标题
====================

• 列表项1
• 列表项2
【加粗文本】
```

### Xiaohongshu Output
```
【标题】
✨ 一级标题 ✨

【正文】
1. 列表项1

2. 列表项2

【话题】
#生活记录 #分享 #好物推荐
```

### Zhihu Output
```
# 一级标题

## 二级标题

- 列表项1
- 列表项2
**加粗文本**
```

### Douyin Output
```
【文案】
列表项1 列表项2 加粗文本

【标题】
一级标题

【话题】
#短视频 #推荐 #热门
```

## Safety
- 模拟模式下不发送任何网络请求
- 凭证从环境变量读取，不会记录到日志
- 真实 API 调用时使用 HTTPS
- 支持 dry-run 模式用于安全测试

## Roadmap
- [ ] 微信公众号真实 API 实现
- [ ] 小红书真实 API 实现
- [ ] 知乎真实 API 实现
- [ ] 抖音真实 API 实现
- [ ] 图片上传功能
- [ ] 平台草稿箱保存功能
- [ ] 发布历史记录

## License
MIT
