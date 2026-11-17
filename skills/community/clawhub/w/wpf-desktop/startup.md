# 自启部署与排查

适用于 WPF 普通／管理员登录自启、单文件路径异常、计划任务和设置状态不一致。先读取现有实现、日志与任务定义，再决定修复。这里的自启指用户登录后启动桌面应用；机器启动时、无人登录的后台工作需要另行设计，不能直接套用交互式托盘任务。

## 默认维护检查

新建与通用维护按下表检查自启需求，不必等用户报错；专项修复沿受影响路径检查，只读评估只报告差距。

确需管理员常驻或用户明确要求时，在授权维护范围内补齐可选开关、状态回读、注册／修复／卸载、取消与失败反馈，并同步本地化和用户文档。已有实现优先修复，避免叠加注册器。

## 选择权限与部署方式

区分 Windows 机制、部署建议和产品策略。普通进程不能直接注册最高权限任务，应由提权的安装器或注册 helper 完成；`HighestAvailable` 不会让标准账户凭空获得管理员权限。[任务权限上下文](https://learn.microsoft.com/windows/win32/taskschd/security-contexts-for-running-tasks)

| 产品需求 | 实现与部署选择 |
| --- | --- |
| 普通托盘自启，偶尔需要管理操作 | 当前用户权限自启，管理操作按需提升。保留现有 Run／启动文件夹等合适机制。 |
| 长期操作管理员窗口、处理管理员前台输入，或明确要求管理员自启 | 使用该管理员用户的交互式登录任务和最高可用权限；支持便携／按用户安装形态。 |
| 一次性工具，无常驻需求 | 不增加登录自启。 |

**路径策略**：便携单文件可从用户可写目录经 UAC 注册，不以 `StartsWith(ProgramFiles)`、可信所有者或完整父目录 ACL 检查作为通用门槛，也不增加每次启动的路径警告或自动修改 ACL。高权限任务执行可被普通权限替换的程序有代码替换风险；在用户文档说明，并提供受保护部署或受保护 helper 作为可选方案。

检查应用 AGENTS.md、注释、保存逻辑和提示文案：把受保护目录写成 Windows／WPF 硬要求的，纠正说明；若是明确产品策略，说明策略归属、具体风险和修复选项，并遵循用户选择。不要擅自添加或移除该策略，也不要把管理员自启降级成普通自启。提示示例：「需要管理员账户；开启时可能需要同一账户的 UAC 授权。便携模式的计划任务仍保存在本机。」

### 账户资格与当前权限

设置页判断「本账户能否同账户提升」，helper 判断「本进程是否已提升」，两者不能混用。UAC 受限令牌中管理员 SID 为 Deny-Only，`WindowsIdentity.Groups` 会过滤它，`WindowsPrincipal.IsInRole(Administrator)` 也不会将它算作启用组；结果为 false 不足以判定本账户是标准用户。[.NET 10 实现](https://github.com/dotnet/runtime/blob/v10.0.0/src/libraries/System.Security.Principal.Windows/src/System/Security/Principal/WindowsIdentity.cs)

需要前置资格检查时，复用模板 `ElevatedStartup.IsAdministratorAccount()` 或现有等价实现：查询 `GetTokenInformation(TokenElevationType)`；`Limited (3)` 表示受限分割令牌，`Full (2)` 表示已提升，`Default (1)` 表示没有关联令牌，需结合 `IsInRole` 判断，不能直接视作标准用户。[令牌类型](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ne-winnt-token_elevation_type)

模板布尔结果为保守判断，false 不能细分标准账户与检测失败；需要明确原因时补充检测诊断。资格检查不保证 UAC 获批或注册成功，helper 仍需校验实际权限与请求者 SID。

### 受保护部署与更新

- 安装器方案见 [项目起手与发布配置](project-setup.md) 的 Inno Setup 权限配置。默认 ACL 正确的 `Program Files` 是常用选择；已正确限制权限的自定义目录也可用。
- 当用户选择受保护部署或排查权限策略误判时，验证目标文件和目录的有效权限，包含写入、删除替换、修改 ACL／所有者及替换父路径组件的能力；遇到 junction／符号链接核对实际目标。只查 `Users` 一条 ACE、只看只读属性，或用当前管理员进程写入成功与否，都不能证明普通权限下是否可替换。ACL 读取失败应报告「无法确认」，不谎报「检测到可写」，也不将此诊断变成通用注册前置闸门。[Windows 访问权限](https://learn.microsoft.com/windows/win32/secauthz/access-rights-and-access-masks)
- 同时检查实际加载的外置 DLL、插件、脚本及更新入口；保护 exe 不能补救可被替换的加载代码。单文件若提取原生库，也应核对实际提取路径和加载权限。不要为了让所有实例启动而把提取目录设成全体用户可写的共享目录。[单文件原生库与提取](https://learn.microsoft.com/dotnet/core/deploying/single-file/overview#native-libraries)
- 配置、日志与用户文件写到产品约定的数据目录，不为方便写数据而放宽程序目录 ACL。更新通过受控提权安装器／更新器完成，验证实际待安装包与目标后写入，升级后复核任务路径和目录权限。
- 迁移保留用户数据，自启切换遵循下节事务要求。不要递归修改用户已有目录权限或接管不属于本应用的任务。

## 注册交互式管理员任务

1. **身份与会话**：记录发起请求用户的 SID，区分登录用户和提权 helper 的账户。通常使用该用户的登录触发器、对应任务主体及交互式令牌（`InteractiveToken`／PowerShell `Interactive`），以便 UI 和托盘出现在其桌面会话。使用其他管理员凭据提升时，不要把 helper 账户误写为原用户；标准用户场景需明确设计账户与会话方案。不要用 SYSTEM 或「不管用户是否登录都运行」解决需要交互界面的托盘自启。
2. **任务动作**：对发布 exe 使用 `Environment.ProcessPath`，验证文件存在，写入绝对路径，并分别设置参数与工作目录；空路径或开发宿主应明确报错。不要用单文件下可能为空的 `Assembly.Location`，也不要指向临时解包 DLL、旧下载位置或 `dotnet.exe` 开发宿主。XML 的 `Command` 写不带引号的路径；回读旧任务时可去除路径两端成对引号，不能把 `"exe" --tray` 当作路径接受。使用 XML 转义及 `ProcessStartInfo.ArgumentList` 处理空格、中文和参数，不经 `cmd /c` 拼接命令。[ExecAction](https://learn.microsoft.com/windows/win32/taskschd/execaction)、[单文件 API 差异](https://learn.microsoft.com/dotnet/core/deploying/single-file/overview#api-incompatibility)
3. **注册权限**：由已提权进程设置最高可用权限并注册／更新。UAC 通常发生在设置阶段；后续由已注册任务按主体权限运行，不应依赖每次登录再弹 UAC。任务账户和本机策略仍可能限制执行。检查任务及任务文件夹的修改权限，避免非授权用户改写动作；为多用户使用的任务采用可区分 SID 的稳定名称。
4. **运行条件**：常驻应用核对 `DisallowStartIfOnBatteries`、`StopIfGoingOnBatteries`、`ExecutionTimeLimit`、触发器延迟和多实例策略，按产品需求配置。任务重复触发时避免同时启动普通和高权限实例；检查单实例检测是否把新进程转发给已有的普通实例。[TaskSettings](https://learn.microsoft.com/windows/win32/taskschd/tasksettings)
5. **结果与回滚**：将任务变更与本应用旧启动项清理纳入同一事务。操作前备份任务定义和普通启动项，完成后回读任务主体、动作、触发器、运行级别、启用状态及普通启动项，再保存设置。切回普通、关闭和卸载同样适用；部分写入失败后恢复并回读旧状态。查询被拒绝或未知不能当作不存在。

区分用户取消（Win32 1223）、产品策略拦截、注册失败、成功和结果未知；访问拒绝保留原始 HRESULT。提示包含阶段、实际路径／任务名、原因与下一步，只有回读证明恢复时才说「原启动方式已保留」。helper 超时不等于取消，不自动重试或宣称回滚。

提权注册 helper 只接受经过验证的本应用操作参数；不要把任意命令行透传成高权限执行入口。

## 采用可复用模板

缺少合适实现时，使用 [ElevatedStartup.cs](templates/ElevatedStartup.cs)，按 [模板接入与隔离测试](startup-template.md) 接入。该页集中说明 helper 分流、事务切换、API 结果、配置参数和隔离 runner。

## 按阶段排查失败

先记录任务完整名称、当前 exe 路径、程序版本、发起用户 SID、注册进程是否提权、失败阶段和原始错误码。读取对应时间段的应用日志；不要仅根据一条「自启设置失败」推断原因。

| 观察结果 | 优先核对与处理 |
| --- | --- |
| 尚未调用任务 API 就提示需要管理员账户 | 检查是否混淆账户资格与进程权限，按 [账户资格与当前权限](#账户资格与当前权限) 核对分割令牌。 |
| 尚未调用任务 API 就提示目录不安全 | 定位路径／ACL 闸门，按 [路径策略](#选择权限与部署方式) 区分产品策略和平台要求。 |
| 注册被拒绝或取消 | 分清 UAC 取消、helper 未提升、任务／文件夹权限、同名任务冲突或本机策略。没有读到任务不一定是不存在，也可能是查询被拒绝。 |
| 任务存在但登录不启动 | 回读触发用户 SID、主体、LogonType、RunLevel、启用状态、电池／空闲条件；检查动作文件是否已移动或随升级更名。 |
| 任务运行但没有窗口／托盘 | 核对会话与账户、启动参数、工作目录、数据目录和崩溃日志；排除 SYSTEM／非交互登录、实例转发及配置目录变化。 |
| 启动成功却不是管理员 | 检查实际进程令牌、主体账户是否具备管理权限，以及是否只剩原有普通实例。勾选最高权限或注册返回成功都不是实际提权证据。 |
| 过一阵退出或只在接电时启动 | 检查执行时限、电池停止设置、应用退出日志与任务历史；不要直接归因于 WPF 或单文件。 |

下面只读查看本应用的已知任务，替换为日志或实现中确认的名称和路径；查询失败应保留具体错误。需要读取受限任务时在相应权限下重查，不执行注册、删除或修改 ACL：

```powershell
$startupTaskName = 'MyApp-Startup'
$startupTaskFolder = '\MyApp\'
$startupTask = Get-ScheduledTask -TaskName $startupTaskName -TaskPath $startupTaskFolder -ErrorAction Stop
$startupTask | Select-Object TaskName, TaskPath, State
$startupTask.Principal | Format-List UserId, LogonType, RunLevel
$startupTask.Actions | Format-List Execute, Arguments, WorkingDirectory
$startupTask.Triggers | Format-List *
$startupTask.Settings | Format-List *
$startupTask | Get-ScheduledTaskInfo | Format-List LastRunTime, LastTaskResult, NextRunTime
Export-ScheduledTask -TaskName $startupTaskName -TaskPath $startupTaskFolder
# 使用从任务动作核对的实际路径；ACL 输出是排查证据，不等于有效访问判定。
Get-Acl -LiteralPath 'C:\Program Files\MyApp\MyApp.exe' | Format-List Owner, Sddl
Get-Acl -LiteralPath 'C:\Program Files\MyApp' | Format-List Owner, Sddl
```

结合 `Microsoft-Windows-TaskScheduler/Operational` 中对应任务和时间的事件判断触发、启动与退出；未启用历史或日志不可读应明确记录。`LastTaskResult` 可能来自上一次运行，`0x00041301` 表示仍在运行，不应当成失败；退出码 0 也不证明 UI 可见或进程已提升。[任务结果码](https://learn.microsoft.com/windows/win32/taskschd/taREDACTED-SECRET)

## 验证结果

| 证据层级 | 检查内容与结论边界 |
| --- | --- |
| 静态检查／隔离测试 | 用任务与注册表替身覆盖注册、修复、普通／管理员切换、卸载、取消、查询／回读／回滚失败，确认设置与系统回读一致。模板的 runner、XML 解析和单文件发布选项见 [隔离验证](startup-template.md#隔离验证)；不改真实登录配置。 |
| 真实注册与恢复 | 在隔离账户／VM 内用带空格和中文路径的框架依赖／自包含单文件测试：可写便携与受保护目录、移动后修复、UAC 同意／取消、失败恢复、同名任务冲突、升级保留数据及卸载仅清理本应用项。明确采用额外 ACL 策略时才验其判定和读取失败。 |
| 真实登录与进程 | 注销后登录，核验触发用户、实际管理员令牌、窗口／托盘可操作且无双重实例；确认旧普通实例未吞掉提权启动。helper 交互验收见 [开发期自查工具](dev-switches.md#人工交互验收确认框explorer-拖放与恢复)。 |

集成检查按本次授权范围进行，不在使用者桌面运行钩子或清理真实自启项；只读评估给出待验步骤。分别报告以上层级，注册回读、XML 解析和单文件隔离运行都不能替代真实登录与提权证据。
