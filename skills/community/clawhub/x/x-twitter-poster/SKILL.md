---
name: x-twitter-poster
description: |
  X (Twitter) 发推 Skill。使用 Playwright 连接用户已登录的 Chrome 浏览器，自动填写并发送推文。
  
  适用场景：
  - 用户要求"发推"、"发一条推"、"发推文"、"发推特"
  - 用户要求"帮我发一条关于 XX 的推"
  - 用户要求"发一条推文，内容是..."
  
  核心能力：
  - 连接用户 Chrome 浏览器（CDP 模式）
  - 继承用户的登录状态
  - 跨平台支持：Mac (Meta+Enter) / Windows/Linux (Control+Enter)
  
  ⚠️ 安全要求：
  - 仅在信任代码时启用 CDP 端口
  - 建议使用单独 Chrome 账号测试
  - 可配置 X_USERNAME 环境变量
---

# X/Twitter 发推 Skill

## 从头讲起：为什么这个方法能成功

### 背景：X 的反爬虫机制

X (Twitter) 会检测自动化浏览器，主要通过：
1. **浏览器指纹**：navigator.webdriver、AutomationControlled 标志
2. **自动化特征**：Chrome 的自动化相关标志
3. **行为检测**：异常的浏览器行为模式

### 关键发现：复用用户真实浏览器

**核心思路**：不启动新的自动化浏览器，而是连接用户已经登录的真实 Chrome 浏览器。

**优势**：
- ✅ 用户已经登录，无需处理登录问题
- ✅ 真实浏览器指纹，无法被检测
- ✅ Cookie 和会话状态完全保留

## 安全警告 ⚠️

### 风险说明

开放的 CDP 端口允许技能：
- 访问所有浏览器标签页
- 读取/写入 Cookie 和会话
- 以登录用户身份执行操作

### 安装前检查清单

- [ ] **审查代码**：自己检查 `post_tweet.js`（或让信任的人帮忙）
- [ ] **专用配置**：使用测试 Chrome 配置文件或一次性账户，**不要用主账号**
- [ ] **本地安装**：`npm install` 在隔离环境而非全局安装
- [ ] **手动调用**：优先用户手动触发，避免自主持久运行
- [ ] **关闭端口**：使用完毕后关闭 Chrome 的 `--remote-debugging-port`

### 敏感配置

| 变量 | 说明 | 敏感度 |
|------|------|--------|
| `CDP_URL` | 本地调试端口，如 `http://127.0.0.1:28800` | ⚠️ 本地端点，勿泄露 |
| `X_USERNAME` | X 用户名 | 低（公开信息） |

### 额外建议

- **更高安全保障**：在一次性虚拟机或专用 Chrome 配置文件中运行
- **验证无数据外传**：确认脚本不会向外部服务器发送数据
- **限制执行权**：如需更严格控制，可限制技能仅限用户手动调用

### 信任链

```
用户启动 Chrome (开启 CDP) → Playwright 连接 → 以用户身份发帖
```

## 完整流程

### 第一步：用户启动 Chrome（开启 CDP 模式）

用户需要打开一个开启了调试端口的 Chrome。这是**一次性操作**，之后都保持运行。

**Mac**：
```bash
open -a "Google Chrome" --args --remote-debugging-port=28800
```

**Windows/Linux**：
```bash
chrome.exe --remote-debugging-port=28800
```

**验证方法**：
```bash
curl http://localhost:28800/json/version
```
如果返回 JSON，说明 Chrome 已经在监听。

### 第二步：Playwright 连接 Chrome

```javascript
const { chromium } = require('playwright');

(async () => {
  // 连接用户已有的 Chrome（CDP 模式）
  const browser = await chromium.connectOverCDP('http://127.0.0.1:28800');
  
  // 获取已有页面（继承登录状态！）
  const page = browser.contexts()[0].pages()[0];
  
  // 验证
  console.log('当前页面:', page.url());
  
  // 发推...
})();
```

### 第三步：发推的特殊方法

#### 为什么普通方法不 work？

| 方法 | 问题 |
|------|------|
| `page.fill()` | 直接设置 DOM 值，不触发 React onChange 事件 |
| `page.click('button')` | 按钮初始是 disabled，React 状态未更新 |
| `page.evaluate(() => btn.click())` | URL 跳转了但推文没发出 |

#### 正确方法：keyboard.type() + Meta+Enter

```javascript
// 1. 打开发帖页面
await page.goto('https://x.com/compose/post');
await page.waitForTimeout(3000);

// 2. 点击输入框（获得焦点）
await page.click('[data-testid="tweetTextarea_0"]');
await page.waitForTimeout(500);

// 3. 用键盘输入（触发 React 状态更新！）
await page.keyboard.type('这是推文内容 #Web3', { delay: 30 });

// 4. 用 Meta+Enter 发送（不能用 click！）
await page.keyboard.press('Meta+Enter');

// 5. 等待跳转
await page.waitForTimeout(3000);
```

#### 发送快捷键（跨平台）

