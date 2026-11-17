# 开发期自查工具：常驻开关与临时探针

这里集中维护 smoke、布局与交互验收、临时探针和测试结果判定；具体故障改法见 [pitfalls.md](pitfalls.md)。

已有的自查开关挂在 `OnStartup` 里、**且放在单实例互斥体检查之前**，这样托盘里正在用的实例照常工作，检查进程自己开自己关，互不干扰。探针则是临时的：量完就删，不进主干。

```csharp
protected override void OnStartup(StartupEventArgs e)
{
    // …读配置、上主题…
    if (e.Args.Contains("--smoke") || e.Args.Contains("--shots"))
    {
        ShutdownMode = ShutdownMode.OnExplicitShutdown; // 关闭第一扇测试窗口后仍能布局下一扇
        // 等消息循环可处理布局后再执行，避免验证未初始化的窗口。
        Dispatcher.BeginInvoke(() =>
        {
            if (e.Args.Contains("--shots")) RunShots(e.Args); else RunSmoke();
        }, DispatcherPriority.ApplicationIdle);
        return;
    }

    _mutex = new Mutex(true, @"Local\Xxx.App", out bool isFirst);   // ← 之后才是单实例；Local\ 每会话一实例，要整机唯一才用 Global\
    // …
}
```

## `--smoke`：CI 里防 XAML 错误带到发版

构造并布局每一个窗口，然后退出。WPF 的 XAML 是懒加载的，某个窗口写错了，只要不打开它就不会报错。

```csharp
private void RunSmoke()
{
    InSmoke = true;                       // App 上的 static bool；窗口定位/居中逻辑判它跳过，别乱动
    string report = Path.Combine(Path.GetTempPath(), "xxx-smoke.txt");
    try
    {
        foreach (var make in new Func<Window>[] { () => new MainWindow(), () => new SettingsWindow(), /*…*/ })
        {
            var w = make();
            w.WindowStartupLocation = WindowStartupLocation.Manual;
            w.Left = -32000; w.Top = -32000; w.ShowActivated = false;
            w.Show();
            Dispatcher.Invoke(() => { }, DispatcherPriority.Loaded);   // 泵到 Loaded：Show 排队的收尾活当场做完
            w.UpdateLayout();
            // 不只「没抛」：必须断言真的布局出了尺寸。Window.Show() 在应用已开始关闭时会静默空转
            // （不抛、hwnd=0、ActualWidth=0），只判异常的 smoke 在那种状态下照样绿灯——
            // 初始化事件也可能触发 Shutdown，需同时核对实际尺寸。
            if (w.ActualWidth <= 0 || w.ActualHeight <= 0)
                throw new InvalidOperationException($"{w.GetType().Name}: laid out to zero size");
            w.Close();
        }
        File.WriteAllText(report, "OK");
        Shutdown(0);
    }
    catch (Exception ex) { File.WriteAllText(report, ex.ToString()); Shutdown(1); }
}
```

CI 里判成功以**它写的 marker**为准，退出码只做辅助：PowerShell 经 `Start-Process -PassThru` 读 GUI 进程的 `ExitCode` 有已知的读空坑（拿到 `$null`），而且 marker 顺带证明了应用真跑到了「所有窗口都布局完、走到写文件」那一步——这正是这个开关要验的事。所以成败看 marker，退出码只在**明确非零**时才判失败。

**完整的 CI 步骤（含定位 exe、失败时打印异常）见 [CI 模板](templates/ci.yml) 的 `Smoke (parse every window's XAML)` 步骤**，直接照抄进 test job 即可，别自己拼。

## `--shots <目录>`：多语言 / 多分辨率 / 双主题批量截图

用 `RenderTargetBitmap` 离屏渲染每个窗口成 PNG，不抢焦点、不打扰运行中的实例。`OnStartup` 里调的 `RunShots(args)` 不是框架的东西，就是把下面这些 `Shot()` 调用按你的窗口清单包一层。

关键是**模拟工作区高度**，因为窗口高度上限是按显示器工作区算的：

