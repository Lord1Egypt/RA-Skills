# Edge Automation Playbook

## Default Paths
- Edge 可执行：`C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`
- 下载目录：`C:\Users\<USER>\Downloads`
- 临时截图目录：`%TEMP%\\edge-shot.png`

## 常用 Powershell 片段
- 启动 Edge（隐身模式）：`Start-Process msedge "--inprivate https://example.com"`
- 关闭所有 Edge：`Get-Process msedge | Stop-Process`
- 清理 Edge 缓存：`RunDll32.exe InetCpl.cpl,ClearMyTracksByProcess 8`

## UIAutomation 入口
- 依赖 `UIAutomationClient` 程序集 (`Add-Type -AssemblyName UIAutomationClient`)
- 获取地址栏：`$window.FindFirst(TreeScope::Subtree, New-Object PropertyCondition($AutomationElement::NameProperty, "Address and search bar"))`
- 发送文字：`$valuePattern.SetValue($Url)`

## 截图与取证
1. 使用 `Graphics.CopyFromScreen` 捕捉全屏 → `capture_screenshot.ps1`
2. 若只需浏览器窗口，可在脚本中获取 Edge 窗口矩形 (`[System.Windows.Forms.Screen]::AllScreens` + `Get-Process msedge`).
3. 回传：`openclaw message send --channel discord ... --file path`。

## 下载文件打包
1. 等待下载完成：轮询 `Downloads` 目录里 `.crdownload` 文件消失。
2. 执行 `download_and_zip.ps1 -SourcePath "C:\Users\<USER>\Downloads" -ZipPath "$env:TEMP\\edge-export.zip"`
3. 上传 ZIP。可在上传前过滤最近修改时间，避免旧文件混入。

## 常见问题
| 症状 | 处理 |
|------|------|
| Edge 没有窗口句柄 | 可能是所有窗口都在后台或多桌面，需 `Start-Process msedge` 重新开一个可见窗口。 |
| SetForegroundWindow 失败 | 同一线程限制，需先 `ShowWindowAsync`。可以在 `focus_edge.ps1` 中补充。 |
| 截图全黑 | 检查是否在 RDP 会话锁定状态；必要时使用 `psr.exe /start` 或 `SnippingTool /clipmode`. |

## 实测记录（2026-03-15）
- `launch_edge.ps1 -Url https://www.bing.com` → 首次启动成功；重复执行时返回 “Edge already running; no relaunch.”
- `focus_edge.ps1` → “Focused existing Edge window”。
- `edge_nav.ps1 -Url https://www.microsoft.com` → “Navigated Edge to …”。
- `capture_screenshot.ps1 -Output C:\Users\louis\Desktop\edge-shot.png` → 成功生成截图。
- `download_and_zip.ps1 -SourcePath C:\Users\louis\Downloads -ZipPath C:\Users\louis\Desktop\edge-downloads.zip` → “Zipped downloads to …”。
