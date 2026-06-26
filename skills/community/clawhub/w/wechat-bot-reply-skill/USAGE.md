# 微信自动回复 Skill v5 使用说明（跨平台版）

## v5 新功能

### 跨平台支持

- 同时支持 **macOS** 和 **Windows**
- macOS 使用 Peekaboo CLI，Windows 使用 PeekabooWin (Node.js)
- 脚本自动检测平台，无需手动配置

### v4 保留功能

- **智能等待（10分钟）**：检测到新消息后等待，给你时间手动回复
- **已回复检测**：分析截图判断是否已回复，避免重复回复
- **低频扫描**：每10分钟扫描一次，节省资源

---

## 前置条件

> **第一次使用时，WorkBuddy 会自动帮你检查以下条件。如果未满足，会显示安装指引，你按步骤操作后重新说"监控 XX 的微信"即可。**

### macOS 用户

| 要求 | 说明 |
|------|------|
| Peekaboo CLI | `brew install steipete/peekaboo/peekaboo` |
| 权限 | 屏幕录制 + 辅助功能 |
| Python | 3.7+ |

### Windows 用户（3 件事必须提前安装）

| 步骤 | 要求 | 说明 |
|------|------|------|
| **第 1 步** | Node.js 22+ | 从 https://nodejs.org 下载安装，务必选 **22.x LTS** 版本 |
| **第 2 步** | PeekabooWin | 打开 PowerShell 运行：`git clone https://github.com/FelixKruger/PeekabooWin` → `cd PeekabooWin` → `npm install` → `npm test` |
| **第 3 步** | 环境变量 | 运行：`[System.Environment]::SetEnvironmentVariable("PEEKABOO_WIN_DIR", "C:\PeekabooWin", "User")` 然后重新打开 PowerShell |

此外还需要：
- Python 3.7+（从 https://python.org 下载，安装时勾选"Add to PATH"）
- 微信窗口必须保持可见（不能最小化到任务栏）

> Windows 安装详细步骤请参考 `references/peekaboo-guide.md`

### 自动检查机制

当你第一次说 **"监控 XX 的微信"** 时，WorkBuddy 会自动：

1. **检测你的操作系统**（macOS / Windows）
2. **逐项检查依赖**（Node.js 版本、Peekaboo/PeekabooWin 是否安装、环境变量是否设置）
3. **如果全部通过** → 直接开始监控
4. **如果有未满足项** → 显示对应的安装指引（告诉你缺什么、怎么装），等你安装完再重新调用即可

---

## 快速开始

### macOS

```bash
# 1. 安装 Peekaboo
brew install steipete/peekaboo/peekaboo

# 2. 授予权限
# 系统设置 → 隐私与安全 → 屏幕录制 / 辅助功能

# 3. 启动监控（WorkBuddy 会自动检查条件）
# 在 WorkBuddy 中说：监控 mini 的微信
```

### Windows

> **你不需要手动检查，WorkBuddy 会自动检测。** 但如果你想提前安装好，按以下步骤操作：

```powershell
# 1. 安装 Node.js 22+
# 从 https://nodejs.org 下载安装（务必选 22.x LTS 版本）

# 2. 安装 PeekabooWin
git clone https://github.com/FelixKruger/PeekabooWin
cd PeekabooWin
npm install
npm test

# 3. 设置环境变量（永久生效）
[System.Environment]::SetEnvironmentVariable("PEEKABOO_WIN_DIR", "C:\PeekabooWin", "User")
# 重要：设置后必须重新打开 PowerShell 才能生效！

# 4. 安装 Python 3.7+
# 从 https://python.org 下载，安装时勾选 "Add to PATH"

# 5. 启动监控（WorkBuddy 会自动检查条件）
# 在 WorkBuddy 中说：监控 mini 的微信

# 4. 重新打开 PowerShell

# 5. 启动监控
# 在 WorkBuddy 中说：监控 mini 的微信
```

---

## 如何调用这个 Skill

只需要对我说：

```
监控 mini 的微信
```

或者更详细的需求：

```
监控 老板 的微信，回复风格要正式一点
监控 张三 的微信，他是我的好朋友，回复随意一点
监控 mini 的微信，等待时间设为 15 分钟
```

---

## 调用后会发生什么？

当你说 **"监控 [联系人] 的微信"** 后，我会：

### 1. 询问回复风格（可选）

```
你想要什么样的回复风格？
- 匹配你的说话风格（默认）
- 正式一点（适合工作联系人）
- 随意轻松（适合好友）
```

### 2. 检测平台并验证依赖

自动检测 macOS/Windows，确认对应引擎（Peekaboo/PeekabooWin）已安装并可用。

### 3. 启动后台监控

启动 Python 监控脚本（自动选择对应平台的截图引擎）：
- **每10分钟截图一次**微信窗口
- 检测截图文件大小变化
- 检测到变化后，写入"待回复"信号文件

**macOS 命令**：
```bash
python3 scripts/wechat_monitor.py --contact mini --interval 600 --wait 600
```

**Windows 命令**：
```powershell
python scripts/wechat_monitor.py --contact mini --interval 600 --wait 600
```

### 4. 创建自动回复任务

创建 WorkBuddy 自动化任务（每30秒检查一次），逻辑：

- 如果有待回复消息 → 检查是否超过10分钟
  - **没超过** → 等待
  - **已超过** → 截图分析是否已回复
    - **已回复**（绿色气泡）→ 不发送
    - **未回复**（白色气泡）→ 生成回复并发送

---

## 回复在多久内完成？

