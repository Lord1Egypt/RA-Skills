# 白名单领域配置

三件套闭环引擎在检测到重复任务后，会先检查是否被现有技能覆盖。以下是当前白名单：

| 领域关键词 | 覆盖技能 |
|-----------|---------|
| 邮箱/邮件 | himalaya, google-workspace |
| 信息图 | sn-infographic, baoyu-infographic, ai-daily-news |
| 日报 | ai-daily-news, ai-news-collector |
| 新闻 | ai-news-collector, ai-daily-news, ai-research-intelligence |
| 公众号 | wechat-article, wechat-publisher, wechat-official-account |
| 文章 | wechat-article, wechat-article-writer |
| 备份 | openclaw-backup |
| PDF | pdf, pdf-toolkit-pro, nano-pdf, minimax-pdf |
| PPT | pptx-generator, Powerpoint / PPTX, html-ppt, sn-ppt-entry |
| Excel | Excel / XLSX, minimax-xlsx, sn-da-excel-workflow |
| 文档 | doc-handler, Word / DOCX, minimax-docx |
| 图片 | sn-image-base, wan-image-video-gen-edit, comfyui |
| 视频 | seedance-video, wan-image-video-gen-edit, short-video-auto |
| 搜索 | web-tools-guide, firecrawl, tavily-search |
| 截图 | agent-browser |
| 技能 | darwin-skill, huashu-nuwa, skill-evolution-loop |
| 工作流 | workflow-engine |
| Notion | notion |
| GitHub | github, github-pr-workflow |
| 巡检 | self-evolution, kuro-health-check-system |
| 报告 | sn-deep-research, sn-research-report |
| 数据 | sn-da-excel-workflow, sn-da-large-file-analysis |

## 维护指南

当安装了新技能覆盖某个领域时，更新 `engine.py` 中的 `EXISTING_SKILL_DOMAINS` 字典。

## 检测逻辑说明

引擎只认**AI实际执行过tool调用**的用户任务，忽略纯对话。具体判断：
- 扫描session `.jsonl` 文件
- 找 `role=user` 消息
- 检查后续 `role=assistant` 消息是否有 `tool_calls` 字段或包含 `terminal(`/`write_file(`/`browser_` 标记
- 只有确认有工具调用的用户消息才计入重复模式
