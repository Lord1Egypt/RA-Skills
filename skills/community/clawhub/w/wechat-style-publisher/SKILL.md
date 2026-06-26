---
name: wechat-style-publisher
description: 支持多账号微信公众号发布，提供自定义文章主题、文章开头/结尾模板。当用户需要将带样式的文章发布到一个或多个微信公众号时使用此工具。
---

当任务是将一篇文章发布到**一个或多个微信公众号**，并需要使用**账号独立凭据、主题化 HTML、以及可选的开头/结尾引导模板**时，请使用此技能。

## 主要入口

- Node.js 发布脚本：`{baseDir}/scripts/publish-node.mjs`
- Python 发布脚本：`{baseDir}/scripts/publish-python.py`
- 仅应用样式（Node.js）：`{baseDir}/scripts/apply-style.mjs`
- 模板导入工具：  
  - `{baseDir}/scripts/import-template-node.mjs`  
  - `{baseDir}/scripts/import-template-python.py`
- 配置编辑器：`{baseDir}/scripts/set-config.mjs`

---

# 功能说明

- 将草稿文章发布到一个或多个已配置的微信公众号
- 支持通过 **账号 ID 列表** 或 **所有已启用账号**进行发布
- 支持内置主题以及自定义 CSS 覆盖
- 在文章正文前后自动插入 **intro / outro HTML 模板**
- 上传文章中的本地图片以及可选的封面图片
- 在 Node.js 流程中自动 **内联 CSS** 以兼容微信公众号
- 可从现有微信公众号文章 **HTML 文件或文章 URL** 中导入 intro/outro 模板和文章布局样式
- 将提取出的模板存储为 **命名变量**，方便后续复用
- 发布配置优先读取  
  `wechat.accounts.<accountId>.publishing`  
  若不存在则回退到顶层 `publishing`
- 支持兼容参数别名，例如  
  `--article-url`、`--link`、`--template-name`、`--template-registry`
- 支持 `--extract-mode ai`  
  用于保留更多候选内容与分析 JSON，以便 AI 进一步优化模板

---

# 输入内容

- **HTML 内容**  
  如果原始文章是 Markdown，需要先转换为 HTML。

- **多账号配置 JSON**  
  示例文件：  
  `{baseDir}/assets/config.example.json`

- **可选的文章开头/结尾模板**  
  示例文件：