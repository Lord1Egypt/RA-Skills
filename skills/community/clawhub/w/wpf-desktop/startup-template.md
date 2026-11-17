# 管理员自启模板：接入与隔离测试

仅在采用或修改 [ElevatedStartup.cs](templates/ElevatedStartup.cs) 时读取。权限选择、部署策略、任务注册与验收要求统一见 [自启部署与排查](startup.md)；已有合适实现时优先适配。

## 模板能力与边界

模板无第三方依赖，适用于 .NET 10 Windows apphost，支持框架依赖／自包含单文件。通过 Task Scheduler COM 注册 XML，无需外置脚本、临时 XML 或命令字符串。任务名包含应用 ID 和用户 SID，元数据标记归属；同名但归属不符的任务拒绝覆盖或删除。归属标记防止误操作，不能替代访问控制。

模板只支持请求者本人的管理员账户同账户 UAC；helper 在写入前拒绝其他账户。账户资格的前置判断见 [账户资格与当前权限](startup.md#账户资格与当前权限)。

任务和 Run 值在同一 helper 内完成事务：读取旧值 → 注册／删除任务 → 回读 → 更新本应用 Run 值；失败时尽力恢复并回读，回滚不完整单独报告。操作锁按应用／用户隔离、跨进程和会话，并仅允许当前用户访问（.NET 10 `NamedWaitHandleOptions`）。

修复将任务指向当前 `Environment.ProcessPath`，配置当前用户登录触发、`InteractiveToken`、`HighestAvailable`、独立工作目录、允许电池运行、无执行时限和忽略重复实例。它不会启动任务、安装钩子、退出旧驻留实例或迁移配置。旧版无归属标记／不同名称的任务，需要调用方验证旧动作和账户后按迁移规则备份处理，不能只凭名称认领。

## 接入步骤

1. 复制模板、调整命名空间，在受信应用代码中固定配置，例如 `StartupOptions Options = new("Example.App", "Example.exe", "--tray")`；不要将应用 ID、exe 名或启动参数开放为 helper 命令行输入。`AppId` 同时是 HKCU Run 值名；已有其他值名或固定任务名时适配后端与迁移流程。
2. 在 WPF `Application` 构造、单实例检查及配置／钩子初始化之前分流 helper。配置 `<StartupObject>你的命名空间.Program</StartupObject>`；已有入口时在原入口接入：

   ```csharp
   [STAThread]
   public static int Main(string[] args)
   {
       // 此前沿用测试/无系统集成开关，禁止系统操作时拒绝 helper 请求。
       if (ElevatedStartup.TryHandleHelper(args, Options, LogStartupError, out int code))
           return code;
       var app = new App();
       app.InitializeComponent();
       return app.Run();
   }
   ```

   日志函数不依赖设置写入。仅放在 `OnStartup` 不能保证早于 App 构造中的副作用。显式传播 `Application.Run()` 返回值，不能只调用 `Shutdown(code)` 后丢弃入口退出码。

3. 设置页共用 `await ElevatedStartup.ChangeAsync(operation, Options)`，按下表选择操作。不要默认开启管理员自启、在启动时自动提权或在超时后重放。

   | 用户操作 | `StartupOperation` |
   | --- | --- |
   | 开启管理员自启 | `Install` |
   | 移动／升级后修复 | `Repair` |
   | 切回普通自启 | `Plain`，在同一事务内移除任务并写 Run |
   | 关闭自启或卸载 | `Uninstall` |

4. 将结果映射到本地化 UI，并在保存前按本次期望配置回读系统状态。`Detail` 用于诊断日志；用户提示包含阶段、可理解原因和日志位置，不原样展示长堆栈。

   | `StartupOutcome` | UI 与保存行为 |
   | --- | --- |
   | `Applied`／`Unchanged` | 可保存成功状态 |
   | `Cancelled` | 回读并恢复显示，不当作错误 |
   | `Failed` | 显示失败阶段；按实际回读呈现旧状态或回滚失败 |
   | `Uncertain` | helper 可能仍运行或回读失败；保留未知状态，禁用重试直至 helper 结束且显式回读成功，不宣称已回滚 |

## 配置与调用方职责

| 配置／行为 | 接入要求 |
| --- | --- |
| `LogonDelaySeconds` | 默认 3，范围 0–300 秒，0 可省略 XML Delay；这是模板边界，不是 Windows 上限。生成和回读使用本次期望值，不能用尚未保存的旧设置验证新任务。helper 只额外接受范围校验过的整数；Plain 的 Run 不应用延迟。 |
| 任务优先级 | 显式 `Priority=4`（Normal），不使用默认 7。短延迟不能替代托盘创建重试及 Explorer 重启恢复。[微软优先级说明](https://learn.microsoft.com/windows/win32/taskschd/tasksettings-priority)、[PowerToys 实现](https://github.com/microsoft/PowerToys/blob/main/src/runner/auto_start_helper.cpp)。 |
| `LegacyRunValueName`／`PlainArguments` | 前者指定旧 Run 名，注册、移除、切换及回滚均处理新旧名称；后者单独指定普通启动参数。 |
| 任务 DACL | 模板允许当前用户只读，是模板策略。允许本用户管理任务的产品需明确维护相应 DACL，不能授予任意用户写权限；它与便携目录 ACL 是两件事。 |
| `IsHelperPending` | 跟踪等待超时后仍存活的 helper，并拒绝新 `ChangeAsync`。进程内跟踪不覆盖应用重启恢复；60 秒等待从 helper 启动后计时，不包含 ShellExecute 等待 UAC 同意的时间。 |
| Run 命令行长度 | 超过 260 字符时在写入前拒绝并保留原状态。可选较短路径，或另行设计普通权限登录任务后端；写注册表成功不保证登录执行。[微软 Run 文档](https://learn.microsoft.com/windows/win32/setupapi/run-and-runonce-registry-keys)。 |

## 隔离验证

[ElevatedStartup.Tests](templates/ElevatedStartup.Tests/Program.cs) 是无测试框架包的可执行回归 runner，失败返回非零退出码。将 [test-startup.ps1.txt](templates/test-startup.ps1.txt) 复制为 `tools/Test-ElevatedStartup.ps1` 后运行：

```powershell
pwsh -NoProfile -File tools/Test-ElevatedStartup.ps1 -TemplateDirectory <skill>/templates
```

脚本复制模板、测试源和 `.csproj.txt` 到独立临时目录，使用真实编译器及内存任务／注册表替身，完成后清理。默认不启动 helper、不访问真实任务或 Run 值；只创建随机名称的短期互斥锁来验证串行化。

修改模板时同步维护行为断言，优先复用应用已有 runner。覆盖以下场景，不仅检查源码关键词：

- 注册与普通自启互斥、移位修复、禁用／过期任务恢复、卸载幂等、归属冲突、新旧 Run 名与 Plain 切换回滚。
- 中文／空格／XML 字符和旧路径引号、用户隔离、交互权限、电池／时限设置、Normal 优先级、0／3／自定义／300 秒延迟、非法秒数及超长 Run 命令。
- UAC 取消、账户不匹配、查询失败、部分写入、回读／回滚失败、并发冲突及 helper 超时不重放。

可追加以下选项：

| 选项 | 额外验证 |
| --- | --- |
| `-ValidateXml` | Windows Task Scheduler 的**未注册** TaskDefinition 解析 XML；不注册、删除任务或访问 Run。 |
| `-PublishSingleFile` | 在本机架构发布框架依赖及自包含单文件，执行同一隔离回归；路径用例使用真实 `Environment.ProcessPath`。需要可还原对应运行时包。 |

这些测试不证明真实注册、任务 DACL 生效、UAC 交互、登录触发或管理员进程已通过。实际集成验收及证据分级见 [验证结果](startup.md#验证结果)；应用本身仍需 WPF 发布与窗口测试。
