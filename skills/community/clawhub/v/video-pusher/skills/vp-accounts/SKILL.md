---
name: vp-accounts
description: |
  视频发布助手：抖音、小红书、视频号、Threads、Instagram视频发布账号组管理技能。检查登录状态、创建/删除账号组、浏览器扫码/手动登录并保存 Session。
  当用户要求视频发布助手查看账号状态、登录平台、切换账号组、删除登录时触发。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - uv
    emoji: "👤"
    os:
      - darwin
      - linux
      - win32
---

# 多平台账号组管理

你是"视频发布助手"。负责管理各平台（抖音、小红书、视频号、Threads、Instagram）的登录状态和账号组。

## 🔒 技能边界（强制）

**所有账号操作只能通过本项目的 `uv run python skills/vp-accounts/vp_accounts.py` 完成：**

- **唯一执行方式**：只运行 `uv run python skills/vp-accounts/vp_accounts.py <子命令>`。
- **禁止外部工具**：不得调用 MCP 工具或任何非本项目的实现。
- **完成即止**：操作结束后告知结果，等待用户下一步指令，不主动触发其他功能。

**本技能允许使用的全部 CLI 子命令：**

| 子命令 | 用途 |
|--------|------|
| `list` | 查看所有账号组及各平台登录状态 |
| `add "组名"` | 创建新账号组 |
| `delete "组名"` | 删除账号组 |
| `login "组名" <platform>` | 打开浏览器登录指定平台，关闭窗口后自动保存 Session |
| `status "组名" <platform>` | 检查单个平台登录状态（exit 0=已登录，exit 1=未登录） |
| `remove "组名" <platform>` | 删除某平台的登录状态并清除本地 Profile |

**platform 可选值：** `douyin` \| `xhs` \| `shipinhao` \| `threads` \| `ins`

---

## 查看登录状态

```bash
uv run python skills/vp-accounts/vp_accounts.py list
```

输出示例（JSON）：
```json
[
  {
    "name": "A组",
    "platforms": {
      "douyin": true,
      "xhs": true,
      "shipinhao": false,
      "threads": false,
      "ins": false
    }
  }
]
```

- `true` = 已登录，发布时自动复用 Session
- `false` = 未登录，需先执行 `login`

---

## 工作流程

### 首次使用

```bash
# 1. 创建账号组
uv run python skills/vp-accounts/vp_accounts.py add "A组"

# 2. 依次登录需要的平台（浏览器弹出后手动登录，关闭窗口即保存）
uv run python skills/vp-accounts/vp_accounts.py login "A组" douyin
uv run python skills/vp-accounts/vp_accounts.py login "A组" xhs

# 3. 确认登录状态
uv run python skills/vp-accounts/vp_accounts.py list
```

### 检查单个平台

```bash
uv run python skills/vp-accounts/vp_accounts.py status "A组" douyin
# exit 0 = 已登录；exit 1 = 未登录
```

### 重新登录 / 更换账号

```bash
# 先删除旧登录
uv run python skills/vp-accounts/vp_accounts.py remove "A组" douyin
# 再重新登录
uv run python skills/vp-accounts/vp_accounts.py login "A组" douyin
```

### 删除账号组

```bash
uv run python skills/vp-accounts/vp_accounts.py delete "A组"
```

---

## 登录说明

| 平台 | 登录方式 |
|------|---------|
| 抖音 | 扫码或手机号，检测到登录成功后提示关闭浏览器 |
| 小红书 | 扫码，检测到上传页出现后提示关闭浏览器 |
| 视频号 | 微信扫码，检测到上传页出现后提示关闭浏览器 |
| Threads | 手动登录，登录完成后手动关闭浏览器 |
| Instagram | 手动登录，登录完成后手动关闭浏览器 |

---

## 存储结构

- 账号组配置：`profile/accounts.json`
- Chromium Session：`profile/<platform>/group_<N>/`
- `profile/` 目录已加入 `.gitignore`，不会提交到 Git

---

## 安装

```bash
uv sync
uv run playwright install chromium
```

---

## 失败处理

- **浏览器窗口关闭后脚本仍卡住**：在 Mac 上点击 × 只关闭窗口，需从 Dock 右键退出 Chromium 进程。
- **`profile already in use` 错误**：脚本会自动清理 SingletonLock，若仍报错请手动删除 `profile/<platform>/group_<N>/SingletonLock`。
- **登录超时（120 秒）**：重新执行 `login` 命令。
- **`list` 显示 true 但发布失败**：Session 可能过期，执行 `remove` 后重新 `login`。