```csharp
// 工作区高度（DIP）= 屏幕物理高 / 缩放 - 任务栏高度
// 任务栏随 DPI 缩放，所以它在 DIP 里是个常数：Win10 约 40，Win11 约 48（自动隐藏则为 0）。
// 以下是测试样例；矩阵按产品支持的屏幕、缩放与任务栏设置调整。
const double taskbar = 48;
var waHeights = new[] {
    768 / 1.50 - taskbar,    // 1366x768 @150% ≈ 464——最紧的一档，XAML 兜底 MaxHeight 按这一档减边距算
    768 / 1.25 - taskbar,    // 1366x768 @125% ≈ 566
    1080 / 1.50 - taskbar,   // 1920x1080 @150% ≈ 672
    1080 / 1.00 - taskbar,   // 1920x1080 @100% ≈ 1032
};

void Shot(string name, Func<Window> make, Action<Window>? tweak = null)
{
    foreach (var wa in waHeights)
    {
        ThemeService.Apply(activeTheme);          // 每个窗口都重设：有的窗口初始化时会改全局主题
        var w = make();
        w.WindowStartupLocation = WindowStartupLocation.Manual;
        w.Left = -32000; w.Top = -32000; w.ShowActivated = false;
        w.Show();
        w.MaxHeight = wa;                          // 必须 Show 之后设，否则被真实显示器的值覆盖
        tweak?.Invoke(w);
        // 改 MaxHeight（以及 tweak 里的任何改动）只是让布局失效，ActualWidth/ActualHeight
        // 要等下一次布局过程才更新。少了这两句，截图就是按「封顶之前」的尺寸拍的——正好是
        // 这个 harness 要模拟的那个维度，等于白跑。RunSmoke 里同样有这两句。
        w.Dispatcher.Invoke(() => { }, DispatcherPriority.Loaded);
        w.UpdateLayout();
        var rtb = new RenderTargetBitmap((int)Math.Ceiling(w.ActualWidth), (int)Math.Ceiling(w.ActualHeight),
                                         96, 96, PixelFormats.Pbgra32);
        rtb.Render(w);
        // …PngBitmapEncoder 存成 $"{name}@{wa:0}.png"…
        w.Close();
    }
}
```

示例按工作区高度渲染指定窗口；主题和语言由调用方设置。

### 截图的盲区

布局与 DPI 验收使用产品支持的最小工作区、混合缩放副屏、长译文与 RTL、深浅主题，并构造受影响的条件性字段状态；切换显示器或窗口形态后复验。

- harness 设置 `w.MaxHeight` 会掩盖应用缺少运行时封顶的问题。另走正常开窗路径，覆盖显示器探测成功与失败。
- `RenderTargetBitmap` / `PrintWindow` 能画出屏外内容；PNG 完整不证明可点击。将主按钮的屏幕 rect 与所在显示器的 `rcWork` 比较，确认标题栏和操作区可达。
- 源码扫描只是线索，需结合绑定、祖先约束与实际布局，不能只匹配辅助函数名或按截图数量判断覆盖。

