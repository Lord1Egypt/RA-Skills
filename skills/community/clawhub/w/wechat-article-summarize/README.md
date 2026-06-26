# WeChat Article Summarize

这是一个用于整理微信公众号文章的 skill。

## 功能简介

- 读取一个或多个 `mp.weixin.qq.com` 文章链接
- 抽取文章正文、标题、发布时间，以及可选的图片链接
- 自动修复常见的微信正文乱码问题
- 调用 `summarize` 用中文总结全文内容
- 生成结构化 markdown 文件
  - 单篇文章整理
  - 多篇文章汇总 / 日报
- 支持按日期 + 标题，或日期 + 篇数 + 汇总说明命名
- 支持把文件保存到用户指定目录

## 使用前需要确认

在真正开始抓取文章之前，需要先确认：

1. `summarize` 已经配置好 API key，并且可正常使用
2. 是否需要在最终 markdown 中保留图片链接
3. 最终文件保存到哪个目录

## 主要脚本

- `scripts/read_wechat_article.py`：抓取微信文章基础内容
- `scripts/fix_wechat_body.py`：修复正文乱码
- `scripts/summarize_cn.py`：强制中文摘要并做语言校验
- `scripts/normalize_markdown_text.py`：整理段落和换行
- `scripts/build_mindmap_markdown.py`：生成单篇 markdown
- `scripts/build_batch_report.py`：生成多篇汇总日报
- `scripts/run_wechat_mindmap_workflow.py`：串联完整流程

## 适用场景

- 总结单篇微信文章
- 把多篇微信文章汇总成一份日报
- 输出适合继续阅读、归档或二次整理的 markdown 文件
