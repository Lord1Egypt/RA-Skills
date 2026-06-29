# Browser Testing Reference

## 工具选择

### 对比表

| | OpenClaw 内置浏览器 | Playwright MCP | browser-use CLI |
|---|---|---|---|
| **调用方式** | `browser` 工具（snapshot/act/screenshot） | `playwright__browser_*` 系列 | `exec` 调用 `browser-use` 命令 |
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
| **多会话并行** | 有限 | 有限 | ✅ `--session NAME` |
| **命令链** | 不支持 | 不支持 | ✅ `&&` 链式执行 |

### 何时用哪个

**→ 用 OpenClaw 内置浏览器（默认首选）**
- 常规功能测试和页面交互
- 已登录的会话内操作
- 不需要截图分享给用户时
- **优势**：工具集成度高，一步到位

**→ 用 Playwright MCP**
- 需要截图分享给用户（bug 截图、状态确认）
- React/Vue 受控组件的精确交互（键盘事件支持好）
- 需要精确 selector 定位元素
- **优势**：元素定位最精确，截图可用

**→ 用 browser-use CLI**
- 需要云浏览器（反爬、CAPTCHA、住宅代理）
- 需要复用用户本地 Chrome 登录态
- 内网服务需通过隧道访问（`tunnel <port>`）
- 新产品快速探索（命令链 `&&` 高效）
- 多产品并行测试（`--session` 多会话）
- **优势**：浏览器能力最强，云+本地+隧道全覆盖

### 决策树

**默认用 OpenClaw 内置浏览器**，遇到以下情况再切换：

```
需要截图分享给用户？
  → 先试 Playwright MCP（take_screenshot 存文件）
    → playwright__browser_navigate 能跑通？→ 用 Playwright MCP
    → 跑不通（缺系统依赖 / 无 root）？→ 用内置浏览器 + CDP 直连截图（见下方）

React/Vue 受控组件操作失败（键盘事件不生效）？
  → 改用 Playwright MCP

目标网站有反爬 / CAPTCHA，内置浏览器和 Playwright 都被拦？
  → 改用 browser-use CLI（cloud connect）

需要复用用户本地 Chrome 登录态？
  → 改用 browser-use CLI --profile "Default"

需要内网隧道或多会话并行？
  → 改用 browser-use CLI
```

---

## 截图正确流程

### 路径 1：Playwright MCP（首选）

```
1. playwright__browser_navigate → 目标 URL（真正跑通才算可用）
2. playwright__browser_take_screenshot → filename="~/.openclaw/workspace/bug_<序号>_<描述>.png"
3. 回复中附加: MEDIA:~/.openclaw/workspace/bug_<序号>_<描述>.png
```

### 路径 2：Chrome CDP 直连（Playwright MCP 不可用时的主 fallback）

setup.sh 创建了 `~/.local/bin/chrome-cdp` 启动脚本，封装了正确的 LD_LIBRARY_PATH 和启动参数。

```bash
# 1. 启动 Chrome（后台运行）
chrome-cdp &
sleep 2  # 等待启动

# 2. 导航到目标页面
curl -s http://localhost:9223/json/new?about:blank  # 创建新标签页
TARGET_ID=$(curl -s "http://localhost:9223/json" | python3 -c \
  "import json,sys; t=[x for x in json.load(sys.stdin) if x.get('type')=='page']; print(t[0]['id'])")

# 3. 通过 CDP WebSocket 导航
node -e "
const ws = new (require('ws').WebSocket)('ws://localhost:9223/devtools/page/$TARGET_ID');
ws.on('open', () => {
  ws.send(JSON.stringify({id:1, method:'Page.navigate', params:{url:'https://your-target.com'}}));
});
ws.on('message', d => { const r=JSON.parse(d); if(r.id===1){ws.close();} });
"

# 4. 截图
SCREENSHOT="$HOME/.openclaw/workspace/screenshot_$(date +%s).png"
node -e "
const ws = new (require('ws').WebSocket)('ws://localhost:9223/devtools/page/$TARGET_ID');
ws.on('open', () => ws.send(JSON.stringify({id:1,method:'Page.captureScreenshot',params:{format:'png'}})));
ws.on('message', d => {
  const r = JSON.parse(d.toString());
  if (r.id === 1) {
    require('fs').writeFileSync('$SCREENSHOT', Buffer.from(r.result.data,'base64'));
    ws.close(); process.exit(0);
  }
});
"
echo "MEDIA:$SCREENSHOT"
```

**JS 交互（填表单、点击按钮）同理**，用 `Runtime.evaluate` 替换截图命令：
```javascript
{id:2, method:'Runtime.evaluate', params:{expression:'document.querySelector("button").click()'}}
```

### 路径 3：browser-use CLI（CDP 也搞不定时）

