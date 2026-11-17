# Connector 配置速查表

> **连接器配置的权威入口**：配置要点、常见踩坑和最佳实践都在这里。
> 连接器出现故障（如 disconnected、调用失败）→ 排查路径见 `references/faq.md` → 第1节「连接器」。
> 这里只讲"怎么配"，FAQ 讲"坏了怎么办"，两个配合使用。

---

## 🚀 新手上路：3 分钟配好你的第一个连接器

> 授权看着吓人，其实就 3 步——跟着做，配错了我陪你查。这是新手最容易卡住的第一步，所以写得比别处都细、都暖。

### 授权流程（建议用 Visualizer 渲染下方 SVG）

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 680 175" font-family="-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif">
  <defs>
    <marker id="ar2" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L7,3 L0,6 Z" fill="#2f6fed"/>
    </marker>
  </defs>
  <text x="12" y="22" font-size="14" font-weight="700" fill="#1f2933">连接器授权流程：从打开设置到 connected</text>
  <g font-size="13" font-weight="600" text-anchor="middle">
    <rect x="12"  y="40" width="92" height="48" rx="9" fill="#2f6fed"/>
    <text x="58"  y="64" fill="#ffffff">① 打开设置</text>
    <rect x="116" y="40" width="92" height="48" rx="9" fill="#2f6fed"/>
    <text x="162" y="64" fill="#ffffff">② 找连接器</text>
    <rect x="220" y="40" width="92" height="48" rx="9" fill="#2f6fed"/>
    <text x="266" y="64" fill="#ffffff">③ 配 mcp.json</text>
    <rect x="324" y="40" width="92" height="48" rx="9" fill="#2f6fed"/>
    <text x="370" y="64" fill="#ffffff">④ 点 Trust</text>
    <rect x="428" y="40" width="92" height="48" rx="9" fill="#2f6fed"/>
    <text x="474" y="64" fill="#ffffff">⑤ 授权登录</text>
    <rect x="532" y="40" width="92" height="48" rx="9" fill="#0e9f6e"/>
    <text x="578" y="64" fill="#ffffff">⑥ connected</text>
  </g>
  <g stroke="#2f6fed" stroke-width="2" marker-end="url(#ar2)">
    <line x1="106" y1="64" x2="112" y2="64"/>
    <line x1="210" y1="64" x2="216" y2="64"/>
    <line x1="314" y1="64" x2="320" y2="64"/>
    <line x1="418" y1="64" x2="424" y2="64"/>
    <line x1="522" y1="64" x2="528" y2="64"/>
  </g>
  <g font-size="10" fill="#687385" text-anchor="middle">
    <text x="58"  y="108">找"连接器"页</text>
    <text x="162" y="108">列表里看到它</text>
    <text x="266" y="108">粘贴配置片段</text>
    <text x="370" y="108">右上角激活</text>
    <text x="474" y="108">OAuth / 填凭证</text>
    <text x="578" y="108">状态变绿 ✅</text>
  </g>
