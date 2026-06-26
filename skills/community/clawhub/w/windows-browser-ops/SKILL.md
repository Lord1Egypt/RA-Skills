---
name: windows-browser-ops
description: Windows Desktop 浏览器远程操控。用于在 Discord / 本地会话中触发 Edge/Chrome 执行“打开网页、交互、截图、打包下载”等动作，并回传证据。
---

# Windows Browser Ops

## Overview
- 让 Desktop 节点把 Edge（或默认浏览器）当作“远程手”来执行导航、交互与取证。
- 典型使用场景：远程帮少爷打开网页截图、下载文件、在 Discord 演示浏览器操作。

## Prerequisites
1. Desktop 节点已 `openclaw devices approve` 并可通过 `tools.exec node=Desktop` 执行命令。
2. PowerShell 有权限运行本 skill 的脚本（默认位于 `skills/windows-browser-ops/scripts/`）。
3. Edge 已登录目标账号（若需），并允许运行图形界面命令。
4. RDP 会话保持解锁，确保截图与 UIAutomation 可用。

## Quick Start
| 需求 | 步骤 |
|------|------|
| 打开网页 + 截图 | 1) `launch_edge.ps1 -Url <网址>` 2) `focus_edge.ps1` 3) `capture_screenshot.ps1 -Output <路径>` 4) 把截图上传给少爷 |
| 下载文件并打包 | 1) 导航并执行下载 2) 等待 `.crdownload` 消失 3) `download_and_zip.ps1 -SourcePath "C:\\Users\\<USER>\\Downloads" -ZipPath %TEMP%\\edge-export.zip` 4) 上传 ZIP |

## Workflow Decision Tree
1. **识别类别**：
   - 只需打开/截图 → 走 "导航 + 取证" 路线。
   - 需填写表单/点击按钮 → 额外插入 UIAutomation / JS 注入步骤。
   - 需下载 → 加入“监控下载并打包”步骤。
2. **准备环境**：若 Edge 未运行先调用 `launch_edge.ps1`，再 `focus_edge.ps1`。
3. **执行动作**：根据请求选择脚本或自定义 PowerShell。
4. **取证 + 回传**：截图 / 保存日志 / 打包下载并上传。

## Task Guide
### 1. 启动 & 聚焦浏览器
1. `launch_edge.ps1 -Url <初始URL>`：若 Edge 未运行则启动（未来可扩展到 Chrome）。
2. `focus_edge.ps1`：调用 Win32 API 把 Edge 窗口置前。若失败，重启 Edge 并重试。

### 2. 导航与交互
- `edge_nav.ps1 -Url <目标>`：当前版本通过重新打开 Edge 导航，后续可换成 UIAutomation/DevTools。
- 复杂互动：使用 PowerShell `Add-Type -AssemblyName UIAutomationClient` 获取控件；参考 `references/edge_playbook.md` 中的片段。

### 3. 取证
- `capture_screenshot.ps1 -Output %TEMP%\\edge-shot.png` 捕捉全屏。必要时修改脚本以截取指定窗口。
- 若要导出 PDF，可在 Edge 使用 `Ctrl+P` + `Enter`（后续可通过 SendKeys/AutoHotkey 脚本扩展）。

### 4. 整理下载
1. 轮询 `Downloads`，等待 `.crdownload` 文件清空。
2. `download_and_zip.ps1 -SourcePath <下载目录> -ZipPath %TEMP%\\edge-export.zip`。
3. 上传 ZIP 并在回复中说明包含内容与时间戳。

## Scripts Reference
| 脚本 | 作用 | 备注 |
|-------|------|------|
| `scripts/launch_edge.ps1` | 启动 Edge 并可选导航到 URL | 需改进为检测执行路径 / 支持 Chrome |
| `scripts/focus_edge.ps1` | 调用 Win32 API 将 Edge 置前 | 后续可加入 ShowWindowAsync |
| `scripts/edge_nav.ps1` | 导航到目标 URL | 未来替换为 DevTools/automation |
| `scripts/capture_screenshot.ps1` | 全屏截图 | 当前抓取主屏；多屏需扩展 |
| `scripts/download_and_zip.ps1` | 打包下载目录 | 记得过滤旧文件 |

> Windows 本地实测时，将这些脚本复制到 `C:\Users\louis\openclaw-scripts\windows-browser-ops\`，并使用 WSL 跨环境调用：
>
> ```bash
> /mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe \
>   -File C:\Users\louis\openclaw-scripts\windows-browser-ops\edge_nav.ps1 \\
>   -Url "https://www.microsoft.com"
> /mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe \
>   -File C:\Users\louis\openclaw-scripts\windows-browser-ops\capture_screenshot.ps1 \\
>   -Output C:\Users\louis\Desktop\edge-shot.png
> /mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe \
>   -File C:\Users\louis\openclaw-scripts\windows-browser-ops\download_and_zip.ps1 \\
>   -SourcePath C:\Users\louis\Downloads \\
>   -ZipPath C:\Users\louis\Desktop\edge-downloads.zip
> ```

更多细节与扩展想法见 `references/api_reference.md` 与 `references/edge_playbook.md`。

## Troubleshooting
- **Edge 没有窗口句柄**：可能全部窗口最小化或在其他虚拟桌面，重新 `Start-Process msedge`。
- **截图全黑/空白**：确认远程会话未锁屏。必要时开启 `tscon` 让会话保持前台。
- **脚本执行策略阻止**：在 Desktop 节点上提前 `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`。
- **DevTools/自动化受限**：如需更稳定交互，考虑安装 AutoHotkey 或 Playwright，并在 references 中记录使用方式。
