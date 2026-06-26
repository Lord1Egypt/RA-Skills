# Website Screenshot Tool

> 中英文双语 | Bilingual Documentation

---

## English

Automated website screenshot tool with responsive capture, batch processing, visual comparison, and scheduled monitoring.

### Features

- **Single Page Capture** — full page or viewport-only screenshots
- **Batch Processing** — capture multiple URLs in one run
- **Responsive Testing** — simulate Desktop (1920x1080), Tablet (768x1024), Mobile (375x812)
- **Visual Comparison** — compare two versions of a webpage
- **Scheduled Monitoring** — periodic screenshots with interval scheduling
- **History & Export** — track all captures with JSON export

### Quick Start

```python
from scripts.website_screenshot import WebsiteScreenshot

tool = WebsiteScreenshot(output_dir="my_screenshots")

# Basic capture
result = tool.capture("https://example.com")

# Full page
result = tool.capture("https://example.com", full_page=True)

# Responsive (creates 3 images)
results = tool.capture_responsive("https://example.com")
```

## 中文

网站截图自动化工具，支持响应式截图、批量处理、视觉对比和定时监控。

### 功能特性

- **单页截图** — 完整页面或仅视口截图
- **批量处理** — 一次性截取多个网址
- **响应式测试** — 模拟桌面 (1920x1080)、平板 (768x1024)、手机 (375x812)
- **视觉对比** — 对比网页的两个版本
- **定时监控** — 按间隔定期截图
- **历史与导出** — 追踪所有截图并导出JSON

### 快速开始

```python
from scripts.website_screenshot import WebsiteScreenshot

tool = WebsiteScreenshot(output_dir="my_screenshots")

# 基础截图
result = tool.capture("https://example.com")

# 完整页面
result = tool.capture("https://example.com", full_page=True)

# 响应式（生成3张图）
results = tool.capture_responsive("https://example.com")
```

### 安装依赖

```bash
pip install -r requirements.txt
# 安装 Playwright 浏览器:
playwright install chromium
```

### 运行测试

```bash
python3 -m pytest tests/ -v
```
