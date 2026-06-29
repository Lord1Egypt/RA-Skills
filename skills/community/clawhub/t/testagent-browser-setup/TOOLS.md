# TOOLS.md — 浏览器工具使用指南

## 三个浏览器工具对比

| | OpenClaw 内置浏览器 | Playwright MCP | browser-use CLI |
|---|---|---|---|
| **调用方式** | `browser` 工具（snapshot/act/screenshot） | `playwright__browser_*` 系列工具 | `exec` 调用 `browser-use` 命令 |
| **浏览器引擎** | 本地 Chromium | 本地 Chromium | 本地 Chromium / 云端浏览器 |
| **状态获取** | accessibility snapshot（文本树） | snapshot（文本树） | `state`（元素索引列表） |
| **元素定位** | ref（如 e36） | ref + selector | 数字索引（如 click 5） |
| **截图返回** | AI 分析文本（❌ 不可分享） | PNG 文件（✅ 可分享） | 保存路径（✅ 可分享） |
| **JS 执行** | ✅ evaluate | ✅ evaluate | ✅ eval |
| **键盘事件** | ⚠️ React 受控组件不生效 | ✅ 支持良好 | ✅ `keys "Enter"` |
| **云浏览器** | ❌ | ❌ | ✅ `cloud connect` |
| **复用登录态** | ❌ | ❌ | ✅ `--profile "Default"` |
| **反爬/CAPTCHA** | ❌ | ❌ | ✅ 云浏览器内置 |
| **住宅代理** | ❌ | ❌ | ✅ 195+ 国家 |
| **内网隧道** | ❌ | ❌ | ✅ `tunnel <port>` |
| **多会话并行** | 有限（tabs） | 有限（tabs） | ✅ `--session NAME` |
| **命令链** | 不支持 | 不支持 | ✅ `&&` 链式执行 |
| **登录态保持** | ✅ 同一 tab 内保持 | ✅ 同一 page 内保持 | ✅ daemon 保活，跨命令保持 |

## 使用场景选择

### → 用 OpenClaw 内置浏览器（默认首选）
- 常规功能测试和页面交互
- 已登录的会话内操作
- 不需要截图分享给用户时
- **优势**：工具集成度高，一步到位

### → 用 Playwright MCP
- 需要截图分享给用户（bug 截图、状态确认）
- React/Vue 受控组件的精确交互（键盘事件支持好）
- 需要精确 selector 定位元素
- **优势**：元素定位最精确，截图可用

### → 用 browser-use CLI
- 需要云浏览器（反爬、CAPTCHA、住宅代理）
- 需要复用用户本地 Chrome 登录态
- 内网服务需通过隧道访问（`tunnel <port>`）
- 新产品快速探索（命令链 `&&` 高效）
- 多产品并行测试（`--session` 多会话）
- **优势**：浏览器能力最强，云+本地+隧道全覆盖

## 典型测试流程

1. **新产品首次探索** → browser-use CLI（云浏览器 + 命令链快速摸底）
2. **已熟悉产品回归测试** → OpenClaw 内置（快）或 Playwright MCP（精）
3. **需要截图记录 Bug** → Playwright MCP 或 browser-use CLI
4. **登录态受限的网站** → browser-use CLI（`--profile` 复用登录）
5. **反爬严格的网站** → browser-use CLI（`cloud connect`）

## 截图正确流程

```
1. playwright__browser_take_screenshot → filename="/tmp/screenshot.png"
2. cp /tmp/screenshot.png /root/.openclaw/workspace/<描述>.png
3. 回复中附加: MEDIA:/root/.openclaw/workspace/<描述>.png
```

- 内置浏览器的 `browser screenshot` 只返回 AI 分析文本，**无法**用 `MEDIA:` 分享
- `MEDIA:` 只在聊天回复中渲染，写进 `.md` 文件里不会显示图片

## CDP 直连（内置浏览器 SSRF 被拦时的主路径）

内置浏览器的 SSRF 白名单配置经常不生效（gateway 运行时缓存，文件写入不起作用）。**一旦 `browser navigate` 报 `blocked by policy`，立即切换到 CDP 直连，不要继续重启验证。**

### 启动

```bash
chrome-cdp &          # ~/.local/bin/chrome-cdp，headless + CDP port 9223
sleep 2
curl -s http://localhost:9223/json   # 验证可访问
```

### Node.js CDP 登录模板

