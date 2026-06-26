# Web Automation Suite - 网页自动化套件

## 🚀 快速开始

```bash
# 1. 进入scripts目录
cd scripts

# 2. 安装依赖
npm install playwright

# 3. 启动Chrome远程调试
chrome.exe --remote-debugging-port=9222

# 4. 运行示例
node cdp-connect.js
```

## 目录结构

```
web-automation-suite/
├── SKILL.md              # 本文档
├── scripts/
│   ├── cdp-connect.js       # Chrome CDP连接
│   ├── form-automation.js   # 表单自动化
│   ├── scheduled-task.js     # 定时任务
│   └── scraper-helpers.js   # 爬虫辅助
└── README.md             # 本文件
```

## 主要模块

### cdp-connect.js
```javascript
const { getChromeWSUrl, connectToChrome, createBrowserContext } = require('./cdp-connect.js');

// 获取WebSocket URL
const wsUrl = await getChromeWSUrl();

// 连接Chrome
const browser = await connectToChrome();

// 创建浏览器上下文
const { browser, context, page } = await createBrowserContext();
```

### form-automation.js
```javascript
const { fillForm, submitForm, batchPost } = require('./form-automation.js');

// 填充表单
await fillForm(page, {
  'input[name="username"]': 'user',
  'input[name="password"]': 'pass'
});

// 提交表单
await submitForm(page, 'button[type="submit"]');
```

## 依赖安装

```bash
npm install playwright
```

确保Chrome已开启远程调试：
```bash
chrome.exe --remote-debugging-port=9222
```
