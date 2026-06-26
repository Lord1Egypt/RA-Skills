# Auth 模块

使用 OAuth 2.0 设备授权流程完成认证。
只需运行一次 — 凭证会保存在本地，其他所有模块自动加载。

## 子命令

| 子命令 | 说明 |
|------------|-------------|
| `login`  | 完整流程：初始化 → 输出链接并尝试打开浏览器 → 轮询 → 保存凭证 |
| `poll`   | 恢复之前中断的登录（仅用于恢复） |
| `logout` | 删除已保存的凭证文件 |
| `status` | 显示当前登录状态（uid、email、name、遮蔽的 api_key） |

## 用法

```bash
python {baseDir}/scripts/auth.py <subcommand>
```

## `login` — 完整登录流程

```bash
python {baseDir}/scripts/auth.py login
```

此命令处理**整个登录流程**：
1. 调用远程 OAuth 服务器启动设备会话
2. 输出授权链接（`URL: https://...`），并尝试自动打开浏览器（无浏览器环境下静默跳过）
3. 自动轮询直到用户授权（或会话过期）
4. 成功后将凭证保存到 `~/.tekan/credentials.json`

**关键：无论浏览器是否成功打开，Agent 都必须从命令输出中提取授权链接，并在引导消息中以 `[👉 点击此处完成登录授权](实际URL)` 的 Markdown 链接格式提供给用户**；详见主 SKILL 中「安装完成与登录引导」步骤 2 的详细规则和正反示例。

### 完整流程

```
Agent 运行：  python auth.py login
                 ↓ 输出授权链接（URL: https://...），尝试打开浏览器（可能静默失败）
Agent 发送引导消息：以 [👉 点击此处完成登录授权](URL) 格式展示可点击登录链接
                 ↓ 命令持续自动轮询
                 ↓ 用户在浏览器中登录并点击授权
                 ↓ 命令检测到授权通过，保存凭证
凭证已保存到 ~/.tekan/credentials.json ✓
```

## `poll` — 恢复中断的登录

```bash
python {baseDir}/scripts/auth.py poll
```

**仅在** `login` 被中断时使用（如轮询期间终端被关闭）。
从 `~/.tekan/pending_device.json` 读取待处理的会话并恢复轮询。

## `status` — 检查登录状态

```bash
python {baseDir}/scripts/auth.py status
```

已登录时的输出：

```
Logged in
  uid:         NsDAaOPF4jLuAie4ewyg
  name:        John Doe
  email:       user@example.com
  api_key:     sk-...3HB
  charge_type: pro
  authorized:  2026-03-04T10:00:00+00:00
  file:        /Users/you/.tekan/credentials.json
```

## `logout` — 删除凭证

```bash
python {baseDir}/scripts/auth.py logout
```

## 凭证文件

保存位置：`~/.tekan/credentials.json`。文件权限设置为 `0600`（仅所有者可读写）。

## 凭证加载优先级

所有模块通过 `shared/config.py` 加载凭证：

1. `~/.tekan/credentials.json`（由 `auth.py login` 设置）
2. 报错 — 提示运行 `auth.py login`

## Agent 规则

- **永远不要** 让用户自己运行 `python auth.py login` 或其他任何命令。
- **始终** 自己运行 `auth.py login`，从输出中提取授权链接，并以 `[👉 点击此处完成登录授权](实际URL)` 格式展示给用户（与 SKILL 登录模板一致，禁止裸贴 URL）。
