---
name: web-automation-suite
version: 1.0.0
description: >
  网页自动化套件 - 整合爬虫+浏览器自动化+定时任务。
  功能：Chrome CDP连接封装、网页操作（点击/输入/滚动/截图）、数据抓取模板、表单自动填写、定时监控任务。
  触发场景：自动抓取网页、自动化填表、批量发布内容、数据监控、定时任务执行。
---

# Web Automation Suite - 网页自动化套件

> 整合爬虫 + 浏览器自动化 + 定时任务，一套搞定所有网页自动化需求。

## 核心能力

| 功能 | 说明 |
|------|------|
| 🌐 Chrome CDP连接 | 远程调试模式稳定连接，自动重连 |
| 🖱️ 元素操作 | 点击、输入、滚动、拖拽、悬停 |
| 📸 截图取证 | 页面快照、全页截图、元素截图 |
| 📊 数据抓取 | 文本、链接、图片、表格、JSON |
| 📝 表单填写 | 批量填充、自动提交 |
| ⏰ 定时任务 | Cron式定时执行监控任务 |
| 🔄 状态管理 | 保存/加载登录状态，多账号切换 |

## Chrome远程调试连接

### 启动Chrome调试模式
```bash
chrome.exe --remote-debugging-port=9222
```

### 获取WebSocket URL（必须）
```javascript
const http = require('http');
const wsUrl = await new Promise((resolve, reject) => {
  http.get('http://localhost:9222/json/version', res => {
    let data = '';
    res.on('data', c => data += c);
    res.on('end', () => resolve(JSON.parse(data).webSocketDebuggerUrl));
  }).on('error', reject);
});
```

### 连接浏览器
```javascript
const { chromium } = require('playwright');
const browser = await chromium.connectOverCDP(wsUrl);
```

## 工作流程

```
1. 启动Chrome调试模式（用户执行）
2. 获取WebSocket URL
3. 连接CDP
4. 创建页面
5. 执行操作（导航/点击/输入/截图）
6. 提取数据
7. 保存状态（如需要）
8. 关闭连接
```

## 常用操作

### 打开网页
```javascript
await page.goto('https://example.com', {
  waitUntil: 'networkidle',
  timeout: 30000
});
```

### 点击元素
```javascript
await page.click('#submit-button');
await page.click('button:has-text("登录")');
```

### 输入文本
```javascript
await page.fill('input[name="username"]', 'your_text');
await page.type('textarea', 'content here', { delay: 100 });
```

### 滚动页面
```javascript
await page.evaluate(() => window.scrollBy(0, 500));
await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
```

### 截图
```javascript
// 普通截图
await page.screenshot({ path: 'screenshot.png' });
// 全页截图
await page.screenshot({ path: 'fullpage.png', fullPage: true });
```

### 提取数据
```javascript
// 提取所有链接
const links = await page.evaluate(() =>
  Array.from(document.querySelectorAll('a'))
    .map(a => ({ text: a.innerText, href: a.href }))
);

// 提取表格数据
const tableData = await page.evaluate(() => {
  const rows = document.querySelectorAll('table tr');
  return Array.from(rows).map(row =>
    Array.from(row.querySelectorAll('td')).map(td => td.innerText)
  );
});

// 提取JSON数据
const data = await page.evaluate(() => {
  const el = document.querySelector('script#__NEXT_DATA__');
  return el ? JSON.parse(el.textContent) : null;
});
```

### 等待元素
```javascript
await page.waitForSelector('#content', { timeout: 5000 });
await page.waitForLoadState('networkidle');
```

### 表单填写
```javascript
const formData = {
  'input[name="username"]': 'user123',
  'input[name="password"]': 'pass123',
  'select[name="country"]': 'CN',
  'textarea': '内容文本'
};

for (const [selector, value] of Object.entries(formData)) {
  await page.fill(selector, value);
  await page.waitForTimeout(100);
}

await page.click('button[type="submit"]');
```

## 数据抓取模板

### 列表页抓取
```javascript
async function scrapeListPage(page, itemSelector) {
  await page.waitForLoadState('networkidle');
  return await page.evaluate((selector) => {
    const items = document.querySelectorAll(selector);
    return Array.from(items).map(item => ({
      title: item.querySelector('h2, h3, .title')?.innerText || '',
      link: item.querySelector('a')?.href || '',
      price: item.querySelector('.price')?.innerText || '',
      desc: item.querySelector('.desc, p')?.innerText || ''
    }));
  }, itemSelector);
}
```

