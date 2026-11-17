---
name: windows-agent
description: 全能 Windows 桌面控制：看屏幕/截图/控窗口(移动缩放激活关闭启动)/模拟鼠标键盘/点按钮填框/UI自动化/管理进程。当用户说"看屏幕/看窗口/截图/帮我点/输入文字/控制程序/打开应用/操作窗口/最小化/最大化/移动窗口"时使用。
metadata:
  openclaw:
    os:
      - win32
---

# Windows Agent — 全能 Windows 桌面控制

一站式 Windows 桌面自动化：看、点、输、控。所有操作通过 PowerShell 脚本完成，无需节点/Tray 应用。

## 关键：脚本位置

所有脚本位于本 skill 目录下 `scripts/`，用 **pwsh**（PS7）执行：

```
脚本目录: `{baseDir}/scripts`（即 workspace/skills/windows-agent/scripts）
```

执行方式（统一）：
```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File "{baseDir}/scripts/<脚本>.ps1" -Action <动作> [参数]
```

⚠️ 用 `pwsh`（不是 `powershell`，避免 GBK 编码问题）。

> ⚠️ **使用前先读**：[`PREREQUISITES.md`](PREREQUISITES.md)（前置条件 & 注意事项）——含各板块必须满足的前提、坐标语义、避坑速查。

## 安全规则

1. **关窗口/结束进程前**：先确认是否有未保存内容
2. **发输入前**：确保正确窗口已激活（先 focus）
3. **覆盖剪贴板前**：提醒用户
4. **点击/输入可能造成破坏性操作**（删除、提交、发送）→ 先确认

---

## 🎯 常用任务指引（用户想做事 → 照此调用，必然正确）

> 覆盖最常见的自动化需求。每项都是能跑通的完整序列，含避坑。

| 用户想做什么 | 正确调用序列 |
|-------------|-------------|
| 看屏幕/了解现状 | `vision.ps1 -Action observe` → 用 image 工具看图 |
| 点某个应用/按钮 | `window list-windows`/`uiauto dump` 定位 → `uiauto find-text` 拿物理坐标 → `input mouse-click` 或 `uiauto click` |
| 打开一个应用/此电脑 | `window.ps1 -Action open -Target "名称"`（自动走 shell/开始菜单lnk/桌面lnk/**UWP(计算器/设置等)**/UIA/截图兜底, 不碰坐标）|
| 拖一个东西(文件/内容) | `uiauto find-text` 拿起点坐标 → `input mouse-drag` 或 `batch "drag..."`（**移动窗口推荐用 window.ps1 move**(API, 保留尺寸); mouse-drag 主要拖内容/文件/滑块） |
| 输入/打字(含中文) | `window focus` 目标 → `input type-text -Text "...请"`(SendInput Unicode 不乱码) |
| 多次操作/批量 | 一次 `batch.ps1 -Sequence "move...;click...;drag..."`(省64%) |
| 等窗口/加载完成 | `wait.ps1 -Action window -Target "标题"`(或 text/control) |
| 读窗口文本 | `read-text.ps1 -Action read -Target "标题"`(UWP编辑区除外) |
| 复制/粘贴 | `clipboard.ps1 get` 备份 → `set` → 用完 `clear` 或恢复 |
| 看进程/杀进程 | `process list` 查 PID → `info` → `kill -ProcId`(勿随手杀) |

---

## ⚡ 核心避坑速查（调用前扫一眼）