布局修法见 [小屏对话框](pitfalls.md#对话框在小屏上确定按钮跑到任务栏底下)和[长译文控件](pitfalls.md#德语界面上控件被挤没)。

### harness 初始化与副作用

- 样例配置先完成正常启动需要的归一化，例如将跟随系统语言解析成具体 locale。构造/Loaded 中的 `SelectionChanged`、`Checked` 等事件不能把初始化误当成用户操作，触发写盘、重启或弹窗。
- 意外关闭的诊断见 [应用突然消失](pitfalls.md#应用突然消失没留下任何日志)；窗口布局结果统一按 smoke 断言。
- `OverrideMetadata` 同一类型与属性只能调用一次；逐语言截图改设每个窗口的 `FlowDirection`，不要在循环里重复覆写元数据。[DependencyProperty.OverrideMetadata](https://learn.microsoft.com/dotnet/api/system.windows.dependencyproperty.overridemetadata)
- 全屏覆盖窗、热键与输入钩子会影响真实桌面。harness 默认跳过不相关的系统集成；必须验证时使用隔离模式，并沿用相应窗口创建前的初始化。ghost window 边界见 `pitfalls.md` 对应小节。

## 分段计时探针：定位启动耗时

在需要区分耗时的启动阶段之间临时打点：

```csharp
private static readonly Stopwatch _sw = Stopwatch.StartNew();
private static readonly List<string> _log = new();
private static void Mark(string what) => _log.Add($"{_sw.ElapsedMilliseconds,5}ms  {what}");
// OnStartup 末尾：Dispatcher.BeginInvoke(new Action(Dump), DispatcherPriority.ApplicationIdle);
```

在每个阶段之间打点，退出时写文件。左边一列是**累计**值，所以每一阶段自身的耗时要用相邻两行相减——这一步别省，耗时大头往往就藏在两个看起来平平无奇的打点之间。

按耗时分布决定优化对象。首次库初始化的后台化及就绪/异常契约见 `pitfalls.md`「冷启动慢，耗时却不在磁盘」。

## 像素采样探针：验证视觉问题

「白闪」「闪一下」这类问题，需要把主观描述变成可数的帧。开窗期间起个后台线程，每 5ms 用 `GetPixel` 从屏幕固定坐标取色：

```csharp
IntPtr dc = GetDC(IntPtr.Zero);
uint c = GetPixel(dc, x, y);      // 0x00BBGGRR
ReleaseDC(IntPtr.Zero, dc);
```

对照 `SHOW` 和 `ContentRendered` 时间戳，定位白帧发生的阶段。优先在应用进程内布置探针；外部屏幕采样需确认目标窗口确实可见，避免采到遮挡窗口。查询 GDI 对象时检查 `GetObject` 的返回值，跨进程查询失败不能把未写入的结构体当成有效结果。

## 从外部驱动 UI 做验证

UIA 未列出可见模态窗口时，改用 `EnumWindows` 按进程 ID、可见性和标题定位：

```csharp
EnumWindows((h, _) => {
    GetWindowThreadProcessId(h, out uint pid);
    if (pid == target && IsWindowVisible(h)) { /* GetWindowText 判标题 */ }
    return true;
}, IntPtr.Zero);
```

配套两条：窗口没显示时 `Process.MainWindowHandle` 是 0（托盘应用常态如此），所以别拿它当入口；窗口矩形用 `DwmGetWindowAttribute(DWMWA_EXTENDED_FRAME_BOUNDS)` 而不是 `GetWindowRect`，后者在 DWM 下会多出一圈不可见的边框阴影。

窗口找到后，可用 UIA 的 `InvokePattern`／`SelectionItemPattern`／`ExpandCollapsePattern` 操作控件。按名字查询同时过滤 `ControlType`，避免将标签 TextBlock 当成 ComboBox；`AutomationId` 不会为没有默认 automation peer 的 Border 等元素创建 peer。

## 人工交互验收：确认框、Explorer 拖放与恢复

自动化工具无法操作高权限窗口或拒绝跨窗口释放鼠标时，保留真实交互这一验收项。准备独立数据目录、测试文件和目标 Explorer 窗口，关闭应用已有的 Shell 集成／自启动开关，确认夹具没有被单实例转发到用户正在使用的实例。给用户可辨认的窗口标题、路径特征、操作按钮和预期结果；交接后暂停输入，避免抢走焦点。

先保存源文件与目标文件的内容摘要、必要的修改时间以及相关数据库业务行。用户回复完成后，再检查这些证据：

- **应用确认框取消**：窗口关闭，日志记录取消及正常退出；目标内容与修改时间、相关业务行保持基线，没有执行成功记录。原始数据库文件摘要可能受 WAL 或连接收尾影响，应核对业务数据。
- **Explorer 拖放**：至少包含两个同名文件和一个含子目录的文件夹，检查目标文件集合、两个同名内容均保留、目录层级及摘要；同时核对源文件未被移动。若产品承诺成功后移除暂存并隐藏空架，再检查数据库清理、成功历史和窗口行为。物化服务测试通过不能代替跨进程 OLE 拖放。
- **空架隐藏**：结合可见窗口、进程存活与实际数据验证隐藏，不能把进程退出误当成隐藏。辅助功能树可能滞后，证据冲突时核对实时画面和磁盘结果。

分别记录实际管理员令牌、应用自身的批准／取消、Windows 系统 UAC 提示是否出现。系统策略可能使 RunAs 直接提升；此时只能验证实际提升及应用确认流程，不能声称系统同意／拒绝提示通过，也不要为补验随意更改全机安全策略。固定夹具自动批准 Core API 的专项测试，同样不能代替应用确认框的真实交互。

若应用本来就支持文件与数据库之间的中断恢复，用可停在提交边界的隔离 worker 覆盖提交前、提交后未记账、完成记账，以及相应撤销边界。终止真实进程后重启，重复恢复和撤销，检查最终文件内容、历史及未决标记。不要用正常抛异常或取消令牌代替进程强杀；强杀通过也不证明断电和硬件缓存丢失场景通过。只终止本次夹具进程，并保留不确定状态的证据。

## 间歇性问题：跑 N 轮记比分

间歇性问题用重复试验记录成功率与环境。A/B 尽量交错或相邻运行，减少桌面状态与缓存变化的干扰；次数按复现概率和验证成本选择。对照组也无法复现时，不据此宣布修复有效。

## 跑测试会真的接管你这台机器的鼠标

真实安装 `WH_MOUSE_LL` / `WH_KEYBOARD_LL` 的测试可能接收或抑制桌面输入；无头 CI 中未能安装钩子不能证明交互安全。

只验证泵线程、安装与拆卸的测试使用观察模式，关闭不相关的吞键、延迟闸门与输入注入。回调保持轻量，避免被 `LowLevelHooksTimeout` 静默移除。需要测试抑制或注入行为时，用明确的交互验收环境，并保证失败/超时后卸载。

验证实际行为与清理结果，不用“源码中出现某个构造参数”替代功能验证。

## 测试运行与结果判定

沿用项目测试框架和 runner，版本迁移按[依赖升级](upgrade-dependencies.md)适配。命令退出 0 不足以证明实际运行了测试：

| 模式 | 命令与配置 |
| --- | --- |
| .NET 10 MTP | 按[项目配置](project-setup.md#sdk-固定globaljson-一处说了算)选择 MTP，再运行 `dotnet test --project tests/Xxx.Core.Tests -c Release --minimum-expected-tests 1`；下限改为该项目实际预期数量。 |
| VSTest | 保留项目原调用，输出 TRX 并检查实际测试数；多目标项目各用独立结果路径并汇总全部目标。 |

VSTest 示例：

```powershell
dotnet test tests/Xxx.Core.Tests -c Release --logger "trx;LogFileName=results.trx"
if ($LASTEXITCODE) { exit $LASTEXITCODE }
[xml]$result = Get-Content tests/Xxx.Core.Tests/TestResults/results.trx
if ([int]$result.TestRun.ResultSummary.Counters.total -lt 1) { throw 'No tests discovered' }
```

检查运行是否完整结束及错误／跳过原因；宿主初始化失败可能使部分测试未执行，即使失败数为零也不能判绿。需要前台的真实发键测试抢不到前台时记为跳过；窗口构造或离屏截图不替代接收端验证。

## WPF 回归测试：STA、Application 与入口程序集资源

需要实例化窗口的测试不能只在任意测试线程上 `new Window()`。在 STA 线程上建立宿主，并保持 Dispatcher 消息循环存活；通过它调度构造、交互和关闭。多个测试类共享同一个 `Application` fixture，同一 AppDomain 内不要为每个测试类重建 Application。临时线程退出后仍留下的 `Application.Current` 会指向已失效的 Dispatcher。

若 XAML 在测试里报图标或字典资源找不到，而应用内正常，先检查相对 pack URI 的解析程序集。测试入口程序集与应用程序集不同；可使用明确的 `/Assembly;component/...` 引用，或在测试项目以相同资源路径链接已有资源。不要生成另一份图标掩盖路径问题，也不要为了加载资源启动完整生产 App 的自启、钩子与配置流程。

测试编辑器要走真实保存路径，再把结果写到隔离文件并重读。复制、嵌套排序等变更同时验证结构关系和执行轨迹，单纯断言列表长度看不出父引用错位。共享模型被另一个入口修改时，还要检查已经构造的行 ViewModel 是否更新。

## 多语言资源：检查承诺完整翻译的语种

从应用支持的语言列表取样本，逐一打开预期的 `.resx`。这样删掉整份翻译文件也会让测试失败。对承诺完整翻译的语言，用键集合的对称差同时检查缺键和多键。允许父级文化回退的地区变体按回退链验证。

```csharp
// resourceDir、supportedCultures 由项目提供；此处传入承诺独立完整翻译的 culture 名。
static HashSet<string> ReadKeys(string path) =>
    XDocument.Load(path).Root!.Elements("data")
        .Select(entry => (string)entry.Attribute("name")!)
        .ToHashSet(StringComparer.Ordinal);

var neutral = ReadKeys(Path.Combine(resourceDir, "Strings.resx"));
foreach (var culture in supportedCultures)
{
    var keys = ReadKeys(Path.Combine(resourceDir, $"Strings.{culture}.resx"));
    keys.SymmetricExceptWith(neutral);
    Assert.True(keys.Count == 0, $"{culture}: {string.Join(", ", keys)}");
}
```

项目有已废弃术语表时，用它检查翻译值；用户可见错误与内部诊断分别约定用语。
