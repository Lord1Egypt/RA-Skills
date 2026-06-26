# 浏览器操作模块

## 设计原则

基于本地 `browser-relay-cli`，目标是 **稳定、可审计、手动确认**：

- 使用你们自己的 Browser Relay 运行时，而不是 OpenClaw
- 优先 DOM 可见元素与标准输入，不依赖 stealth / 规避检测逻辑
- 点赞、关注、评论都先生成建议，再由用户确认是否执行
- 能复用现有 tab 就复用，不盲目开新窗口

---

## 1. 运行时准备

### 1.1 检查 Browser Relay

```bash
npx browser-relay-cli version
npx browser-relay-cli extension-path
npx browser-relay-cli relay-start
npx browser-relay-cli status
```

要求：
- `extensionConnected: true`
- Chrome/Chromium 已登录目标 X 账号

### 1.2 推荐流程

```bash
npx browser-relay-cli list-tabs
npx browser-relay-cli create-tab https://x.com/home
```

如果已经有可复用的 X tab，优先复用，不重复创建。

---

## 2. 核心规则

1. **不要自动发送评论。**
2. **不要自动安装调度器。**
3. **所有写操作先展示预览，再等待用户确认。**
4. **只在用户明确同意时执行点赞、关注、评论。**

---

## 3. 常用操作

### 3.1 打开首页

```bash
npx browser-relay-cli create-tab https://x.com/home
```

### 3.2 查看当前页面

```bash
npx browser-relay-cli screenshot <tabId>
npx browser-relay-cli describe-visible <tabId>
```

### 3.3 切到 Following / Recent

优先用 DOM 选择器；选择器失效时，再用截图 + 坐标点击。

```bash
npx browser-relay-cli click <tabId> 'a[href="/home"]'
npx browser-relay-cli click <tabId> 'a[href="/home?tab=following"]'
npx browser-relay-cli click <tabId> 'a[href="/home?tab=recent"]'
```

### 3.4 读取推文内容

```bash
npx browser-relay-cli raw CDP.send "{\"tabId\":<tabId>,\"method\":\"Runtime.evaluate\",\"params\":{\"expression\":\"(() => { const tweets = [...document.querySelectorAll('[data-testid=\\\"tweet\\\"]')]; return tweets.slice(0, 5).map((tweet) => ({ author: tweet.querySelector('[data-testid=\\\"User-Name\\\"]')?.innerText || '', content: tweet.querySelector('[data-testid=\\\"tweetText\\\"]')?.innerText || '', link: tweet.querySelector('a[href*=\\\"/status/\\\"]')?.href || '' })); })()\",\"returnByValue\":true}}"
```

---

## 4. 评论流程

### 4.1 生成评论建议

先基于 persona、历史记录、推文内容生成 1-3 个候选评论，只展示，不自动提交。

输出格式建议：

```text
推文作者: @example
推文链接: https://x.com/...
候选评论:
1. ...
2. ...
3. ...
```

### 4.2 用户确认后再填入输入框

```bash
npx browser-relay-cli click <tabId> '[data-testid="reply"]'
npx browser-relay-cli type <tabId> '[data-testid="tweetTextarea_0"]' '这里填入用户已确认的评论'
```

### 4.3 发送前最后确认

发送动作必须单独确认一次。确认前可以：

```bash
npx browser-relay-cli screenshot <tabId>
npx browser-relay-cli describe-visible <tabId>
```

确认后再执行：

```bash
npx browser-relay-cli click <tabId> '[data-testid="tweetButton"]'
```

---

## 5. 点赞与关注

点赞、关注同样走确认流：

1. 先展示目标账号/推文
2. 说明为什么要点赞或关注
3. 等用户确认
4. 再执行 click

示例：

```bash
npx browser-relay-cli click <tabId> '[data-testid="like"]'
npx browser-relay-cli click <tabId> '[data-testid$="-follow"]'
```

---

## 6. 频率建议

这些是人工运营建议，不是自动化节流器：

- 点赞：每小时不超过 20 次
- 评论：每小时不超过 5 次
- 关注：每小时不超过 5 次
- 评论之间保留自然阅读和思考时间

---

## 7. 故障处理

### 7.1 选择器失效

1. `screenshot`
2. `describe-visible`
3. `click-at` 或 `click-at-norm`

### 7.2 扩展未连接

```bash
npx browser-relay-cli status
```

如果未连接：
1. 运行 `npx browser-relay-cli relay-start`
2. 在 `chrome://extensions` 加载 unpacked 扩展
3. 重试 `status`

---

## 8. 与 x-engagement 整合

- Persona 仍然从 `memory/daily/hotspots/personas/*.md` 读取
- 评论历史仍然写到 `memory/daily/hotspots/history/comments/`
- Browser Relay 只负责浏览器交互，不负责定时任务

---

## 9. 最佳实践

1. 复用已有 tab
2. 所有写操作先预览
3. 评论发送前二次确认
4. 定期手动运行清理脚本，而不是后台常驻
5. 把 Browser Relay 当成受控工具，不要当隐身机器人