| 坑 | 正确做法 |
|----|---------|
| 点偏/点错 | 坐标用 `uiauto find-text` 的**物理坐标**，勿用截图逻辑坐标(偏DPI) |
| 移动窗口尺寸稳定 | 移动窗口推荐 `window.ps1 move`(API,保留尺寸)；mouse-drag 拖标题栏曾观测到 Size 变化(根因未证实,不断言最大化), 移动窗口用 move 更稳 |
| 只做单次操作慢 | 单次 `input.ps1` 即可；**多次用 `batch.ps1`**(一次做多个) |
| 找不到窗口/控件 | 先 `uiauto dump`/`window list-windows` 看实际标题, 再 `find-text` |
| Electron 应用(OpenClaw Control) | UIA 读不到/坐标乱 → `vision` 截图兜底 |
| UWP 记事本编辑区 | read-text 读不到内容(平台限制) → 读菜单/标题文本或 vision 截图 |
| process 报 Missing -ProcId | info/monitor/wait 需要 `-ProcId`, 先 `list` 查 PID |
| vision 报错 | 用 `-Action observe`(不是 screenshot) |
| clipboard 覆盖用户内容 | set/clear 前先 `get` 备份原内容, 用后恢复 |

---

## 板块总览

| 板块 | 脚本 | 能力 |
|------|------|------|
| ① 视觉看屏 | `vision.ps1` | 截图 → 自动视觉模型看图，返回画面描述（"看屏幕"首选）|
| ② 窗口管理 | `window.ps1` | 列/激活/移动/缩放/最小化/最大化/还原/关闭/启动/分屏/置顶 |
| ③ 输入模拟 | `input.ps1` | 鼠标点击/移动/滚动/按下释放(down/up)、键盘输入/按键/组合键 |
| ④ 屏幕截图 | `screen.ps1` | 全屏/窗口/区域截图，存成图片文件 |
| ⑤ UI自动化 | `uiauto.ps1` | UIAutomation 读控件树/定位(含按文本)/点击/填文本框/滚动窗口内容 |
| ⑥ 进程管理 | `process.ps1` | 列表/信息/启动/结束/监控 |
| ⑦ 输入拖拽 | `input.ps1 -Action mouse-drag` | 从 A 拖到 B（拖文件/滑块/窗口） |
| ⑧ 智能等待 | `wait.ps1` | 等待窗口/文本/控件出现（自动化节奏关键） |
| ⑨ 读窗口文本 | `read-text.ps1` | UIA 提取窗口真实文本（比 OCR 快准）|
| ⑩ 剪贴板 | `clipboard.ps1` | 读/写/清空剪贴板（set-get-clear）|
| ⑪ 批量输入 | `batch.ps1` | **多次鼠标/键盘操作一次做**(省64%)，命令 move/click/drag/type/keys/scroll/delay |

**推荐流程（完整闭环，沿此走即正确）**：
1. **看屏幕** → `vision.ps1 -Action observe`（先知道屏幕现状；OpenClaw Control 等 Electron 窗口 UIA 读不到 → 用 vision 截图兜底）
2. **定位** → 窗口用 `window.ps1 -Action list-windows`；控件/坐标用 `uiauto.ps1 -Action dump`/`find-text`（返回**物理坐标**，**千万别用截图逻辑坐标**）
3. **操作** → 单次用 `input.ps1`（点击/按键/拖拽）；**多次操作用 `batch.ps1`**（一次做多个，省64%）
4. **等加载** → `wait.ps1` 等窗口/文本/控件出现
5. **验证** → 再 `vision.ps1` 截屏确认结果
6. **避坑**：坐标一律用 uiauto 物理坐标；`process` 的 info/monitor/wait 需 -ProcId；`clipboard` set/clear 前先 get 备份；UWP 记事本编辑区 read-text 读不到(用菜单/标题文本)

---

## ① 视觉看屏 vision.ps1

截图并用视觉模型描述画面。**"看屏幕"第一入口。**

```powershell
# 截图+视觉描述（最常用）
pwsh ...\vision.ps1 -Action observe

# 只看某窗口
pwsh ...\vision.ps1 -Action observe-window -Target "Notepad"

# 只看某区域 (x,y,w,h)
pwsh ...\vision.ps1 -Action observe -RegionX 100 -RegionY 100 -RegionWidth 800 -RegionHeight 600
```

