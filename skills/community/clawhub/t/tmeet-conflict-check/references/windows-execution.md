# Windows x64 执行与验收

## 支持边界

- 官方 `tmeet` npm 包提供 `win32-x64` 产物；本模块的 Windows 支持范围限定为 Windows x64。
- 监测脚本需要 Python 3.9+；官方 CLI 的 npm 安装需要 Node.js 14+。
- Windows 不保证自带 IANA 时区数据。使用 `Asia/Shanghai` 等自定义时区前安装 `tzdata`。

## 安装与验证

在 PowerShell 中执行：

```powershell
npm install -g @tencentcloud/tmeet@latest
tmeet.cmd -V
py -3 -m pip install -r ".\scripts\requirements.txt"
& ".\scripts\test_windows.ps1"
```

需要连同 OAuth 和真实会议列表做只读冒烟测试时，先在前台执行 `tmeet.cmd auth login`，再运行：

```powershell
& ".\scripts\test_windows.ps1" -Live
```

`-Live` 只查询登录状态和未来 14 天会议，不创建、修改或取消会议。

## 即时冲突查询

不要把 Bash 的行尾 `\` 复制到 PowerShell。在 Windows x64 中将命令写成单行：

```powershell
tmeet.cmd meeting list --start "<ISO_START>" --end "<ISO_END>" --show-all-sub 1 --compact
```

分页、内部 ID 隐私和多结果确认规则与 `SKILL.md` 一致。

## 状态目录

将状态放在当前 Windows 用户的 LocalAppData，不依赖 POSIX `0600` 权限语义：

```powershell
$StateDir = Join-Path $env:LOCALAPPDATA "tmeet-conflict-check"
New-Item -ItemType Directory -Force -Path $StateDir | Out-Null
$StateFile = Join-Path $StateDir "conflict-watch.json"
```

## 常驻模式

```powershell
py -3 ".\scripts\watch_meeting_conflicts.py" --watch --state-file "$StateFile"
```

进程会休眠到当前时区下一个工作日整点/半点。宿主必须持续消费 stdout：空输出不创建 Agent 回合；只有 `meeting.conflict.detected` NDJSON 才唤醒 Agent。

## Windows 任务计划程序模式

对长运行进程不可靠的宿主，配置一个单次任务：

1. 程序设为 `py.exe`。
2. 参数设为 `-3 "<SKILL>\scripts\watch_meeting_conflicts.py" --state-file "<STATE>\conflict-watch.json"`。
3. 触发器设为周一至周五 09:00，每 30 分钟重复，持续 9 小时；覆盖 09:00–18:00（含 18:00）。
4. 设置“如果任务已在运行，则不启动新实例”。
5. 将 stdout 交给 Agent 宿主的事件适配器，或使用 `--event-file` 让宿主监听只在冲突时增长的 NDJSON 文件。

任务计划程序只负责运行脚本，不会自动把 stdout 转成 Agent 回合。如果宿主没有事件适配器，必须明确告知用户“只完成定时检查，未建立 Agent 主动提醒链路”。

## 自定义示例

```powershell
py -3 ".\scripts\watch_meeting_conflicts.py" --watch --timezone "Asia/Shanghai" --weekdays "1,2,3,4,5" --office-start "08:30" --office-end "19:00" --schedule-times "09:15,12:00,17:45" --state-file "$StateFile"
```

更改参数后重启常驻进程，或同步更新 Windows 任务计划程序的触发器与操作参数。
