# X/Twitter Poster Skill

通过 Playwright 连接用户已登录的 Chrome 浏览器，自动填写并发送推文。

## 安全警告 ⚠️

开放的 CDP 端口可访问所有浏览器数据。**安装前**：

1. ☐ **审查代码**：检查 `post_tweet.js` 确认无恶意代码
2. ☐ **专用配置**：使用测试 Chrome 配置文件或一次性账户，**不要用主账号**
3. ☐ **本地安装**：`npm install` 在隔离环境而非全局
4. ☐ **手动调用**：优先用户手动触发，避免自主持久运行
5. ☐ **关闭端口**：使用完毕后关闭 Chrome 的 `--remote-debugging-port`

**更高保障**：在一次性虚拟机或专用 Chrome 配置文件中运行。

## 工作原理

```
用户启动 Chrome (开启 CDP) → Playwright 连接 → 以用户身份发帖
```

## 使用前提

### 1. 启动 Chrome（开启 CDP 模式）

**Mac:**
```bash
open -a "Google Chrome" --args --remote-debugging-port=28800
```

**Windows/Linux:**
```bash
chrome.exe --remote-debugging-port=28800
```

### 2. 安装依赖

```bash
npm install
```

## 使用方法

```javascript
const { postTweet } = require('./post_tweet');

// 发送推文
postTweet('这是推文内容 #Web3', 'your_username')
  .then(result => console.log(result));
```

环境变量：
```bash
export CDP_URL=http://127.0.0.1:28800
export X_USERNAME=your_username
node post_tweet.js "推文内容"
```

## 跨平台支持

| 平台 | 发送快捷键 |
|------|-----------|
| Mac | Meta+Enter |
| Windows/Linux | Control+Enter |

脚本会自动检测平台。

## 安全建议

- 使用单独 Chrome 账号测试
- 不使用时关闭 CDP 端口
- 可限制技能仅限用户手动调用