> 说明：`observe` 会截屏 → 调用视觉模型（你配置的视觉模型）→ 返回"画面里有什么"的文字描述，供我理解当前屏幕状态后决定下一步操作。

### ⚠️ 最小化窗口的截法（重要）

**最小化窗口截不到完整内容**（Windows CopyFromScreen 只能截屏幕可见区域，最小化窗口只剩任务栏缩略条，如 237x39 小图）。
**遇到最小化窗口要先还原可见 → 截图 → 再复原（恢复最小化）**，全程不新开应用：

```powershell
# ① 还原窗口(临时变可见)
pwsh ...\window.ps1 -Action restore -Target "Edge"
# ② 截图(此时可见, 截到完整页面)
pwsh ...\vision.ps1 -Action observe-window -Target "Edge"
# ③ 复原(恢复最小化)
pwsh ...\window.ps1 -Action minimize -Target "Edge"
```

> 原则：测/用 `observe-window` 优先用**屏幕上已可见的现有窗口**当目标，**绝不为截图新开应用**；目标是最小化窗口时按上面 restore→截→minimize 处理，用完恢复原状态不留残留。

## ② 窗口管理 window.ps1

```powershell
# 列出所有可见窗口（PID/状态/位置/大小/标题）
pwsh ...\-windows

# 激活/前置某窗口（可按标题模糊匹配或 PID）
pwsh ...\window.ps1 -Action focus -Target "Notepad"
pwsh ...\window.ps1 -Action focus -ProcId 1234

# 启动应用
pwsh ...\window.ps1 -Action launch -Target "notepad"
pwsh ...\window.ps1 -Action launch -Path "E:\app\app.exe" -Arguments "arg"

# 智能打开（按名字，不靠猜坐标，六级确定性链路）
pwsh ...\window.ps1 -Action open -Target "网易发烧游戏"
#   ①a shell 系统项 → explorer shell:... 直开（此电脑/控制面板/回收站等，零鼠标零坐标）
#   ①b 开始菜单 .lnk → 用户+公共开始菜单扫描直启
#   ①  桌面 .lnk → 桌面快捷方式直启
#   ②  桌面图标 UIA → 枚举桌面图标物理坐标双击（UIA 不稳, 重试3次）
#   ②b 任务栏图标 UIA → 枚举任务栏按钮物理坐标单击激活（UIA 不稳, 重试3次）
#   ③  截图兜底 → 输出截图路径供视觉定位后点击
pwsh ...\window.ps1 -Action open -Target "此电脑"   # 走 ①a shell 直开，不碰坐标
pwsh ...\window.ps1 -Action open -Target "微信"     # 走 .lnk 直启

# 读当前鼠标物理坐标（配合精准点击）
pwsh ...\input.ps1 -Action get-pos

# 移动/调整大小
pwsh ...\window.ps1 -Action move -Target "Notepad" -X 100 -Y 100
pwsh ...\window.ps1 -Action resize -Target "Notepad" -Width 800 -Height 600

# 最小化/最大化/还原/关闭
pwsh ...\window.ps1 -Action minimize -Target "Notepad"
pwsh ...\window.ps1 -Action maximize -Target "Notepad"
pwsh ...\window.ps1 -Action restore -Target "Notepad"
pwsh ...\window.ps1 -Action close -Target "Notepad"

# 按位置分屏
pwsh ...\window.ps1 -Action snap -Target "Notepad" -Position left

# 窗口置顶 / 取消置顶 (默认 toggle 切换)
pwsh ...\window.ps1 -Action topmost -Target "Notepad"
#   置顶:    -State on
#   取消置顶: -State off
#   切换(默认)

# Win 键组合 (input.ps1, keybd_event 真 Win 键, 不再是假 Ctrl+Esc)
pwsh ...\input.ps1 -Action send-keys -Keys "Win+D"   # 显示桌面
pwsh ...\input.ps1 -Action send-keys -Keys "Win+R"   # 运行
pwsh ...\input.ps1 -Action send-keys -Keys "Win+Shift+S"  # 截图 (暂仅单键, 组合另议)
```