```javascript
// login.js — 需要 ws 包（setup.sh 已预装）
const WebSocket = require('ws');

async function cdp(ws, method, params = {}) {
  return new Promise((resolve, reject) => {
    const id = Date.now();
    ws.send(JSON.stringify({ id, method, params }));
    ws.once('message', d => {
      const r = JSON.parse(d);
      r.error ? reject(r.error) : resolve(r.result);
    });
  });
}

async function waitForElement(ws, selector, timeout = 10000) {
  const start = Date.now();
  while (Date.now() - start < timeout) {
    const { result } = await cdp(ws, 'Runtime.evaluate', {
      expression: `!!document.querySelector('${selector}') && document.querySelector('${selector}').offsetParent !== null`,
      returnByValue: true,
    });
    if (result.value) return;
    await new Promise(r => setTimeout(r, 500));
  }
  throw new Error(`Timeout waiting for ${selector}`);
}

async function fillInput(ws, selector, value) {
  // 用 nativeInputValueSetter 触发 React state 更新
  await cdp(ws, 'Runtime.evaluate', {
    expression: `
      const el = document.querySelector('${selector}');
      const setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
      setter.call(el, '');                                     // 先清空
      el.dispatchEvent(new Event('input', { bubbles: true }));
      setter.call(el, ${JSON.stringify(value)});               // 再填值
      el.dispatchEvent(new Event('input', { bubbles: true }));
      el.dispatchEvent(new Event('change', { bubbles: true }));
    `,
  });
}

(async () => {
  const targets = await (await fetch('http://localhost:9223/json')).json();
  const ws = new WebSocket(targets[0].webSocketDebuggerUrl);
  await new Promise(r => ws.on('open', r));

  await cdp(ws, 'Page.navigate', { url: 'https://your-app.example.com/login' });
  await cdp(ws, 'Page.loadEventFired');  // 等页面加载完

  // 填邮箱（Auth0 identifier-first 流程）
  await waitForElement(ws, 'input[type="email"], input[name="email"]');
  await fillInput(ws, 'input[type="email"], input[name="email"]', 'user@example.com');
  await cdp(ws, 'Runtime.evaluate', { expression: `document.querySelector('[type="submit"], button[name="action"]').click()` });

  // 等密码框出现（Auth0：URL 不变，DOM 更新）— 不要用 URL 判断
  await waitForElement(ws, 'input[type="password"]');
  await fillInput(ws, 'input[type="password"]', 'your-password');
  await cdp(ws, 'Runtime.evaluate', { expression: `document.querySelector('[type="submit"], button[name="action"]').click()` });

  // 等登录跳转
  await cdp(ws, 'Page.loadEventFired');
  console.log('Login done');
  ws.close();
})();
```

运行：`node login.js`

---

## 常见踩坑

### React 表单填充：input.value = 'xxx' 不生效

React 受控组件劫持了 `input.value`，直接赋值不触发 state 更新，表单提交时值为空。

**必须用 nativeInputValueSetter**（见上方 `fillInput` 函数）。不要用简单赋值，不要用 Playwright 的 `fill()`（它在 CDP 直连场景不可用）。

### Auth0 分步登录：不要用 URL 变化判断步骤

Auth0 identifier-first 流程：输入邮箱 → 点 Continue → URL **不变**（仍是 `/u/login/identifier`），但 DOM 内部更新为密码页。密码框一开始是 `hidden`，邮箱提交后才显示。

**判断依据：`input[type="password"]` 是否 visible**（offsetParent !== null），用轮询等待，最多 10 秒。不要等 URL 变化。

### 填充前先清空旧值

每次 `fillInput` 前必须先 `setter.call(el, '')` + 触发 input 事件，否则若输入框有残留值，新值会被追加而非覆盖。

### Python 缺 pip，CDP 脚本用 Node.js

容器 Python 无 `pip`，无法装 `websockets`。用 Node.js + `ws` 包（`setup.sh` 已预装）。

### React/Vue 受控组件键盘事件不生效
`keyboard.press('Control+Enter')` 等快捷键在受控组件中可能无法触发。

解决：找页面上的实际提交按钮，用 JS 点击：
```javascript
document.querySelector('[aria-label="发送"]').click()
```

### 截图中文乱码（□□□）
运行 `testagent-browser-setup` skill 中的 `setup.sh`，会自动安装中文字体并配置 fontconfig。

### 配置修改后不生效
改 `~/.openclaw/openclaw.json` 后必须完整执行：
```
browser stop → openclaw gateway restart → 等 15 秒 → browser start
```
仅 restart gateway 或仅重启浏览器均不够。**SSRF 白名单即使文件写入成功，也可能因运行时缓存不生效。**