### 分页抓取
```javascript
async function scrapeWithPagination(page, baseUrl, maxPages = 5) {
  const results = [];
  for (let i = 1; i <= maxPages; i++) {
    await page.goto(`${baseUrl}?page=${i}`);
    await page.waitForLoadState('networkidle');
    const data = await scrapeListPage(page, '.item');
    results.push(...data);
    if (await page.$('.next-page:disabled')) break;
    await page.click('.next-page');
    await page.waitForTimeout(1000);
  }
  return results;
}
```

### 动态内容抓取（滚动加载）
```javascript
async function scrapeInfiniteScroll(page, itemSelector) {
  await page.waitForLoadState('networkidle');
  let lastHeight = 0;
  const results = new Set();

  while (true) {
    const items = await page.$$eval(itemSelector, els =>
      els.map(el => el.href || el.src || el.innerText)
    );
    items.forEach(i => results.add(i));

    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForTimeout(1000);

    const newHeight = await page.evaluate(() => document.body.scrollHeight);
    if (newHeight === lastHeight) break;
    lastHeight = newHeight;
  }
  return Array.from(results);
}
```

## 定时任务

### 创建定时任务脚本
```javascript
// scripts/scheduled-task.js
const { chromium } = require('playwright');
const fs = require('fs');

async function runTask() {
  const wsUrl = await getChromeWSUrl();
  const browser = await chromium.connectOverCDP(wsUrl);
  const page = await browser.newPage();

  try {
    await page.goto('https://example.com/prices');
    await page.waitForLoadState('networkidle');
    const data = await page.evaluate(() => ({
      price: document.querySelector('.price')?.innerText,
      timestamp: new Date().toISOString()
    }));

    const logFile = 'price_log.json';
    const logs = fs.existsSync(logFile)
      ? JSON.parse(fs.readFileSync(logFile, 'utf8'))
      : [];
    logs.push(data);
    fs.writeFileSync(logFile, JSON.stringify(logs, null, 2));
    console.log('Task completed:', data);
  } finally {
    await browser.close();
  }
}

runTask().catch(console.error);
```

### Cron表达式
- `0 * * * *` - 每小时
- `0 9 * * *` - 每天上午9点
- `*/15 * * * *` - 每15分钟

## 状态管理

### 保存登录状态
```javascript
const statePath = './browser-state.json';
await page.context().storageState({ path: statePath });
console.log('State saved to', statePath);
```

### 加载登录状态
```javascript
const browser = await chromium.launch({ headless: false });
const context = await browser.newContext({
  storageState: './browser-state.json'
});
const page = await context.newPage();
```

## 使用场景

- **数据采集**：商品信息、股票数据、新闻内容
- **内容监控**：竞品动态、价格变化、内容更新
- **自动化测试**：网页功能测试、表单验证
- **批量操作**：批量发帖、批量填表、批量下载
- **定时任务**：定期抓取、定期监控、定期提交

## 注意事项

1. **必须先启动Chrome调试模式**：`chrome.exe --remote-debugging-port=9222`
2. **禁止关闭Chrome** - 自动化期间保持Chrome运行
3. **等待页面加载** - 操作前等待 networkidle
4. **复用连接** - 不要频繁断开重连
5. **反爬策略** - 可用 `--disable-blink-features=AutomationControlled` 减少检测

## 错误处理

| 错误 | 解决方法 |
|------|---------|
| WebSocket 404 | Chrome调试端口未启动 |
| Timeout | 增加等待时间或检查网络 |
| Element not found | 等待元素出现或检查选择器 |
| Blocked | 使用隐身上下文或更换User-Agent |

## 应用示例

### 抓取股票价格
```javascript
await page.goto('https://finance.yahoo.com/quote/AAPL');
await page.waitForLoadState('networkidle');
const price = await page.textContent('[data-testid="qsp-price"]');
console.log('AAPL Price:', price);
```

### 定时监控价格
```javascript
// 保存为 scripts/monitor-price.js
const { chromium } = require('playwright');
const http = require('http');

async function getWSUrl() {
  return new Promise((resolve, reject) => {
    http.get('http://localhost:9222/json/version', res => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => resolve(JSON.parse(data).webSocketDebuggerUrl));
    }).on('error', reject);
  });
}

async function monitor() {
  const browser = await chromium.connectOverCDP(await getWSUrl());
  const page = await browser.newPage();
  await page.goto('https://example.com/product');
  const price = await page.textContent('.price');
  console.log(`[${new Date()}] Price: ${price}`);
  await browser.close();
}

setInterval(monitor, 300000); // 每5分钟执行
monitor();
```

---