```bash
browser-use screenshot --output ~/.openclaw/workspace/screenshot.png
```

**通用注意事项**：
- 内置浏览器的 `browser screenshot` 只返回 AI 分析文本，三条路径都不包括它
- `MEDIA:` 只在聊天回复中渲染，写进 `.md` 文件里不显示
- `mcp doctor --probe` 返回 ok 是假阳性，不代表 Playwright 真正可用

---

## 报告格式

```
## 测试报告：[功能名称] @ [URL]
测试时间：YYYY-MM-DD
测试工具：Playwright MCP / browser-use CLI / 内置浏览器

### 测试结果摘要
- 测试点总数：5
- 通过：3
- 发现 Bug：2

### 通过的测试点
- ✅ 正常登录流程
- ✅ 表单必填项校验
- ✅ 核心功能 X happy path

### Bug 清单

**Bug #1：[标题]**
- 测试点：[对应的测试点]
- 现象：[一句话描述]
- 复现步骤：
  1. ...
  2. ...
  3. ...
- 期望结果：...
- 实际结果：...
- 截图：MEDIA:/root/.openclaw/workspace/bug_1_xxx.png
- 建议优先级：高（核心功能不可用）
- 建议 assignee：[根据 AGENTS.md 分工规则]
- 建议修复工期：2 天
```

---

## 优先级规则

| 情况 | 建议优先级 | coding-net 值 |
|------|-----------|--------------|
| 核心功能完全不可用，阻塞用户 | 最高 / 高 | 0 或 1 |
| 功能异常但存在绕路方案 | 中 | 2 |
| UI / 体验问题，不影响核心使用 | 低 / 最低 | 3 或 4 |

若 AGENTS.md 中有更具体的优先级标准，以 AGENTS.md 为准。

---

## 踩坑

### 内置浏览器启动失败 / 超时（容器环境）
**现象**：`browser start` 报 `Timeout waiting for browser`，`browser doctor` 卡在 `launching...`

**根因**：容器以 root 运行，Chromium 需要 sandbox，但容器缺少 `USER_NAMESPACE` 权限

**解决**：直接编辑 `~/.openclaw/openclaw.json`（不能用 `config.patch`，browser 路径受保护）：
```json
{
  "browser": {
    "noSandbox": true
  }
}
```
然后执行完整重启序列（顺序不能错）：
```bash
browser stop
openclaw gateway restart
# 等待约 15 秒
browser start
```

### 内置浏览器导航报 blocked by policy（SSRF 拦截）
**现象**：`browser navigate` 到目标 URL 时报 `blocked by policy`

**根因**：内置浏览器默认启用 SSRF 防护，只允许访问白名单域名

**解决**：在 `~/.openclaw/openclaw.json` 的 `browser.ssrfPolicy.allowedHostnames` 中添加目标域名，以及登录页的 Auth0 / SSO 域名（否则登录跳转也会被拦截）：
```json
{
  "browser": {
    "noSandbox": true,
    "ssrfPolicy": {
      "allowedHostnames": [
        "app.example.com",
        "xxx.us.auth0.com"
      ]
    }
  }
}
```
改完同样执行完整重启序列：`browser stop` → `gateway restart` → 等 15 秒 → `browser start`

### Ctrl+Enter 快捷键不生效
React 受控组件的键盘快捷键在自动化工具中可能无法触发。

解决：找页面上真正的发送/提交按钮，用 JS 直接点击：
```javascript
document.querySelector('[aria-label="发送"]').click()
// 或用 playwright evaluate / browser evaluate
```

### 截图中文显示乱码（□□□）
说明字体未正确安装，重新运行 browser-setup skill。

验证命令：
```bash
fc-match ":lang=zh"
# 期望输出包含 "Noto Sans CJK SC"，而非 "DejaVu Sans"
```

### Playwright MCP 报 Missing system dependencies

**现象**：`playwright__browser_navigate` 报错 `Missing system dependencies`，`mcp doctor --probe` 却返回 ok

**根因**：`mcp doctor` 只检查 MCP server 进程启动，不验证 Chromium 是否能运行。无 root 环境下 20+ 个系统 `.so` 缺失，Chromium 启动即崩溃。

**解决**：不要尝试 `sudo`/`apt`/`install-deps`，直接切换路径：
- 截图需求 → 内置浏览器 + CDP 直连（见上方路径 2）
- 页面交互需求 → 继续用内置浏览器（snapshot/act）

### 遇到操作卡点
同一方法尝试 2-3 次失败后立即切换策略：
- 内置浏览器失败 → 改用 Playwright MCP
- Playwright MCP 失败（缺依赖）→ 截图用 CDP 直连，交互用内置浏览器
- 都失败 → 改用 browser-use CLI
- 不要在一条路上死磕
