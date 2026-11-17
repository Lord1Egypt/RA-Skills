# screen-off

Toggle any macOS display on or off from the command line — by stable ID, list index, or name.

Zero dependencies. Just the system Python 3.8+ (or newer). No root, no accessibility permissions, no `pip install`.

Built on the core private-API calls from **[zy0816/ScreenOff](https://github.com/zy0816/ScreenOff)**, extracted into a standalone CLI.

## Features

- List every display, including disabled ones
- Turn a display off/on by **stable ID**, list **index** (`#2`), or **name** (`main`, `builtin`, or fuzzy like `S2700`)
- `--force` to power off even the last active display
- `--permanent` to keep the setting across reboots
- Quiet mode (`-q` / `--quiet`)

## Install

```bash
git clone https://github.com/mfang0126/screen-off.git
# Use it directly, or make an alias:
alias screen-off='python3 /path/to/screen-off/screen-off.py'
```

## Usage

```bash
# List all displays (including disabled ones)
screen-off --status

# Toggle by ID (stable — does not change when displays turn off/on)
screen-off --off 3
screen-off --on 3

# By list index (# prefix, matches the # column of --status; changes as displays toggle)
screen-off --off #2

# By name
screen-off --off main        # the main display
screen-off --off builtin     # the built-in display
screen-off --off "S2700"     # fuzzy name match

# Force off (even if it's the only active display)
screen-off --off 3 --force

# Keep the setting after reboot
screen-off --off 3 --permanent
```

### Target resolution priority

| Format | Matched by | Stability |
|--------|------------|-----------|
| `3` | Display ID | ✅ stable |
| `#2` | List index | ⚠️ changes |
| `main` | Main display | ✅ stable |
| `builtin` | Built-in display | ✅ stable |
| `S2700` | Fuzzy name match | ✅ stable |

### Exit codes

| Code | Meaning |
|------|---------|
| 0 | Done, or already in the target state |
| 1 | Target display not found |
| 2 | Blackout protection refused (override with `--force`) |
| 3 | Configuration committed but not applied |

## How it works

macOS has no public API to power individual displays on or off. This tool uses 4 private CoreGraphics/SkyLight functions:

| Function | Purpose |
|---------|---------|
| `CGSGetDisplayList` | List every display slot (including disabled) |
| `CGSBeginDisplayConfiguration` | Begin a configuration transaction |
| `CGSConfigureDisplayEnabled` | Enable/disable a display (no public equivalent) |
| `CGSCompleteDisplayConfiguration` | Commit the configuration (return code unreliable — poll state instead) |

Notable findings (from the original project):
- Once the built-in display is disabled it disappears from the public API — only `CGSGetDisplayList` keeps its slot
- When all physical displays are off, macOS inserts a virtual display (`vendor="unkn"`, `model="virt"`)
- `CGSCompleteDisplayConfiguration` often returns `1001` but the display change actually takes effect

## Requirements

- macOS (SkyLight/CoreGraphics frameworks)
- Python 3.8+ (ships with macOS)
- No `pip install` needed

## Credit

The core private-API calls come from **[zy0816/ScreenOff](https://github.com/zy0816/ScreenOff)** (MIT License) by zy0816 <zyan980816@proton.me>. That project also ships a full menu-bar app (Swift) with a more complete recovery chain (three levels: enable → CGRestorePermanentDisplayConfiguration → sleepWake).

This project extracts the CLI part only, and extends target resolution (by ID/index/name) and removes the built-in-display restriction.

## License

MIT — see [LICENSE](LICENSE)

---

## 中文文档

# screen-off

macOS 显示器开关 CLI — 通过 ID/序号/名字控制任意显示器的开关状态。

零依赖，只需要系统 Python 3.8+。不需要 root，不需要辅助功能权限。

**基于 [zy0816/ScreenOff](https://github.com/zy0816/ScreenOff)** 的核心私有 API 调用，提取为独立 CLI 工具。

## 安装

```bash
git clone https://github.com/mfang0126/screen-off.git
# 直接用，或做个 alias：
alias screen-off='python3 /path/to/screen-off/screen-off.py'
```

## 用法

```bash
# 列出所有显示器（含禁用的）
screen-off --status

# 按 ID 开/关（ID 稳定，不会因开关变化）
screen-off --off 3
screen-off --on 3

# 按序号（# 前缀，对应 --status 的 # 列，会随开关变化）
screen-off --off #2

# 按名字匹配
screen-off --off main        # 关主屏
screen-off --off builtin     # 关内建屏
screen-off --off "S2700"     # 模糊匹配

# 强制关（即使它是唯一亮着的屏）
screen-off --off 3 --force

# 重启后保留
screen-off --off 3 --permanent
```

### 目标解析优先级

| 格式 | 匹配方式 | 稳定性 |
|------|----------|--------|
| `3` | 按 Display ID | ✅ 稳定 |
| `#2` | 按列表序号 | ⚠️ 会变 |
| `main` | 主显示器 | ✅ 稳定 |
| `builtin` | 内建显示器 | ✅ 稳定 |
| `S2700` | 模糊匹配名字 | ✅ 稳定 |

### 退出码

| 码 | 含义 |
|----|------|
| 0 | 完成或已在目标状态 |
| 1 | 找不到目标显示器 |
| 2 | 黑屏保护拒绝（加 `--force` 覆盖） |
| 3 | 配置已提交但未生效 |

## 工作原理

macOS 没有公开 API 控制单个显示器开关。本工具使用 4 个 CoreGraphics/SkyLight 私有函数：

| 函数 | 作用 |
|------|------|
| `CGSGetDisplayList` | 列出全部显示器槽位（含禁用的） |
| `CGSBeginDisplayConfiguration` | 开始配置事务 |
| `CGSConfigureDisplayEnabled` | 启用/禁用显示器（公开 API 无对应物） |
| `CGSCompleteDisplayConfiguration` | 提交配置（返回码不可信，以轮询状态为准） |

关键发现（来自原项目）：
- 内建屏被禁用后从公开 API 消失，只有 `CGSGetDisplayList` 保留槽位
- 所有物理屏消失时 macOS 会插入虚拟屏（vendor=`"unkn"`, model=`"virt"`）
- `CGSCompleteDisplayConfiguration` 经常返回 1001 但屏幕实际已生效

## 环境要求

- macOS（SkyLight/CoreGraphics 框架）
- Python 3.8+（系统自带）
- 无需 pip install

## 致谢

核心私有 API 调用来自 **[zy0816/ScreenOff](https://github.com/zy0816/ScreenOff)**（MIT License），作者 zy0816 <zyan980816@proton.me>。该项目还包含一个完整的菜单栏 App（Swift），有更完善的恢复链机制（三级恢复：enable → CGRestorePermanentDisplayConfiguration → sleepWake）。

本项目只提取了 CLI 部分，扩展了目标解析（按 ID/序号/名字），去掉了内建屏限制。

## License

MIT — see [LICENSE](LICENSE)