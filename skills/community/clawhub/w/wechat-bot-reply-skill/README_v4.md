# WeChat Auto Reply Skill v5 - 跨平台版（macOS + Windows）

## v5 新功能

### 跨平台支持

- **macOS**: 使用 Peekaboo CLI (`brew install steipete/peekaboo/peekaboo`)
- **Windows**: 使用 PeekabooWin (Node.js 22+)
- 脚本自动检测平台，无需手动指定引擎

### v4 保留功能

- 智能等待10分钟
- 已回复检测（绿色/白色气泡判断）
- 每10分钟扫描，节省资源

---

## 工作原理

```
1. 监控脚本每10分钟扫描一次微信窗口（自动选择平台引擎）
   macOS: Peekaboo CLI 截图
   Windows: PeekabooWin 截图
   ↓
2. 检测到新消息 → 写入 pending 文件（包含检测时间戳）
   macOS: /tmp/wechat_pending.txt
   Windows: %TEMP%\wechat_pending.txt
   ↓
3. 自动化任务每30秒检查一次 pending 文件
   ↓
4. 发现 pending 文件 → 检查是否超过10分钟
   ↓
5. 如果没超过10分钟 → 等待，不做任何操作
   ↓
6. 如果超过10分钟 → 重新截图，分析是否已回复
   ↓
7. 如果已回复（绿色气泡）→ 删除 pending，不回复
   ↓
8. 如果未回复（白色气泡）→ 生成回复并发送
```

---

## 文件结构

```
wechat-auto-reply/
├── SKILL.md           # Skill 定义 + 技术文档（AI Agent 参考）
├── USAGE.md          # 用户使用说明
├── README_v4.md      # 版本说明（本文件）
├── scripts/
│   └── wechat_monitor.py  # v5 跨平台监控脚本
└── references/
    └── peekaboo-guide.md  # Peekaboo (macOS) + PeekabooWin (Windows) 使用指南
```

---

## 前置条件

### macOS

| 要求 | 安装命令 |
|------|----------|
| Peekaboo CLI | `brew install steipete/peekaboo/peekaboo` |
| 权限 | 屏幕录制 + 辅助功能 |
| Python | 3.7+ (系统自带) |

### Windows

| 要求 | 安装步骤 |
|------|----------|
| Node.js 22+ | https://nodejs.org 下载安装 |
| PeekabooWin | `git clone https://github.com/FelixKruger/PeekabooWin && npm install` |
| 环境变量 | 设置 `PEEKABOO_WIN_DIR` 指向安装目录 |
| Python | 3.7+ (python.org 下载) |

详细安装步骤见 `references/peekaboo-guide.md`

---

## 配置参数

### wechat_monitor.py 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--contact` | "mini" | 监控的联系人名称 |
| `--interval` | 600 | 扫描间隔（秒），默认10分钟 |
| `--threshold` | 1000 | 截图变化阈值（字节） |
| `--wait` | 600 | 等待主人回复的时间（秒） |
| `--workdir` | 自动 | 工作目录（macOS: /tmp/wechat_mon, Windows: %TEMP%\wechat_mon） |
| `--pending` | 自动 | pending 文件路径 |
| `--engine` | auto | 自动化引擎: auto / peekaboo / peekaboo-win |
| `--peekaboo-win-dir` | PEEKABOO_WIN_DIR 环境变量 | PeekabooWin 安装目录 |

### 示例

```bash
# macOS: 默认配置
python3 scripts/wechat_monitor.py --contact mini

# Windows: 默认配置
python scripts/wechat_monitor.py --contact mini

# 指定引擎
python3 scripts/wechat_monitor.py --contact mini --engine peekaboo       # 强制 macOS
python scripts/wechat_monitor.py --contact mini --engine peekaboo-win   # 强制 Windows

# 自定义 PeekabooWin 路径
python scripts/wechat_monitor.py --contact mini --peekaboo-win-dir "D:\Tools\PeekabooWin"
```

---

## Pending 文件格式

```
DETECTED:2026-05-15T02:30:00
SCREENSHOT:/tmp/wechat_mon/latest.png
CONTACT:mini
```

| 字段 | 说明 |
|------|------|
| `DETECTED:` | 检测到新消息的时间戳 |
| `SCREENSHOT:` | 检测到变化时的截图路径 |
| `CONTACT:` | 监控的联系人名称 |

---

## 平台差异速查

| 功能 | macOS | Windows |
|------|-------|---------|
| 截图命令 | `peekaboo image --mode window --app 微信` | `peekaboo-win screen capture --output FILE` |
| 切换应用 | `peekaboo app switch --to 微信` | `peekaboo-win app switch --name "微信"` |
| 点击输入框 | `peekaboo click --coords X,Y --app 微信` | `peekaboo-win click --on "label"` 或 `mouse click --x --y` |
| 输入文字 | `peekaboo type "text" --app 微信` | `peekaboo-win type --text "text"` |
| 发送消息 | `peekaboo type "" --app 微信 --return` | `peekaboo-win press --keys "Enter"` |
| 临时目录 | `/tmp/wechat_mon/` | `%TEMP%\wechat_mon\` |
| Pending 文件 | `/tmp/wechat_pending.txt` | `%TEMP%\wechat_pending.txt` |
| 停止监控 | `kill $(pgrep -f wechat_monitor.py)` | `Stop-Process -Name python -Force` |
| 微信最小化 | 可以（Peekaboo 可取消隐藏） | 不可以（PeekabooWin 截屏幕） |

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