## ③ 输入模拟 input.ps1

```powershell
# 输入文字（需先激活目标窗口）
pwsh ...\input.ps1 -Action type-text -Text "hello world"

# 发送按键/组合键
pwsh ...\input.ps1 -Action send-keys -Keys "ctrl+c"     # 复制
pwsh ...\input.ps1 -Action send-keys -Keys "enter"
pwsh ...\input.ps1 -Action send-keys -Keys "alt+tab"

# 鼠标点击/移动/滚动
pwsh ...\input.ps1 -Action mouse-click -X 500 -Y 300 -Button left
pwsh ...\input.ps1 -Action mouse-click -X 500 -Y 300 -DoubleClick
pwsh ...\input.ps1 -Action mouse-move -X 500 -Y 300
pwsh ...\input.ps1 -Action mouse-scroll -Clicks -3
pwsh ...\input.ps1 -Action mouse-down -Button left     # 按住(配合 mouse-up 做精确拖拽)
pwsh ...\input.ps1 -Action mouse-up -Button left       # 松开
pwsh ...\input.ps1 -Action get-pos                      # 读当前鼠标物理坐标(x,y)
```

## ④ 屏幕截图 screen.ps1

```powershell
# 全屏截图
pwsh ...\screen.ps1 -Action capture -OutputPath "E:\OpenClawData\shots\s.png"

# 窗口截图
pwsh ...\screen.ps1 -Action capture-window -Target "Notepad" -OutputPath "..."

# 区域截图
pwsh ...\screen.ps1 -Action capture-region -X 0 -Y 0 -Width 800 -Height 600 -OutputPath "..."

> ⚠️ **尺寸语义**：截图输出为【逻辑坐标】(本机 1707x1067)。鼠标/坐标点击用【物理坐标 2560x1600】——
> 用截图坐标喂 input.ps1 会偏 DPI 系数。目标坐标一律用 `uiauto.ps1 find-text/click-text` 返回的物理坐标。
```

## ⑤ UI自动化 uiauto.ps1（UIAutomation）

```powershell
# 读取前台窗口的控件树（名称/类型/坐标/是否可用）
pwsh ...\uiauto.ps1 -Action dump

# 按名称找控件并返回坐标
pwsh ...\uiauto.ps1 -Action find -Name "确定"

# 点击指定名称的按钮
pwsh ...\uiauto.ps1 -Action click -Name "确定"

# 向文本框填入文字
pwsh ...\uiauto.ps1 -Action set-text -Name "用户名" -Text "abc"

# 按 AutomationId 操作
pwsh ...\uiauto.ps1 -Action click -AutomationId "btnSave"

# 聚焦目标窗口后再操作
pwsh ...\uiauto.ps1 -Action click -Name "确定" -Target "Notepad"

# 滚动窗口/列表/长页内容 (ScrollPattern, 原生)
#   Direction: up/down/left/right；Amount: page(整页)/line(一行)/top/bottom/max
pwsh ...\uiauto.ps1 -Action scroll -Target "文件管理器" -Direction down -Amount page
pwsh ...\uiauto.ps1 -Action scroll -Target "Notepad" -Direction down -Amount line

# 调用控件默认动作(如按钮点击/勾选)
pwsh ...\uiauto.ps1 -Action invoke -Name "确定" -Target "Notepad"

# 按文本内容定位元素中心坐标(返回 center=(x,y), 配合 input 精准点击)
pwsh ...\uiauto.ps1 -Action find-text -Target "Notepad" -Text "搜索"

# 按文本内容直接点击(InvokePattern或坐标中心, SendInput精准)
pwsh ...\uiauto.ps1 -Action click-text -Target "Notepad" -Text "文件"
```

## ⑥ 进程管理 process.ps1

