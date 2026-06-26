---
name: web-automation-helper
description: 浏览器自动化助手。通过Chrome远程调试模式，自动化执行网页操作，包括数据抓取、表单填写、内容发布、截图等。
---

# Web Automation Helper - 浏览器自动化助手

## 快速开始

```bash
# 1. 启动Chrome远程调试
chrome.exe --remote-debugging-port=9222

# 2. 运行示例
cd scripts
node cdp-helper.js --url https://example.com
```

## 目录结构

```
web-automation-helper/
├── SKILL.md
├── README.md
├── scripts/
│   └── cdp-helper.js
```

## 主要功能

- 网页截图
- 数据抓取
- 表单填写