| 阶段 | 时间 | 说明 |
|------|------|------|
| **检测新消息** | 10分钟内 | 监控脚本每10分钟截图一次 |
| **等待你回复** | 10分钟 | 给你时间手动回复 |
| **AI 分析消息** | 5-15 秒 | 取决于消息复杂度和网络 |
| **发送回复** | 5-10 秒 | 使用 Peekaboo/PeekabooWin 模拟输入 |
| **总计** | **10-15 分钟** | 从收到消息到自动回复完成 |

**重点**：如果你在10分钟内回复了，AI **不会**再自动回复！

---

## 如何调整回复内容？

### 在启动时使用关键词

| 你说的话 | 效果 |
|----------|------|
| `监控 mini 的微信` | 默认风格，匹配你的说话方式 |
| `监控 老板 的微信，正式一点` | 回复更正式、有礼貌 |
| `监控 张三 的微信，随意一点` | 回复更轻松、口语化 |
| `监控 李四 的微信，简短回复` | 回复更简洁 |

### 调整等待时间

```
监控 mini 的微信，等待时间设为 15 分钟  # 延长等待
监控 mini 的微信，等待时间设为 5 分钟   # 缩短等待
```

### 修改已运行的自动回复

```
修改微信自动回复的 prompt，让回复更简短
```

---

## 积分消耗详情

| 项目 | v3（旧版） | v5（新版） | 节省 |
|------|-------------|-------------|--------|
| **扫描频率** | 每15秒 | 每10分钟 | **40倍** |
| **检测后立即回复** | 是 | 否（等待10分钟） | **可能100%** |
| **如果你已回复** | 仍会回复 | 不回复 | **节省1次** |

### 每次回复消耗的 Token

| 步骤 | Token 消耗 |
|------|-------------|
| 截图分析 | ~1000-2000 tokens |
| 消息理解 | ~500-1000 tokens |
| 生成回复 | ~100-300 tokens |
| **总计** | **~1600-3300 tokens/次** |

### 成本估算

| 模型 | 单次回复成本 |
|------|-------------|
| GPT-4o 级别 | 约 ¥0.1 |
| GPT-3.5 级别 | 约 ¥0.007 |

---

## 注意事项

### 通用

1. **微信窗口必须保持可见**（两个平台都是）
2. **联系人名称必须准确**：和微信中显示的名称完全一致
3. **回复不是即时的**：有 10-15 分钟延迟
4. **只会回复指定联系人**：安全可控
5. **已回复检测准确率约 90-95%**

### macOS 专属

- **权限**：屏幕录制 + 辅助功能（`peekaboo permissions` 检查）
- **微信可以最小化到 Dock**：Peekaboo 可以取消隐藏

### Windows 专属

- **微信不能最小化到任务栏**：PeekabooWin 截取屏幕内容，最小化后看不到
- **Node.js 必须 22+**：低于 22 会报错
- **必须设置 PEEKABOO_WIN_DIR 环境变量**：否则脚本找不到 PeekabooWin
- **管理员权限**：部分操作可能需要
- **pyautogui failsafe**：鼠标移到屏幕左上角会紧急停止

---

## 如何停止自动回复？

### 通用方法

```
停止微信监控
```

### macOS 额外操作

```bash
kill $(pgrep -f wechat_monitor.py)
rm -rf /tmp/wechat_mon /tmp/wechat_pending.txt
```

### Windows 额外操作

```powershell
Stop-Process -Name python -Force -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "$env:TEMP\wechat_mon"
Remove-Item -Force "$env:TEMP\wechat_pending.txt"
```

---

## 常见问题

### Q1: 为什么没有自动回复？

**检查清单**：
1. 监控脚本是否运行？
2. 自动化任务是否启用？
3. Pending 文件是否存在？
4. 你是否已在10分钟内回复？（如果已回复，不会自动回复）
5. 微信窗口是否可见？

### Q2: Windows 上截图失败？

- 检查 Node.js 版本: `node --version` (需要 >= 22)
- 检查 PEEKABOO_WIN_DIR 是否正确设置
- 确保微信窗口未被最小化
- 尝试以管理员身份运行 PowerShell

### Q3: macOS 上权限问题？

```bash
peekaboo permissions
# 系统设置 → 隐私与安全 → 屏幕录制 / 辅助功能
```

### Q4: 回复内容不合适？

```
让回复更简短/更详细/更正式/更随意
```

### Q5: 已回复检测不准确？

- 调整等待时间：`等待时间设为 15 分钟`
- 或说"停用已回复检测"

---

## 工作原理

```
微信收到新消息
    ↓
10分钟后截图检测变化（文件大小比较）
    ↓
写入 pending 文件（包含检测时间戳）
  macOS: /tmp/wechat_pending.txt
  Windows: %TEMP%\wechat_pending.txt
    ↓
WorkBuddy 自动化每 30 秒检查
    ↓
发现 pending 文件 → 检查是否超过10分钟
    ↓
没超过 → 等待，不做任何操作
    ↓
已超过 → 重新截图，分析是否已回复
    ↓
已回复（绿色气泡）→ 删除 pending，不回复
    ↓
未回复（白色气泡）→ 生成回复并发送
    ↓
删除 pending 文件
```

---

## 版本历史

| 版本 | 日期 | 主要变化 |
|------|------|----------|
| v1 | 2026-05-14 | 初始版本 (macOS only) |
| v2 | 2026-05-14 | 支持任意联系人 |
| v3 | 2026-05-14 | 修复发送逻辑 |
| v4 | 2026-05-15 | 智能等待10分钟 + 已回复检测 |
| **v5** | **2026-05-15** | **跨平台支持 (macOS + Windows)** |

---

**最后更新**：2026-05-15
**版本**：v5（跨平台版）
