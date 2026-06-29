---
name: testagent-browser-setup
version: 2.2.0
description: 在新的 openclaw 环境中安装并初始化 Chromium、系统依赖、中文字体和 CDP 启动脚本，无需 root 权限。当用户说「初始化测试环境」「安装浏览器工具」「setup browser」或在新机器首次部署测试 agent 时触发。
---

# Browser Setup

一次性环境初始化，在新 openclaw 容器上执行。不需要 root 权限。

## 说明

openclaw 环境默认已预装 Chromium，`setup.sh` 会优先使用它。若未找到则自动通过 Playwright 下载。

**截图和浏览器操作的主路径是：Chrome + CDP 直连。**
setup.sh 会创建 `~/.local/bin/chrome-cdp` 启动脚本。

**`mcp doctor --probe` 是假阳性。**
返回 ok 只说明 MCP server 进程启动，不代表 Chromium 能实际运行。唯一可信的验证：`playwright__browser_navigate` 真正返回页面内容。

## 执行顺序

### 第一步：运行核心安装脚本

```bash
bash scripts/setup.sh
```

脚本完成三件事：
1. **Chromium 检测**：优先用系统预装 Chromium，未找到则通过 Playwright 下载
2. **`chrome-cdp` 启动脚本**：`~/.local/bin/chrome-cdp`，封装 `--headless=new --no-sandbox --remote-allow-origins=*` 参数
3. **中文字体**：从 GitHub 下载 WenQuanYi Micro Hei 到 `~/.local/share/fonts/`

### 第二步：尝试配置内置浏览器（可选，经常无效）

编辑 `~/.openclaw/openclaw.json`（`config.patch` 拒绝修改受保护路径，只能手动写文件）：

```json
{
  "browser": {
    "noSandbox": true,
    "ssrfPolicy": {
      "allowedHostnames": [
        "你的目标产品域名（如 app.example.com）",
        "对应的登录域名（如 xxx.us.auth0.com）"
      ]
    }
  }
}
```

改完后：`browser stop → gateway restart → 等 15 秒 → browser start`

> ⚠️ **SSRF 白名单经常不生效**（gateway 有运行时缓存，不以文件为准）。
> 若 `browser navigate` 仍然报 `blocked by policy`，**立即放弃内置浏览器，改用 CDP 直连（见 TOOLS.md）**，不要继续重启验证。

### 第四步：初始化 TOOLS.md

```bash
cp "$(dirname "$0")/../TOOLS.md" ./TOOLS.md
```

### 第六步（可选）：安装 browser-use

```bash
bash scripts/setup-optional.sh
```

### 第七步：Smoke Test

```bash
# 启动 Chrome CDP
chrome-cdp &
sleep 2

# 验证 CDP 可访问
curl -s http://localhost:9223/json | python3 -m json.tool | head -20

# 截图验证（见 REFERENCE.md 的 CDP 截图流程）
```

验收标准：CDP `/json` 能返回 target 列表，截图中中文清晰无乱码。