| 平台 | 快捷键 |
|------|--------|
| Mac | `Meta+Enter` |
| Windows/Linux | `Control+Enter` |

脚本会自动检测平台并使用正确快捷键。

1. **`keyboard.type()` 触发完整事件链**：
   - keydown → keypress → input → keyup
   - React 监听 input 事件，更新内部状态
   - 状态更新后，按钮自动变为 enabled

2. **`Meta+Enter` 触发发送**：
   - X 支持键盘快捷键发送推文
   - `Meta+Enter` (Mac) / `Ctrl+Enter` (Windows/Linux)
   - 这个快捷键不依赖按钮的 disabled 状态

### 第四步：验证发送结果

```javascript
// 不要检查首页！推文排序可能不是按时间
// 直接去用户主页确认
await page.goto('https://x.com/你的用户名');

const tweets = await page.evaluate(() => {
  const items = document.querySelectorAll('[data-testid="tweet"]');
  return Array.from(items).slice(0, 5).map(t => ({
    text: t.innerText.substring(0, 100)
  }));
});

console.log('最新推文:', tweets);
```

#### username 配置

用户名通过函数参数传入，默认为 `woaijug`：
```javascript
postTweet(content, 'your_username');
```

或通过环境变量：
```bash
export X_USERNAME=your_username
node post_tweet.js "我的推文内容"
```

## 完整示例脚本

```javascript
const { chromium } = require('playwright');

const CONFIG = {
  CDP_URL: process.env.CDP_URL || 'http://127.0.0.1:28800',
  USERNAME: process.env.X_USERNAME || 'woaijug'
};

async function postTweet(content, username = CONFIG.USERNAME) {
  console.log('🚀 开始发推...');
  
  // 检测平台，使用正确的发送快捷键
  const isMac = process.platform === 'darwin';
  const sendKey = isMac ? 'Meta+Enter' : 'Control+Enter';
  console.log('   Platform:', process.platform, '→ Send key:', sendKey);
  
  try {
    // 1. 连接 Chrome
    const browser = await chromium.connectOverCDP(CONFIG.CDP_URL);
    const page = browser.contexts()[0].pages()[0];
    console.log('✓ 已连接，当前页面:', page.url());
    
    // 2. 打开发帖页面
    await page.goto('https://x.com/compose/post');
    await page.waitForTimeout(3000);
    console.log('✓ 已打开发帖页面');
    
    // 3. 点击输入框
    await page.click('[data-testid="tweetTextarea_0"]');
    await page.waitForTimeout(500);
    
    // 4. 用键盘输入内容
    await page.keyboard.type(content, { delay: 30 });
    console.log('✓ 已填写内容');
    
    // 5. 发送（自动适配 Mac/Windows/Linux）
    await page.keyboard.press(sendKey);
    console.log('✓ 已发送');
    
    // 6. 等待跳转
    await page.waitForTimeout(3000);
    
    // 7. 验证结果
    const finalUrl = page.url();
    const success = finalUrl.includes('/home') || finalUrl.includes('/' + username);
    
    await browser.close();
    
    return { 
      success, 
      message: success ? '推文发送成功！' : '发送状态未知',
      url: finalUrl 
    };
    
  } catch (error) {
    return { success: false, message: error.message };
  }
}

// 命令行调用
if (require.main === module) {
  const username = process.env.X_USERNAME || 'woaijug';
  const content = process.argv[2] || '默认推文内容';
  postTweet(content, username).then(r => console.log('结果:', r));
}

module.exports = { postTweet };
```

## 故障排除

### 问题：连接失败

**错误**：`Error: connect ECONNREFUSED 127.0.0.1:28800`

**解决**：用户需要先启动 Chrome：
```bash
# Mac
open -a "Google Chrome" --args --remote-debugging-port=28800

# Windows
chrome.exe --remote-debugging-port=28800
```

### 问题：推文没发出

**检查**：
1. 页面是否正确加载？`page.url()` 应该是发帖页
2. 内容是否输入成功？可以在 `keyboard.type()` 后加 `waitForTimeout`
3. 按钮是否可用？（有时需要等一下 React 状态更新）

**尝试**：
```javascript
await page.waitForTimeout(2000); // 等待 React 更新
```

### 问题：去首页看不到推文

**解决**：去用户主页查看，不要只看首页
```javascript
await page.goto(`https://x.com/${USERNAME}`);
```

## 前置要求

1. **Chrome 开启 CDP 模式**
2. **用户已登录 X**
3. **Playwright 已安装**（在 skill 目录下：`npm install`）

## 技术总结

| 项目 | 说明 |
|------|------|
| 连接方式 | `chromium.connectOverCDP()` |
| 发送方法 | `keyboard.type()` + `keyboard.press('Meta+Enter')` |
| 验证方式 | 去用户主页 `x.com/username`，不是首页 |
| 端口 | 默认 `28800`，可在 CONFIG 中修改 |

## 已知限制

- 需要用户手动启动 Chrome（一次性操作）
- 如果用户退出登录，需要重新登录
- 只支持 X Web 端，不支持移动端
