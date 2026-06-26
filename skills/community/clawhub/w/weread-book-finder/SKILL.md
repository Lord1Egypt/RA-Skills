---
name: weread-book-finder
description: 输入图书名称，优先在微信读书搜索并加入书架；若微信读书没有可信命中或无法加入书架，则自动回退到 Z-Library 搜索并优先下载非 PDF 格式。适用于“把《xxx》加入微信读书书架，不行就去 Z-Library 下载”这类请求。
---

# WeRead Book Finder 自动化

使用 Playwright 脚本自动化处理书籍获取与回退下载。

## 前提

环境依赖：
- `python3`
- `playwright` (安装 Chromium：`playwright install chromium`)
- `requests`
- `beautifulsoup4`

## 快速使用

指定书名运行：

```bash
python3 skills/weread-book-finder/scripts/find_book.py "书名"
```

## 登录态管理

由于微信读书和 Z-Library 需要登录，建议固定使用 profile 目录，避免重复登录：

```bash
# 登录微信读书
python3 skills/weread-book-finder/scripts/find_book.py --login weread --headed

# 登录 Z-Library
python3 skills/weread-book-finder/scripts/find_book.py --login zlib --headed
```

后续运行脚本时，会自动复用已登录的浏览器会话。

## 推荐执行策略

- **默认模式**：直接运行脚本，脚本会自动尝试微信读书。若微信读书找不到，脚本会无缝切换至 Z-Library 搜索并下载。
- **严格标题优先**：优先精确标题；短标题若只有模糊命中，不会直接误加，而是返回候选后走后备链路。
- **作者辅助匹配**：支持输入 `书名 / 作者`、`书名 | 作者`、`书名 by 作者` 这类形式，脚本会把作者纳入排序。
- **候选结果可见**：输出里会附带前 5 个候选，便于调试和人工确认。
- **调试模式**：添加 `--headed` 参数可以打开浏览器窗口观察执行过程。
- **文件保存**：下载的电子书默认保存在 `~/Downloads/OpenClaw-Books`。
