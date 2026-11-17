# Windows 事件日志检测规则（元察 · 元）

分析 Windows 事件日志（Security / System 等通道）中的登录、账户管理、审计与进程活动。
本文件说明元察的 winevt 检测规则、EventID 语义与阈值，供人工复核与调参。
EventID 语义对照微软 Windows Security Auditing 官方参考与 Sigma 社区检测惯例（借鉴规则语义、
字段选择与 level 分级，自研零依赖实现；不引入 Sigma 规则库或转换器，不逐字复制规则文本）。

## 输入形态

元察按「一行一条事件记录」读取。EVTX 二进制日志请先导出为文本（支持 key=value、wevtutil 文本、
XML 单行三种形态），例如：

```bash
# key=value（推荐，信息密度高）
wevtutil qe Security /q:"*[System[(EventID=4625 or EventID=4624)]]" /f:text
Get-WinEvent -FilterHashtable @{LogName='Security'} -MaxEvents 1000 | Export-Csv sec.csv

# XML 单行（每行一条事件）
wevtutil qe Security /f:xml
```

典型行（key=value，每行一条事件）：

```
EventID=4625 ProviderName=Microsoft-Windows-Security-Auditing LogName=Security
TimeCreated=2026-08-27T08:01:01.000Z EventRecordID=201
TargetUserName=admin WorkstationName=WS01 IpAddress=198.51.100.7 LogonType=3
An account failed to log on
```

引擎通过 `EventID=` / `ProviderName=` / `LogName=` / `EventRecordID=` /
`Microsoft-Windows-Security-Auditing` / `Security ID` / `<Event` 等标记自动嗅探 winevt 类；
Event 4104 / 4103 PowerShell 脚本块记录仍走 powershell 检测（避免与 winevt 抢判）。
也可用 `--type winevt` 强制指定。

## EventID 语义与检测规则

| EventID | 语义 | 规则 | 触发条件 | 默认严重度 | 说明 / 复核建议 |
|---|---|---|---|---|---|
| 4625 | 登录失败 | brute_force | 同来源失败次数 >= `--max-fail`（默认 5）或时间窗内达标 | low→high | 暴力破解；核实来源、临时封禁、检查弱口令 |
| 4625 | 登录失败 | credential_stuffing | 同来源尝试 2 个及以上不同用户名 | high | 撞库 / 用户名枚举 |
| 4624 | 登录成功 | abnormal_login | 同来源先失败（4625）后成功 | high | 爆破成功后接管；立即核查会话、重置口令 |
| 4624 | 登录成功 | rdp_logon | Logon Type 10（远程交互 / RDP） | medium | 远程接管迹象；核对来源与账号 |
| 4624 | 登录成功 | admin_logon | 账号为 Administrator / root | medium | 管理员直登；来源非预期时重点核查 |
| 4720 | 账户创建 | account_created | 出现 4720 | high | 后门账户；核对创建者，可疑即禁用 |
| 4726 | 账户删除 | account_deleted | 出现 4726 | high | 清理痕迹 / 破坏操作 |
| 4740 | 账户锁定 | account_locked | 出现 4740 | medium | 连续失败触发；结合 4625 定位来源 |
| 4732 / 4728 | 组成员添加 | group_member_add | 出现 4732 / 4728；组名含 admin → high | medium~high | 权限维持 / 提权迹象 |
| 1102 | 审计日志清空 | audit_log_cleared | 出现 1102 | critical | 攻击后抹除痕迹；立即核查转发 / 备份 |
| 4688 | 进程创建 | suspicious_process | 映像 / 命令行命中可疑特征（见下） | low~critical | 下载执行、编码命令、凭据窃取、持久化 |
| 7045 | 新服务安装 | service_installed | 出现 7045 | medium | 服务持久化；核对服务名与可执行路径 |
| 4698 | 计划任务创建 | task_created | 出现 4698 | medium | 计划任务持久化；核对任务动作与触发条件 |

> 同一条事件可能同时命中多条规则（如 4624 同时触发 rdp_logon + admin_logon + abnormal_login），
> 这是正常行为，便于逐条复核，不影响时间线去重。

## 可疑进程特征（EventID 4688）

| 特征 | 默认严重度 | 说明 |
|---|---|---|
| mimikatz / lsass / procdump | critical~high | 凭据窃取 / 内存转储 |
| downloadstring / frombase64string / -enc / -windowstyle hidden | high | 下载执行 / 编码命令 / 隐藏窗口执行 |
| mshta / certutil -urlcache / regsvr32 /s / rundll32 javascript / bitsadmin /transfer | high | LOLBin 远程加载 / 下载执行 |
| powershell / pwsh / cmd /c / wscript / cscript / schtasks /create / sc create | medium | 脚本宿主 / 持久化命令 |
| whoami / taskkill /f / net user | low~medium | 侦察 / 账户管理（需结合上下文） |

## 阈值与调参

- 4625 聚合复用 `--max-fail` 与 `--window`（与 auth 一致）；调低更敏感、调高更稳健。
- 4688 可疑进程按特征固定严重度；噪音多时可结合 `--min-severity` 只关注 high / critical。
- 检测依赖日志侧审计策略已开启：账户登录（4624/4625）、账户管理（4720/4726/4740）、
  进程创建（4688）、安全日志清空（1102）。

## 复核建议

- 4624 / 4625 先核对来源是否为公司 / 运维跳板 IP，再判定异常；
- 1102（日志清空）与 4720（账户创建）优先级最高，优先排查；
- 4688 命中需结合父进程、命令行与业务合理性判断（正常运维也会用 PowerShell / cmd）；
- 无来源 IP 的事件（如 4720 / 1102）按账号 / 工作站 / 时间关联，必要时人工回溯域控日志。