</svg>
```

### 四步法（文字版，随时回看）
1. **打开设置** → 找「连接器」管理页。
2. **找连接器** → 在列表里看到你要的那个（如 腾讯文档 / 企业微信 / QQ邮箱）。
3. **配置 mcp.json** → 复制下面的片段到 `~/.workbuddy/mcp.json`（注意不是 `.mcp.json`）。
4. **点 Trust 激活 + 授权登录** → 在连接器卡片右上角点「Trust」激活；OAuth 类会弹窗要你点"允许"，授权码类要你填账号+授权码；状态变 `connected` 就成功了。

### 授权类型对照表（提前知道会看到什么，不慌）

| 类型 | 代表连接器 | 你需要提前准备 | 授权时在 UI 看到什么 | 常见卡点 |
|------|-----------|--------------|-------------------|---------|
| OAuth 弹窗 | 腾讯文档 / 企业微信 | 账号已登录对应 App | 自动跳浏览器/弹窗要你点"允许" | 弹窗被拦截 → 允许弹窗后重试 |
| IMAP 授权码 | QQ邮箱(agent-mail) / 163 | 邮箱开启 IMAP/SMTP + **授权码(非登录密码)** | 要你填 EMAIL_USER + EMAIL_PASS(授权码) | 误填登录密码 → 改用授权码 |
| Webhook | 企业微信 Bot 推送 | 管理员给的 webhook URL | 配 URL 即生效 | 群机器人权限不足 |
| API Key / Token | 自选股 / 通达信 | 平台给的账号授权 | 配 env 或配置文件 | token 过期 → 重新授权 |

### ✅ 你试着说（直接复制给 AI）

- **"把腾讯文档连上"** → 我给你 mcp.json 片段 + 提示点 Trust → OAuth 登录 → 状态变 connected
- **"连一下我的 QQ 邮箱"** → 我给你 agent-mail 配置片段 + 提醒你开 IMAP 并用授权码（不是密码）
- **"企业微信怎么连"** → 我给 wecom 片段 + 提醒需管理员授权 / webhook
- **"接腾讯自选股行情"** → 我给 westock-mcp 片段 + 提醒需有效账号授权

> 配好后想查细节（完整配置片段、更多连接器、常见报错）→ 往下看「连接器基础规则 / 常用连接器配置要点 / 常见踩坑」。

---

## 连接器基础规则

> 先按上节「新手上路」走完 3 分钟流程；下面这张规则表是细节备查。

| 规则 | 说明 |

| 规则 | 说明 |
|------|------|
| 配置文件 | `~/.workbuddy/mcp.json`（注意：不是 `.mcp.json`，无前置点） |
| 启用方式 | 配置后需在连接器管理页面右上角点击"Trust"激活 |
| 命令路径 | Windows 下建议用绝对路径，避免 PATH 问题 |
| JSON 规范 | 不允许尾部逗号、不允许注释（标准 JSON） |

---

## 常用连接器配置要点

### 腾讯自选股（westock-mcp）

```json
{
  "mcpServers": {
    "westock-mcp": {
      "command": "npx",
      "args": ["-y", "@westock/mcp-server"]
    }
  }
}
```

**注意**：需要有效的腾讯自选股账号授权。

---

### 腾讯文档（tencent-docs）

```json
{
  "mcpServers": {
    "tencent-docs": {
      "command": "npx",
      "args": ["-y", "@tencent/docs-mcp"]
    }
  }
}
```

**注意**：首次使用需要 OAuth 授权登录；个人版和企业版是两个独立连接器。

---

### QQ邮箱（agent-mail / qq-mail）

```json
{
  "mcpServers": {
    "agent-mail": {
      "command": "node",
      "args": ["path/to/agent-mail-server.js"],
      "env": {
        "EMAIL_USER": "your@qq.com",
        "EMAIL_PASS": "your-auth-code"
      }
    }
  }
}
```

**注意**：QQ邮箱需开启 IMAP/SMTP 并使用授权码（非登录密码）。

---

### 企业微信（wecom）

```json
{
  "mcpServers": {
    "wecom": {
      "command": "npx",
      "args": ["-y", "@wecom/mcp-server"]
    }
  }
}
```

**注意**：需要企业微信管理员授权；Bot 推送需要配置 webhook。

---

### 通达信（tdx-connector）

```json
{
  "mcpServers": {
    "tdx-connector": {
      "command": "python",
      "args": ["tdx_server.py"]
    }
  }
}
```

**注意**：依赖通达信本地客户端数据；可能受网络策略限制。

---

### Obsidian（mcp-obsidian）

```json
{
  "mcpServers": {
    "mcp-obsidian": {
      "command": "npx",
      "args": ["-y", "mcp-obsidian"]
    }
  }
}
```

**注意**：需要指定 Obsidian Vault 路径；确保 vault 目录可访问。

---

## 常见踩坑

### 坑1：授权过期不报错

**现象**：连接器显示 connected，但 API 调用返回空。

**原因**：OAuth token 已过期但状态未更新。

**修复**：在连接器 UI 中 Disconnect 然后重新 Connect 刷新 token。

---

### 坑2：MCP 连接器不显示

**现象**：mcp.json 中已配置但连接器列表不出现。

**排查**：
1. `mcp.json` 路径是否为 `~/.workbuddy/mcp.json`（不是 `.mcp.json`）
2. JSON 语法是否合法（`python -m json.tool ~/.workbuddy/mcp.json`）
3. 是否点击了连接器管理页面的"Trust"

---

### 坑3：native command 找不到

**现象**：`"command": "npx"` 报找不到命令。

**原因**：Windows 下 npx 不在 PATH 中。

**修复**：使用绝对路径，如 `"command": "C:/Program Files/nodejs/npx.cmd"`。

---

### 坑4：env 变量不生效

**现象**：在 mcp.json 的 env 中设置的变量没被读取。

**诊断**：某些 MCP 服务器不从 env 读取，而是从自己的配置文件读取。

**修复**：查阅该连接器的官方文档，确认正确的凭证传入方式（可能是 env / headers / args / 独立配置文件）。

---

## 连接器启用/禁用的最佳时机

| 场景 | 建议 |
|------|------|
| 日常使用 | 保持 3-5 个核心连接器活跃，其余按需启用 |
| 长对话/复杂任务 | 关闭不用的连接器，释放上下文窗口 |
| 弱网环境 | 关闭依赖外部 API 的连接器，减少超时等待 |
| 新建对话 | 检查连接器状态，确保核心工具可用 |
| 故障排查 | 逐个禁用连接器定位问题源 |

---

> 更多帮助：`references/faq.md` → 第1节「连接器」；通用故障排查 `references/system-scan.md`
