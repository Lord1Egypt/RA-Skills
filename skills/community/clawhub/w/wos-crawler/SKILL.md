---
name: wos-literature-toolkit
version: 1.0.0
description: |
  WOS 文献一站式工具：Web of Science 检索爬取 + PDF 批量下载，全部在同一个 Web 界面完成。
  基于 Selenium 爬取 WOS 文献列表，导出 Excel 后自动调用多渠道 PDF 下载器（Sci-Hub/CORE/S2 OA/OpenAlex/Unpaywall/Publisher）。
  This skill should be used when the user wants to search and download academic papers from WOS, or mentions "WOS", "Web of Science", "文献检索下载", "论文下载", "WOS爬虫".
tags: [wos, pdf, academic, paper, download, scihub, crawler, literature]
---

# WOS Literature Toolkit

WOS 文献一站式解决方案：从 Web of Science 检索爬取到 PDF 批量下载，全部在同一个 Web 界面完成。

## 功能概览

**Phase 1 - WOS Crawl:**
- 自然语言检索词自动转换为 WOS 高级检索式
- 支持关键词/作者/标题/DOI/期刊/年份/文献类型多维度检索
- 期刊过滤：内置 40+ 预设期刊，支持精确/模糊匹配
- 自动分页爬取、结果去重
- 自动导出 Excel（标题、作者、期刊、DOI、被引频次、摘要等）

**Phase 2 - PDF Download:**
- 自动使用 Phase 1 爬取的 Excel，一键启动 PDF 下载
- 也支持手动上传任意 Excel 文件
- 6 个免费下载渠道按优先级依次尝试
- 实时进度 + 下载统计 + 渠道分布 + 日志
- 自定义输出目录

**下载渠道优先级:** Sci-Hub (CDN + 爬取) -> Semantic Scholar OA -> CORE -> Unpaywall -> OpenAlex -> Publisher Direct

## 使用方式

```bash
python {SKILL_DIR}/scripts/web_ui.py
```

启动后自动打开 http://localhost:5678

### 工作流程

1. 打开 Web UI，在 **WOS Crawl** 标签页填写检索条件
2. 点击 **Start WOS Crawl**，浏览器自动打开 WOS 并开始爬取
3. 爬取完成后自动导出 Excel，点击 **Download PDFs** 按钮切换到下载标签
4. 在 **PDF Download** 标签页确认设置，点击开始下载
5. 下载完成后点击 **Open PDF Folder** 查看所有 PDF 文件

### 也可以跳过爬取直接下载

如果已有 WOS 导出的 Excel 文件：
1. 切换到 **PDF Download** 标签页
2. 在 **Option B** 区域上传 Excel 文件
3. 选择输出目录，点击开始下载

## 前置条件

- Python 3.7+
- 依赖: `pip install selenium pandas openpyxl flask requests`
- Edge 浏览器（WOS 爬取需要）
- WOS 机构订阅或登录账号

## Agent 使用指南

当用户需要从 WOS 检索并下载文献 PDF 时：

1. 启动 Web UI: `python {SKILL_DIR}/scripts/web_ui.py`
2. 引导用户在浏览器中填写检索条件
3. WOS 爬取需要用户登录机构账号（首次运行时浏览器会自动打开 WOS 页面）
4. 爬取完成后引导用户点击 "Download PDFs" 按钮
5. 下载完成后帮助用户打开输出文件夹查看结果

## 关键注意事项

- WOS 爬取需要机构订阅或已登录 WOS 账号
- Sci-Hub 渠道需要网络能访问（部分网络环境可能不可用）
- Cookie 持久化：首次登录 WOS 后会自动保存 Cookie，后续无需重复登录
- 已下载的 PDF 会被自动跳过（断点续传）
