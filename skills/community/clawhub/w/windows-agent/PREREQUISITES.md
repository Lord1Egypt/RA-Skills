# windows-agent — 使用前置条件 & 注意事项

> 本文件说明**正常使用本 skill 必须满足的前提**与**调用时的关键注意点**，避免"调用就出错"。
> 调用前先确认这些条件，即可流畅使用全部板块。

---

## 〇、使用前说明（请先读）

- **本 skill 是公开发布的 Windows 桌面自动化工具**，可在自己的机器上自由安装使用。
- **不包含任何密钥 / API Key / 账号信息。** 需要的视觉模型由**使用者自己配置**（见下方 ① vision 依赖）。
- **不联网、不上传任何数据**：全部操作都在本机完成（鼠标/键盘/窗口/进程/截图）。
- **截图默认保存位置**：脚本会优先探测当前 OpenClaw 环境允许的可写目录；你也可以通过 `-OutputPath` **自由指定任意保存路径**（每个截图脚本都支持）。发布者本地曾用 `E:\OpenClawData\.openclaw\workspace`，但这只是示例——**你的机器上完全可以用你自己的目录**。
- **执行方式**：下面所有示例中的 `...\` 代表脚本所在目录（本 skill 的 `scripts/`）。你把 skill 装到哪，就用哪的路径；脚本相互调用已用相对路径，**不需要手动改任何脚本**。

---

## 一、全局前置条件（所有板块通用）

| 前提 | 要求 | 说明 |
|------|------|------|
| **PowerShell 7 (pwsh)** | ✅ 必装 | 所有脚本一律用 `pwsh -NoProfile -ExecutionPolicy Bypass -File` 执行（**勿用 powershell.exe 5.1**，会 GBK 中文乱码）|
| **路径** | 脚本目录 `{baseDir}/scripts` | 执行前确认本 skill 完整存在 |
| **Windows 版本** | ✅ Win10/11 | 依赖系统自带的 user32.dll / .NET / UIAutomation，**无需额外安装任何组件** |
| **编码** | 文件 UTF-8，执行用 pwsh | 脚本已统一 UTF-8；用 pwsh 执行即无乱码 |
| **桌面必须登录** | 用户已登录桌面会话 | 无头/锁屏时鼠标、窗口操作无效 |

> 💡 **PWsh 未装？** 脚本会自动探测：优先用 PATH 里的 `pwsh`；找不到再找 `C:\Program Files\PowerShell\7\pwsh.exe`。安装 PowerShell 7 见 microsoft.com/powershell。

---

## 二、板块逐个前置条件

### ① vision.ps1 — 视觉看屏
- **依赖**：需要你的 OpenClaw/客户端配置一个**可用的视觉模型**（能读图的模型即可）。用你自己配置的任何视觉模型都行。
- **注意**：`observe` 截图后输出 `IMAGE_READY:<路径>`，此时用你客户端的**看图工具/视觉模型**分析该图片即可了解屏幕内容。
- **最小化窗口**：`observe-window` 会自动处理（还原→截→复原最小化），不用手动干预。

### ② window.ps1 — 窗口管理
- **前置**：`open` 依赖开始菜单/桌面 `.lnk` 存在、或能走 shell 系统项（此电脑/控制面板）
- **注意**：动作名是 **`list-windows`**（不是 `list`）
- **UWP/商店应用**（计算器/设置等）：`open` 已内置支持（Get-StartApps 探测），直接按名字打开即可

### ③ input.ps1 — 输入模拟
- **关键前置**：鼠标点击/移动的坐标必须是**【物理坐标】**（即当前屏幕分辨率的真实像素，如 2560×1600），**不能喂截图返回的逻辑坐标**（会因 DPI 缩放偏位）
- **坐标来源**：用 `uiauto.ps1 find-text/click-text` 返回的物理坐标（脚本已自动处理），或 UIA `BoundingRectangle`
- **发文字前**：先 `focus` 目标窗口
- `get-pos` 可回读当前鼠标物理坐标用于验证

### ④ screen.ps1 — 屏幕截图
- **关键**：截图返回的是【逻辑坐标】尺寸。**仅供视觉分析，不可直接喂给鼠标点击**（会偏 DPI 系数）
- **输出路径**：`-OutputPath` 可自定义任意目录；不指定时探测默认可写目录

### ⑤ uiauto.ps1 — UI 自动化
- **前置**：目标窗口须能被 UIA 访问（标准 Win32/WPF 应用 ✅）
- **注意**：坐标点击/填字已内建调用 input 的 SendInput 精准能力（自动用物理坐标）
- **Electron/CEF 应用**（如部分控制台）：UIA 树可能不完整 → 用 `vision` 截图兜底
- UIA 桌面/任务栏图标枚举**不稳定**（Windows 限制），`open` 已有重试，极端情况落截图兜底

### ⑥ process.ps1 — 进程管理
- **前置**：无额外依赖
- `kill` 前确认目标（破坏性操作）

### ⑦ input.ps1 -Action mouse-drag — 拖拽
- **前置**：起止坐标须为物理坐标
- 平滑 20 段移动，避免被识别为点击

### ⑧ wait.ps1 — 智能等待
- **前置**：目标窗口/文本须能被 UIA/窗口枚举访问
- 默认超时 30s，可 `-Timeout` 调整

### ⑨ read-text.ps1 — 读窗口文本
- **前置**：目标窗口须能被 UIA 提取文本（标准应用 ✅；Electron/自定义渲染可能读出为空）

### ⑩ clipboard.ps1 — 剪贴板
- **注意**：`set` 会覆盖剪贴板，覆盖他人内容前先确认；用后建议 `clear`

### ⑪ batch.ps1 — 批量输入
- **前置**：同 input.ps1（物理坐标、pwsh）
- **高效场景**：一次启动做多个鼠标/拖拽/打字操作（省 ~64%）；单次拖拽也更快
- **坐标**：同上, 用 uiauto 物理坐标

---

## 三、最容易踩的坑（速查）

| 坑 | 正确做法 |
|----|---------|
| `window.ps1 -Action list` ❌ | `-Action list-windows` |
| `vision.ps1 -Action screenshot` ❌ | `-Action observe` |
| 截图逻辑坐标喂鼠标 ❌ | 用 UIA 返回的物理坐标 |
| 用 powershell.exe(5.1) 跑脚本 ❌ | 用 pwsh（脚本已内置路径探测）|
| 填中文经 SendKeys ❌ | input type-text / uiauto set-text（已内建 Unicode）|

---

## 四、环境确认命令

```powershell
# 确认 pwsh 版本(应 ≥7)
pwsh -NoProfile -Command "$PSVersionTable.PSVersion"

# 确认脚本目录完整 (换成你自己的 skill 安装路径)
Get-ChildItem {你的安装路径}/scripts/*.ps1

# 每个脚本自检方法
pwsh -NoProfile -File <脚本>.ps1 -Action help   # 打印完整用法 + 注意事项
```
