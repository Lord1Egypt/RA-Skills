# 网页截屏技能

此技能用于对指定网页进行截屏操作。

### 工具需求
- 支持网页截屏的工具，如 [Puppeteer](https://pptr.dev/) 等。

### 安装步骤
1. 确保你已经安装了 Node.js 和 npm。
2. 在项目目录下运行 `npm install puppeteer` 来安装 Puppeteer。

### 使用方法
当接收到用户截取网页图片的请求时，调用 Puppeteer 对指定网页地址进行截屏。以下是一个简单的示例代码：
```javascript
const puppeteer = require(puppeteer);

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto(https://example.com);
  await page.screenshot({path: screenshot.png});
  await browser.close();
})();
```