```powershell
pwsh ...\process.ps1 -Action list [-Name filter] [-SortBy memory] [-Top 10]
pwsh ...\process.ps1 -Action info -ProcId 1234
pwsh ...\process.ps1 -Action start -Path "app.exe" [-Arguments "..."]
pwsh ...\process.ps1 -Action kill -ProcId 1234 [-Force]
pwsh ...\process.ps1 -Action monitor -ProcId 1234 -Duration 10
pwsh ...\process.ps1 -Action wait -ProcId 1234        # 等待进程退出(阻塞)

> ⚠️ **info / monitor / wait 需 `-ProcId`**（不支持 -Name）。不知道 PID 时先用 `list` 查到再调用。
```

## ⑦ 输入拖拽 input.ps1 -Action mouse-drag

```powershell
# 从 (X,Y) 拖到 (X2,Y2)（拖文件/滑块/移动窗口）
pwsh ...\input.ps1 -Action mouse-drag -X 100 -Y 100 -X2 400 -Y2 300
```

## ⑧ 智能等待 wait.ps1

```powershell
# 等窗口出现（最长 30s）
pwsh ...\wait.ps1 -Action window -Target "记事本"

# 等某文本出现（限窗口）
pwsh ...\wait.ps1 -Action text -Text "完成" -Window "安装程序"

# 等控件出现
pwsh ...\wait.ps1 -Action control -Target "确定" -Window "对话框" [-Timeout 60]
```

## ⑨ 读窗口文本 read-text.ps1

```powershell
# 读某窗口全部真实文本（UIA 提取，比 OCR 快准）
pwsh ...\read-text.ps1 -Action read -Target "Notepad"
# 不指定 Target 则读当前前台窗口
pwsh ...\read-text.ps1 -Action read
```

## ⑩ 剪贴板 clipboard.ps1

```powershell
# 读剪贴板内容
pwsh ...\clipboard.ps1 -Action get

# 写入文本到剪贴板
pwsh ...\clipboard.ps1 -Action set -Text "要复制的内容"

# 清空剪贴板
pwsh ...\clipboard.ps1 -Action clear
```

## ⑪ 批量输入 batch.ps1（高效: 一次启动+编译做多个操作）

> 相比多次调用 input.ps1(每次 ~850ms 启动+编译), 批量做 N 个鼠标/键盘操作只付一次成本。
> **多次鼠标操作/拖拽首选此方式**——实测 4 操作快 64%, 单次 drag 236ms(vs 850ms)。

```powershell
# 内联序列(分号或换行分隔)
pwsh ...\batch.ps1 -Sequence "move 632 980; click 632 980; drag 632 980 632 1442"

# 或用命令文件(每行一条)
pwsh ...\batch.ps1 -SequenceFile "E:\ops.txt"
```

**命令**（每行一条, 空格分隔参数）:
| 命令 | 参数 | 说明 |
|------|------|------|
| `move` | `<x> <y>` | 移动鼠标(物理坐标) |
| `click` | `<x> <y> [left\|right\|middle] [dbl]` | 点击 |
| `drag` | `<x1> <y1> <x2> <y2>` | 拖拽(自适应段数, 快) |
| `type` | `<文本>` | 输入文字/中文(SendInput Unicode) |
| `keys` | `<组合键>` | 按键(Ctrl+S/Alt+F4/Enter...) |
| `scroll` | `<n>` | 滚动(正=上,负=下) |
| `delay` | `<毫秒>` | 等待 |

> ⚠️ 坐标一律用 **uiauto find-text 物理坐标**(同 input.ps1)。

## 排错

- 脚本没反应：确认用 `pwsh` 且路径正确
- 窗口找不到：先 `-windows` 看确切标题
- 点不到控件：先 `uiauto.ps1 -Action dump` 读控件树拿坐标，或截图 vision 确认
- 中文乱码：脚本用 UTF-8，执行用 pwsh
- 视觉模型不动：确认你配置的视觉模型可用
