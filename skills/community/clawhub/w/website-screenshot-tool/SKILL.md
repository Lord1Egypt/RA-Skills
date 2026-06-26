---
name: website-screenshot-tool
description: Website Screenshot Automation Tool - 网站截图自动化，支持响应式截图、批量处理、定时调度、视觉对比 | Automated website screenshots with responsive capture, batch processing, scheduling, visual comparison
metadata:
  openclaw:
    requires:
      bins: ["python3"]
    install:
      - id: python-deps
        kind: python
        requirements: "requirements.txt"
---

# Website Screenshot Tool

## 功能

- **Capture** — 单页截图，支持全页面/视口截图
- **Batch** — 批量截图多个URL
- **Responsive** — 模拟多设备尺寸（Desktop/Tablet/Mobile）
- **Compare** — 两个网页视觉差异对比
- **Schedule** — 定时截图任务调度
- **History** — 截图历史记录与导出

## 使用

```python
from scripts.website_screenshot import WebsiteScreenshot, ScreenshotScheduler

tool = WebsiteScreenshot(output_dir="screenshots")

# 单页截图
result = tool.capture("https://example.com", full_page=True)

# 响应式截图（桌面/平板/手机）
results = tool.capture_responsive("https://example.com")

# 批量截图
results = tool.capture_batch(["https://site1.com", "https://site2.com"])

# 对比两个网页
diff = tool.compare("https://site.com/v1", "https://site.com/v2")

# 定时截图
scheduler = ScreenshotScheduler(tool)
scheduler.add_job("https://example.com", interval_minutes=60)
```

## CLI

```bash
python3 scripts/website_screenshot.py
```
