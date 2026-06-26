---
name: rss-to-wechat
description: 将 RSS 文章转换为微信公众号格式。适用于：发布 RSS/博客文章到微信、格式化内容以符合微信 API、自动化微信内容发布。
---

# RSS to WeChat | RSS 转微信公众号

将 RSS 文章或任何网页内容转换为微信公众号兼容的 HTML 格式。

## 快速开始

```bash
# 检查配置和依赖
bash scripts/rss-to-wechat.sh --check

# 处理文章
bash scripts/rss-to-wechat.sh --url "https://example.com/article"

# 自动选择最新文章（需要 blogwatcher）
bash scripts/rss-to-wechat.sh --auto
```

## 配置

首次使用：

```bash
# 复制配置示例
cp references/config.example.sh config.local.sh

# 编辑配置
nano config.local.sh
```

最小配置：

```bash
WECHAT_APPID="你的AppID"
WECHAT_APPSECRET="你的AppSecret"
BRAND_NAME="你的品牌名称"
```

## 工作流程

1. **数据准备**（自动）
   - 脚本获取并解析文章
   - 提取标题、作者、内容
   - 保存为 JSON

2. **HTML 生成**（AI 辅助）
   - AI 助手生成微信兼容的 HTML
   - 使用品牌配置
   - 遵循严格的格式要求（见 `references/html-template.md`）

3. **封面生成**（可选）
   - 如果配置了 `COVER_SKILL`
   - 生成 1283×383 封面图

4. **发布**（可选）
   - 如果配置了微信凭证
   - 通过 API 上传到草稿箱

## 微信 HTML 格式要求

微信 API 对 HTML 格式有严格要求：

**必须使用：**
- `<section>` 和 `<p>` 标签（不用 `<div>`）
- 内联样式 `style="..."`
- `<strong>` 和 `<em>` 标签
- 完整 URL（不用相对链接）

**禁止使用：**
- `class` 或 `id` 属性
- 外部 CSS
- JavaScript
- 相对链接

详见 `references/html-template.md` 查看完整模板和示例。

## 脚本

所有脚本位于 `scripts/` 目录：

- `rss-to-wechat.sh` - 主入口
- `parse-article.sh` - 文章内容提取
- `format-wechat.sh` - HTML 格式化（已弃用，使用 AI 生成）
- `config.sh` - 默认配置
- `test.sh` - 依赖检查

## 参考文档

- `references/USER_GUIDE.md` - 完整用户文档
- `references/html-template.md` - 微信 HTML 模板和样式指南
- `references/config.example.sh` - 配置示例（包含所有选项）

## 依赖

**必需：**
- `curl` - HTTP 请求
- `jq` - JSON 处理
- `pandoc` - 格式转换

**可选：**
- `blogwatcher` - RSS 订阅管理（用于 --auto 模式）
- 自定义封面生成脚本
- 自定义发布脚本

## 配置选项

查看 `references/config.example.sh` 了解所有可用选项：

- RSS 源和过滤条件
- 品牌定制（名称、标语、颜色）
- 路径配置
- 外部工具集成
- 关键词过滤

## 故障排除

**错误 45166（invalid content）**
- 检查 HTML 格式是否符合要求
- 确保所有样式都是内联的
- 移除 class/id 属性
- 参考成功案例

**文章解析失败**
- 检查 URL 是否可访问
- 确认没有反爬虫措施
- 尝试手动提取内容

**配置问题**
- 运行 `bash scripts/rss-to-wechat.sh --check`
- 确认所有必需工具已安装
- 检查微信凭证

## 注意事项

- 此 skill 提供数据准备和指导
- AI 助手根据模板生成最终 HTML
- 手动 HTML 生成已弃用（因微信格式要求严格）
- 本地配置（`config.local.sh`）不会提交到 git
