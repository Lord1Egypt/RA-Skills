# wecom-drive-web

通过企业微信官方网页端操作微盘、在线文档和表格的实用 skill。

它适合这些场景：

- 检查企业微信网页端是否已登录
- 自动抓取登录二维码并发给用户
- 保持原登录会话，等待用户扫码或桌面端确认
- 打开企业微信文档、表格和微盘文件链接
- 使用网页原生能力导出 Excel 或 CSV
- 在本地处理导出的文件并生成 Word 报告
- 再通过网页端把结果文件导回企业微信微盘

## Core Capabilities

- Safe login handoff: detect login walls, capture the live QR code, and keep the same session open until the user finishes login.
- Native web export first: prefer the official export entry in WeCom Docs instead of scraping table cells when spreadsheets need offline analysis.
- Local processing workflow: download or export first, then analyze files locally for safer and more stable transformations.
- Round-trip delivery: upload generated `.docx`, `.xlsx`, or other artifacts back to `https://doc.weixin.qq.com/home/recent`.

## Included Scripts

- `scripts/wecom-drive-browser.mjs`
  - 检查登录状态
  - 提取二维码截图
  - 输出页面结构摘要
- `scripts/generate_stutter_report.py`
  - 读取导出的腾讯文档 `.xlsx`
  - 生成分析报告 `.html`
  - 生成 Word 报告 `.docx`

## Quick Start

安装依赖：

```bash
cd /path/to/wecom-drive-web
npm install
```

检查登录状态并生成二维码截图：

```bash
cd /path/to/wecom-drive-web
node ./scripts/wecom-drive-browser.mjs \
  --url "https://doc.weixin.qq.com/home/recent" \
  --qr-path "./.outputs/wecom-login-qr.png" \
  --keep-open
```

基于导出的 Excel 生成报告：

```bash
cd /path/to/wecom-drive-web
python3 ./scripts/generate_stutter_report.py "/path/to/exported.xlsx"
```

## Workflow Notes

1. 如果需要登录，先把二维码发给用户，再继续后续操作。
2. 不要在用户扫码前关闭当前登录页或重建新的登录会话。
3. 对表格分析任务，优先使用网页原生 `导出 -> 本地Excel表格 (.xlsx)`。
4. 大体量处理优先在本地完成，再把结果导回微盘。

## Packaging

发布前建议排除这些目录：

- `node_modules/`
- `.outputs/`
- `.state/`

本目录已经附带 `.gitignore`，可直接作为发布时的排除参考。
