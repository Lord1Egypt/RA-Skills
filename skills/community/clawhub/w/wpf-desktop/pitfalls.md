# WPF 踩过的坑（按症状查）

按症状查找根因、改法与验证方法。示例参数按目标应用调整；性能结论用 [自查工具](dev-switches.md) 在相同条件下复测。

## 窗口出现前白闪一下

先区分背景擦除和首帧合成：若白帧发生在 `WM_ERASEBKGND` 之前，修改背景刷无法解决。用像素采样和 `ContentRendered` 时间戳确认阶段。

检查窗口类的实际背景刷；如果已经是 `NULL_BRUSH`，不要继续用替换背景刷处理合成白帧。

若确认是首帧合成白闪，可试在首帧就绪前 cloak，并同时验证激活、隐藏与再次显示：

```csharp
[DllImport("dwmapi.dll")]
static extern int DwmSetWindowAttribute(IntPtr hwnd, int attr, ref int value, int size);
const int DWMWA_CLOAK = 13, DWMWA_CLOAKED = 14;   // 值见官方 DWMWINDOWATTRIBUTE 枚举

// 每个要防白闪的窗口调一次；hwnd 要等 SourceInitialized 之后才非零
static void EnableAntiFlash(Window w)
{
    void Cloak(int on)
    {
        var hwnd = new WindowInteropHelper(w).Handle;
        if (hwnd != IntPtr.Zero) DwmSetWindowAttribute(hwnd, DWMWA_CLOAK, ref on, sizeof(int));
    }
    w.SourceInitialized += (_, _) => Cloak(1);
    w.ContentRendered   += (_, _) => Cloak(0);
}
```

感知延迟不变，那段时间原本也看不到内容。`AllowsTransparency="True"` 的分层窗口没有这个问题，系统在 WPF 合成之前根本不画它，所以无边框悬浮面板不用管，带原生边框的普通窗口才要处理。

## 改完第一次不闪了，托盘里第二次打开照旧闪

上面那段代码有个前提：**它只对「每次用完就关、下次新建」的窗口成立**。设置窗口、管理器窗口都是这样，每开一次走一遍 `SourceInitialized`。

托盘应用的主窗口通常不是这样，关闭只是 `Hide()`，对象一直活着，`SourceInitialized` 一辈子只触发一次。于是只有开机后第一次显示不闪，之后每次从托盘打开白闪原样回来。

补法是在窗口隐藏之后重新 cloak，为下一次显示备好。**这段接在上面 `EnableAntiFlash` 的函数体里**——`Cloak` 和 `w` 都是那个函数的局部，单独贴到别处编译不过：

```csharp
w.IsVisibleChanged += (_, e) =>
{
    if (e.NewValue is false) { Cloak(1); return; }   // 隐藏态不参与合成，此时 cloak 不可见
    // 兜底：正常由 ContentRendered 摘掉；万一某次没触发，
    // 卡在 cloak 里的窗口就是「点了托盘没反应」的隐形应用
    w.Dispatcher.BeginInvoke(() => Cloak(0), DispatcherPriority.ContextIdle);
};
```

那个兜底不是洁癖。cloak 的失败方向很不对称：没设上只是白闪照旧，回到修之前；设上没摘掉，应用就彻底隐形，用户只会以为程序坏了。`ContextIdle` 排在 `Render` 和 `Loaded` 之后，正常路径跑到它时 `ContentRendered` 早已摘干净，这一次就是空操作。

验证要连着三态一起看，只测第一次会漏掉这个坑：首次显示 `cloaked=0` → 隐到托盘 `cloaked=1` → 再次显示 `cloaked=0`。读法用 `DWMWA_CLOAKED`（14），注意它的签名是 `out` 不是 `ref`：

```csharp
[DllImport("dwmapi.dll")]
static extern int DwmGetWindowAttribute(IntPtr hwnd, int attr, out int value, int size);
DwmGetWindowAttribute(hwnd, DWMWA_CLOAKED, out int cloaked, sizeof(int));
```

## 第一次打开窗口要等一下，之后就很快

分别测量首次布局和复用窗口的打开耗时。若控件模板、主题字典或可视树构造占主要成本，可在应用空闲时预布局；先确认它不会写配置、抢焦点或触发业务操作。

```csharp
// 启动时窗口不显示的那条分支上排一个，ApplicationIdle 保证不和开机任务抢资源
if (!_main.IsVisible)
    Dispatcher.BeginInvoke(WarmMainWindow, DispatcherPriority.ApplicationIdle);

void WarmMainWindow()
{
    // Window.Width/Height 的默认值是 NaN（没在 XAML 里写死尺寸、或用 SizeToContent 的窗口
    // 就是这样），而 UIElement.Measure 明确拒绝 NaN 并抛 InvalidOperationException。
    // 这段跑在每次启动的路径上，直接照抄进一个自适应尺寸的窗口就是启动即崩。
    var w = double.IsNaN(_main.Width) ? _main.RestoreBounds.Width : _main.Width;
    var h = double.IsNaN(_main.Height) ? _main.RestoreBounds.Height : _main.Height;
    if (double.IsNaN(w) || w <= 0) w = _main.MinWidth > 0 ? _main.MinWidth : 800;
    if (double.IsNaN(h) || h <= 0) h = _main.MinHeight > 0 ? _main.MinHeight : 600;
    var size = new Size(w, h);
    _main.Measure(size);
    _main.Arrange(new Rect(new Point(), size));
    _main.UpdateLayout();
}
```

预布局不能保证消除首次 HWND/DWM 呈现成本。用实际开窗路径复测收益，避免为未测出的差异增加离屏渲染步骤。

## 双击 exe 之后忙碌光标长时间旋转

单实例用具名 `Mutex` 判断，`_mutex` 必须是字段，写成局部变量的话方法一返回它就成了垃圾，GC 收走时锁跟着释放，第二个实例照样能启动，而且这种 bug 只在 Release 下偶发。名字前缀决定作用域：`Local\` 或不带前缀是每个登录会话各一个实例，`Global\` 是整机一个。托盘小工具通常要前者（快速切换用户时第二个会话还能开自己的），要跨会话碰全局资源的应用才需要 `Global\`。

检查第二个实例是否在等待仍存活的主实例释放互斥体。普通重复启动只需通知已有窗口，可采用较短等待；应用重启接管则需给旧实例退出留出时间。示例超时按目标机器复测。

还有一条顺序问题：叫醒老实例的信号要发在等互斥体**之前**，反过来写常态路径就是先空等满超时才去叫窗口。

但超时不能一刀切。还有两类进程会撞上同一段代码：切换界面语言后重开自己、以管理员身份重开自己。这两条恰恰相反，接管一个正在退出的实例是它们唯一的目的，而且失败后果不对称：双击失败只是再点一次，这两条路上老实例已经在退了，新实例再一退就一个都不剩，用户切完语言发现应用没了。

按「本进程是被谁启动的」分档。重启路径本来就会带一个 `--show` 之类的参数（用来忽略「启动时最小化」强制显示窗口），正好当判据：

```csharp
var takeover = e.Args.Contains("--show")
    ? TimeSpan.FromSeconds(3)          // 被重启路径派出来顶替，接管是唯一目的，给足余量
    : TimeSpan.FromMilliseconds(250);  // 用户双击，老实例还在，等待必然走满，越短越好
```

`dev-switches.md` 里那句 `_mutex = new Mutex(true, …, out bool isFirst)` 后面用 `// …` 省掉的 `!isFirst` 分支，就是 `takeover` 的去处：`_mutex.WaitOne(takeover)`，按上面那条顺序先叫醒老实例再等。等到了说明老实例已经放手，本进程接着当唯一实例；等不到就自己退出。

## 冷启动慢，耗时却不在磁盘

先按 [分段计时](dev-switches.md#分段计时探针定位启动耗时) 区分配置读取、第三方库首次初始化、索引构建、窗口构造和呈现。词典等库可能在第一次函数调用时加载大量内置数据，不能仅凭函数名将它算成磁盘或业务计算开销。

若测量支持后台初始化，保留三个契约：

- UI 与低级键鼠钩子回调不阻塞等待。低级钩子超时可能被系统静默移除，重活移到工作线程。[Windows 低级键盘钩子](https://learn.microsoft.com/windows/win32/winmsg/lowlevelkeyboardproc)
- 未完成的索引不返回“未找到”。使用异步就绪状态，或由可等待的后台调用方等待完整结果；UI 可显示加载态并在完成后重查。
- 后台异常传回既有错误提示与恢复流程，不能只吞异常并返回空库。

优化后重测用户实际感知的入口，例如热键呼出、重复启动和首次开窗。是否继续优化由收益决定，不把某台机器的耗时当成框架下限。

## 点了「设置」，窗口偶尔没到最前面

用 `GetForegroundWindow()` 和重复 A/B 试验区分托盘菜单关闭时的前台移交、系统拒绝激活与应用回归。先验证 `Show` / `Activate` / `Focus` 的实际路径；重试应有上限，并在用户切换应用或窗口关闭后停止。

若已有实现用短暂切换 topmost 提高 z 序，保留以下边界。它只能改变层叠位置，不能证明获得键盘焦点，也不应在缺少复现时默认添加：

```csharp
// 只在「彻底抢输」这条分支跑，正常抢到前台时完全不执行
static void RaiseAboveBlocker(Window w, IntPtr hwnd, IntPtr blocker)
{
    if (hwnd == IntPtr.Zero || w.Topmost) return;          // ① 置顶窗口一律跳过
    var fg = GetForegroundWindow();
    if (fg == hwnd || fg != blocker) return;               // ② 只压过一开始那个对手
    const uint f = SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE;
    SetWindowPos(hwnd, HWND_TOPMOST,   0, 0, 0, 0, f);
    SetWindowPos(hwnd, HWND_NOTOPMOST, 0, 0, 0, 0, f);
}
// ③ 调用点：gaveUp 要单独判，不能跟着整个退出分支走
if (gaveUp && stable == 0) RaiseAboveBlocker(w, live, blocker);
```

示例中的 `blocker` 是开始激活时的前台窗口，`stable` 是连续确认次数，`gaveUp` 表示真正超时。不要改变本来置顶的窗口，不盖住用户后来切入的第三个应用，也不把窗口关闭等退出原因当成超时。按 [间歇性问题验证](dev-switches.md#间歇性问题跑-n-轮记比分) 复测；无法稳定复现时保留不确定性。

## 副屏上窗口位置算错

`app.manifest` 里必须声明 PerMonitorV2：

`dotnet new wpf` **不会生成这个文件**，要自己建 `app.manifest` 并在 csproj 里用 `<ApplicationManifest>` 指过去（见 `project-setup.md` 的 csproj 片段）。层级贴错一层不报错、清单被静默忽略，正好就是这一节要防的 bug，所以给完整文件：

```xml
<?xml version="1.0" encoding="utf-8"?>
<assembly manifestVersion="1.0" xmlns="urn:schemas-microsoft-com:asm.v1">
  <assemblyIdentity type="win32" name="Xxx.App" version="1.0.0.0" processorArchitecture="*"/>
  <compatibility xmlns="urn:schemas-microsoft-com:compatibility.v1">
    <application>
      <supportedOS Id="{8e0f7a12-bfb3-4fe8-b9a5-48fd50a15a9a}"/>
    </application>
  </compatibility>
  <application xmlns="urn:schemas-microsoft-com:asm.v3">
    <windowsSettings>
      <dpiAware xmlns="http://schemas.microsoft.com/SMI/2005/WindowsSettings">true/pm</dpiAware>
      <dpiAwareness xmlns="http://schemas.microsoft.com/SMI/2016/WindowsSettings">permonitorv2,permonitor</dpiAwareness>
    </windowsSettings>
  </application>
</assembly>
```

清单需符合 schema：先放 `assemblyIdentity`，声明目标 Windows 的 compatibility，再设置 `windowsSettings`。不要把物理像素直接当成 DIP；按窗口所在屏幕的 DPI 换算，移动到不同缩放的屏幕后复验。

两个配套的坑。一是同时开了 `UseWindowsForms` 的混合工程（用 WinForms 托盘图标或剪贴板时会这样），WinForms 的分析器会对清单里这两行报 `WFO0003` 让你改用 `ApplicationHighDpiMode`。那条建议只对真正的 WinForms 应用成立，它作用于 WinForms 生成的 `Main` 里那句 `Application.SetHighDpiMode`，而 WPF 应用的 `Main` 不经过那里。清单才是 WPF 的正规途径，直接 `<NoWarn>$(NoWarn);WFO0003</NoWarn>` 并在旁边写清理由。

二是验证别用 `GetAwarenessFromDpiAwarenessContext`，`DPI_AWARENESS` 这个枚举压根没有 V2 这一档，最大值就是 2（per-monitor），V2 上下文查出来也是 2，看着像没配成功。要用 `AreDpiAwarenessContextsEqual` 拿进程的上下文去和 `DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2`（值 -4）比。

## 对话框在小屏上，确定按钮跑到任务栏底下

用 `SizeToContent="Height"` 的编辑器窗口高度完全由内容决定，必须封顶，否则内容一多就长到屏幕外——首当其冲的是「确定 / 取消」那一行。

按目标显示器的工作区和缩放计算上限，避免固定高度在小屏溢出、在大屏过早滚动。

改成运行时按窗口所在那块屏的工作区算：

```csharp
w.SourceInitialized += (_, _) => {
    var hwnd = new WindowInteropHelper(w).Handle;               // 到这一步才非零
    var mi = new MONITORINFO { cbSize = Marshal.SizeOf<MONITORINFO>() };
    // 拿不到显示器信息就什么都不做——退回 XAML 里那个保守的 MaxHeight
    if (!GetMonitorInfo(MonitorFromWindow(hwnd, MONITOR_DEFAULTTONEAREST), ref mi)) return;
    var scale = VisualTreeHelper.GetDpi(w).DpiScaleY;          // 这块屏自己的缩放
    var cap = (mi.rcWork.Bottom - mi.rcWork.Top) / scale - 72;  // 留点上下呼吸
    w.MaxHeight = Math.Max(cap, w.MinHeight);                   // 不能低于自己声明的下限
    if (!double.IsNaN(w.Height) && w.Height > cap) w.Height = cap;
};
```

三个点容易写错。一是别用 `SystemParameters.WorkArea`，它给的是**主屏**的工作区，而声明了 PerMonitorV2 之后不存在「整个桌面一个尺寸」，对话框又通常是 `CenterOwner`，主窗口在副屏时就错了。二是 DPI 换算直接用 `VisualTreeHelper.GetDpi(窗口)`，PerMonitorV2 下它返回的就是该窗口那块屏的缩放，不必自己去 P/Invoke `GetDpiForMonitor`。三是 `GetMonitorInfo` 的返回值必须判：不判的话探测失败时 `mi.rcWork` 全是零，`cap` 算成负数，`Math.Max(cap, w.MinHeight)` 会把窗口按到 `MinHeight` 上——那可不是「退回 XAML 里那个保守值」，而是把对话框压成一条。

XAML 保留按最小支持工作区选定的兜底值，供探测失败时使用；工作区 DIP 样例及运行时按钮边界验收统一见[布局检查](dev-switches.md#截图的盲区)，不要沿用已知会溢出的旧上限。

### 窗口封顶了，正文和按钮仍可能在屏外

`FitToWorkArea` 限制窗口，不一定约束 `SizeToContent="Height"` + `AllowsTransparency="True"` 下的正文测量。长正文仍可能把按钮挤出工作区；整窗离屏截图也可能包含屏外按钮。需要同时限制可滚动正文并验证按钮屏幕坐标。

修法是给**正文内容**再封一次，取窗口所在那块屏的工作区（不是主屏），并留出标题/按钮/边距：

```csharp
w.SourceInitialized += (_, _) => {
    var workHeight = WorkAreaHeightInDips(w);   // 与上面的 FitToWorkArea 共用同一份；失败返回 0
    if (workHeight > 0)
        msgScroll.MaxHeight = Math.Clamp(workHeight * 0.35, 120, 320); // 比例/上下限按字体和按钮行实测
};
```

保留窗口 `MaxHeight`，另用超长正文覆盖此分支，按[布局验收](dev-switches.md#截图的盲区)检查实际按钮位置。

## 深色应用配了个白色标题栏

看着像窗口只重绘了一半。`DWMWA_USE_IMMERSIVE_DARK_MODE` 的值是 20（[官方枚举](https://learn.microsoft.com/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute)，标注 Win11 build 22000 起支持），要在 `SourceInitialized` 里调用，那时候 HWND 才存在：

```csharp
// hwnd 从 new WindowInteropHelper(w).Handle 取，SourceInitialized 之后才非零
int dark = isDarkTheme ? 1 : 0;
DwmSetWindowAttribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ref dark, sizeof(int));
```

要覆盖 Win10 的话还有一档历史包袱：这个属性在 Win10 build 18985 之前的编号是 **19**，用 20 调过去会被静默忽略（`DwmSetWindowAttribute` 对不认识的编号返回错误码，不抛异常）。稳妥写法是先试 20、失败再试 19，两次都不判返回值就会得到「Win11 好好的、Win10 上标题栏还是白的」。

## 应用突然消失，没留下任何日志

WPF 默认在 UI 线程抛出未捕获异常时直接退进程，用户只看到窗口凭空消失。三个入口都要挂：

```csharp
DispatcherUnhandledException                // UI 线程
AppDomain.CurrentDomain.UnhandledException  // 其他线程
TaskScheduler.UnobservedTaskException       // 没有 await 的 Task
```

仅对可恢复的 UI 异常设置 `e.Handled = true` 并提示；无法保证状态一致时不要强行继续运行。`AppDomain` 那个进来时进程已经在终止；`TaskScheduler` 那个默认不杀进程（.NET 4.5 起未观察的任务异常不再升级，.NET Core / 5+ 沿用这个默认），但异常已经发生、还要等 GC 回收任务时才浮出来——两个都只能把堆栈写进日志。日志可简单追加时间戳与异常，写到产品约定的可写数据目录；不要因便携形态就假定 exe 同级可写，也不为日志放宽受保护程序目录权限。

三个入口都挂了、日志还是空的，就要考虑第四种消失：**它不是异常，是某处代码正常地调了 `Shutdown()`**——异常处理器一个都不会响。临时给关闭事件挂个栈探针，让肇事者自报家门：

```csharp
Dispatcher.ShutdownStarted += (s, e) =>
    File.AppendAllText(log, "ShutdownStarted:\r\n" + Environment.StackTrace + "\r\n");
```

初始化赋值触发 `SelectionChanged` 等业务事件时，可能沿正常逻辑排队调用 `Shutdown()`。同时检查关闭调用点与 Dispatcher 操作；关闭开始后 `Window.Show()` 可能不抛异常却产生零尺寸窗口，smoke 需验证布局结果。

## 绿色版把配置写到了盘符根目录

单文件发布下 `Assembly.Location` 返回空字符串，拿它拼 exe 同级路径会落到盘符根目录。要用 `AppContext.BaseDirectory` 或 `Environment.ProcessPath`，写开机自启的注册表项时同理。

## 扫用户目录，一处读不了就颗粒无收

递归扫描遇到拒绝访问的目录时，不能让根目录级 `catch` 丢掉全部已采集结果。对允许部分结果的选择器，可使用以下选项并在最小失败范围处理错误；需要完整采集的审计则报告被跳过的范围。

按功能选择 `EnumerationOptions`，例如跳过隐藏/系统目录和重解析点：

```csharp
new EnumerationOptions {
    RecurseSubdirectories = true,
    IgnoreInaccessible = true,   // 读不了的跳过去接着走，而不是掀桌子
    // 一旦设了这个属性，默认的 Hidden|System 就不再自动生效，要显式写全
    AttributesToSkip = FileAttributes.Hidden | FileAttributes.System | FileAttributes.ReparsePoint,
}
```

`ReparsePoint` 那一项顺带解决第二个问题：那个联结只是 `Programs` 的另一个名字，跟进去等于把整棵树数两遍。

Shell 命名空间枚举也按条目隔离属性读取失败，保留其余结果。跟随重解析点时另行处理循环与重复，不把跳过目录误报为完整扫描。

## 要启动的应用没有 exe 路径，也没有快捷方式

打包 / Store 应用可能没有可直接选择的 exe 或快捷方式。应用选择器还需考虑 AUMID。

它们能被 `ShellExecute` 启动，写法是 `shell:AppsFolder\<AUMID>`。名字和 AUMID 从 shell 命名空间里枚举：

```csharp
dynamic shell = Activator.CreateInstance(Type.GetTypeFromProgID("Shell.Application"));
foreach (dynamic item in shell.NameSpace("shell:AppsFolder").Items())
{
    string name = item.Name;      // 显示名
    string aumid = item.Path;     // 打包应用形如 Family!AppId
}
```

三个实际会咬人的细节：

- **先扫 `.lnk`、后补 AppsFolder，顺序不能反。** 经典程序两边都有，而快捷方式带着参数、工作目录和图标，比一串 AUMID 完整得多；反过来几百个经典程序会被 AUMID 版本先占住名字。按显示名去重即可，AppsFolder 只补那些 `.lnk` 里没有的。
- **AppsFolder 里混着 `.url` 条目**，它们的「AUMID」本身就是一条网址。套上 `shell:AppsFolder\` 前缀只会做出一个打不开的目标；含 `://` 就原样当网址用。
- **这串东西不是路径也不是 URL**：`Path.IsPathRooted` 认不出（冒号在第 6 位不是第 2 位），从它也推导不出进程名——所以「已在运行则激活窗口」这类优化会自动空转，正好是想要的。

顺带一提，执行侧本来就没有后缀白名单：`UseShellExecute = true` 意味着凡是资源管理器双击能打开的都能开（exe、bat、lnk、文档、文件夹、`ms-settings:` 这类协议、有关联的脚本）。唯一需要特判的是 `.ps1`——它的默认关联是**编辑**不是运行，直接 ShellExecute 会打开记事本，得显式 `powershell.exe -File`。所以「支持的后缀太少」这种反馈，多半问题不在后缀。

## 德语界面上控件被挤没

同一个界面，中文标签短，德语和俄语能长出一倍，容器选错就会有控件被挤没。

| 容器                    | 给子元素的可用宽度 | 宽度不够时                         |
| ----------------------- | ------------------ | ---------------------------------- |
| StackPanel（水平）      | 无限               | 子元素永不换行，超出部分被上层裁掉 |
| DockPanel               | 按声明顺序递减     | 最后停靠的元素可能一点宽度都拿不到 |
| Grid 的 `*` 列          | 按剩余空间分配     | 正常收缩，配合 TextTrimming 截断   |
| Grid 同一格放多个子元素 | 各自拿满整格       | 并列元素互相重叠                   |
| WrapPanel               | 放不下就换行       | 按钮组不会互相挤没                 |

水平 StackPanel 传给子元素的可用尺寸是 `double.PositiveInfinity`，子元素被告知想多宽都行，`TextBlock` 于是永远不会换行。所以控件模板里如果用水平 StackPanel 包住 `ContentPresenter`，这个控件的文字标签在全应用范围内都不可能换行，外面套多少层 Grid 都没用。DockPanel 则按声明顺序分配，三个 `Dock="Left"` 的按钮加一个 `Dock="Right"` 的关闭按钮，标签一长关闭按钮就只剩几个像素。

规则是：一行里只要有必须可点的东西，就用 Grid 的 `Auto` 列先把它的宽度锁住，剩下的交给 `*` 列去截断或者交给 WrapPanel 去换行。

**但对「打开选择器」那类按钮，有个更便宜的解法：不给它文字。** 表单行末尾那颗「浏览…」按钮是最典型的受害者——中文三个字，德语是 `Durchsuchen…`、俄语 `Обзор…`，宽度差四倍，而它正好排在行尾、后面就是滚动条，于是德语下被整个裁掉、点都点不着。改成只画一个「…」（Windows 上「点开会弹选择框」的通用记号）之后，**整行所有元素都变成定宽、与语言无关**，从根上不会再溢出——比把十几行重构成 Grid 便宜得多，效果一样。文案挪到 `ToolTip` 和 `AutomationProperties.Name`，鼠标停一下能看到，读屏软件照样念得出来。

写这个样式时有一个静默陷阱：**具名 Style 不会自动继承隐式样式**。

```xml
<Style x:Key="PickerButton" TargetType="Button" BasedOn="{StaticResource {x:Type Button}}">
```

漏掉 `BasedOn` 那一句，按钮会掉光配色和模板，变成系统默认的灰按钮——而且它不报错，只是长得不对。

顺带一条同类的间距问题：滚动区里的内容默认会一直铺到滚动条跟前，定宽控件还剩点余量，那些换行的说明文字（只有左边距、没有宽度）则正好顶在滚动条上。修法是给 `ScrollViewer` 加 `Padding`——默认模板把它落到内容承载器的 `Margin` 上，而滚动条在另一个网格列里，所以它正好只撑开这条缝，不影响滚动条本身。

**这条规则可以机械化，别只当成 review 要点。** 判据是纯结构的，扫 XAML 就能查：

> `TextWrapping="Wrap"` 的 `TextBlock`，若父容器是水平 `StackPanel`
> （给子元素的可用宽度是无限），而它自己**既没有 `Width` 也没有 `MaxWidth`**
> —— 那么换行永远不会发生，写的那个 `Wrap` 是一句空话。
>
> `WrapPanel` 不在这条规则里：它给子元素的是可用宽度，放不下才换行（见上表）。只有
> `WrapPanel` 自己被放进无限宽的测量里时才会把无限传下去，那种情况要沿祖先链看。

源码检查需排除已设置 `Width` / `MaxWidth` 的控件，并考虑绑定和祖先约束，避免把合法换行判成缺陷。优先用 `Grid` 的 `*` 列提供有限宽度；确需无限宽父容器时再为文本设置上限。长译文与条件性 UI 的验证见 `dev-switches.md`。

还有一个反直觉的组合要避开。给带 `TextTrimming` 的 `TextBlock` 加 `MinWidth`，会让它的测量宽度超过所在单元格，负责截断的主体就从 TextBlock 变成父容器的裁剪。TextBlock 自己截断是从文本末尾切并补省略号，父容器裁剪只按流向切掉超出部分。左到右布局下切的是尾巴看不出问题，阿拉伯语这种右到左布局下切掉的是字符串开头，而且没有省略号。

## 切了语言，日期还是英文格式

**WPF 的绑定做日期和数字格式化时不看 `CurrentCulture`，看的是元素上的 `Language` 属性，而它的默认值写死是 en-US**。想让日期数字跟着界面语言走，启动时、**建第一个窗口之前**补一句（`OverrideMetadata` 晚调不报错，但官方文档明说实例存在后再改元数据"行为会不一致"；重复调则直接抛 `ArgumentException`，所以也别放进会跑多遍的路径）：

```csharp
FrameworkElement.LanguageProperty.OverrideMetadata(
    typeof(FrameworkElement),
    new FrameworkPropertyMetadata(
        XmlLanguage.GetLanguage(CultureInfo.CurrentCulture.IetfLanguageTag)));
```

但先想清楚要不要跟。另一条同样成立的取舍是**文案跟界面语言、日期数字跟系统区域**——只设 `CultureInfo.DefaultThreadCurrentUICulture`（注意 `Thread.CurrentThread.CurrentUICulture` 只对当前线程生效，之后新起的线程不跟），格式化完全不动。用户系统里日期长什么样，应用里就长什么样，比跟着界面语言跳更少被问「格式怎么变了」。走这条路线就不要加上面那句 override。两条路线选一条，整个应用保持一致。

阿拉伯语这类右到左的语言，`FlowDirection` 可以在启动时 `FrameworkElement.FlowDirectionProperty.OverrideMetadata(typeof(Window), …)` 一次设到所有窗口。但有三类东西继承不了，得逐个控件过：硬编码的单边 `Margin="0,0,8,0"`、有方向性的图标（箭头和播放键要镜像）、写死的 `TextAlignment="Left"`。

## 测试工程引用 App 就报 NETSDK1151

先检查发布属性是否写在 csproj，导致测试引用了自包含可执行工程；这些属性也会影响日常 build/run。将 `RuntimeIdentifier`、`SelfContained`、`PublishSingleFile` 移入 [pubxml](project-setup.md#发布四份-pubxmlx64--arm64--自包含--框架依赖csproj-一个发布属性都不放)。该节也统一说明压缩、原生库提取和独立输出目录；`NETSDK1176` 则检查是否为框架依赖包启用了单文件压缩。不在测试工程再补一套相反属性。

## 开了 ReadyToRun 反而更慢

压体积别往 `PublishTrimmed` 和 NativeAOT 上想，[微软官方文档](https://learn.microsoft.com/dotnet/core/deploying/trimming/incompatibilities)写得很直接：WPF 大量用反射，裁剪后几乎跑不起来，所以 .NET SDK 里 WPF 的裁剪支持是关闭状态。剩下的就只有 `EnableCompressionInSingleFile` 和 `PublishReadyToRun`，后者默认别开。

压缩也有启动时解压成本，需一起测量包体积与启动时间。[官方说明](https://learn.microsoft.com/dotnet/core/deploying/single-file/overview#compress-assemblies-in-single-file-apps)。压缩可用范围按 [pubxml 配置](project-setup.md#发布四份-pubxmlx64--arm64--自包含--框架依赖csproj-一个发布属性都不放)执行。

比较 R2R 开关前后的产物大小与启动耗时，并分开测首次解包、冷启动和热启动；不要无条件丢弃第一次运行，它可能正是需要优化的用户场景。热启动对照先稳定缓存状态，冷启动则控制相同条件。

框架程序集已有预编译映像，额外收益取决于应用代码在启动路径中的占比。按各发布 profile 分别决定，只有收益足以抵消体积与构建成本时才启用；取舍说明留在项目配置附近。

## 文档里的体积数字，发两版就对不上了

文档说明自包含版与框架依赖版的使用差异，确切包大小链接发布资产列表。避免在多语言 README 中复制每版都会变化的大小；需要讨论构建选项收益时，用同一条件的增量对照。

## 版本号发出去还是上一版

发布物的版本号别写死在 csproj 里，手写的字面量一定会忘记改。从 git tag 取：

```xml
<Target Name="VersionFromGitTag" BeforeTargets="GetAssemblyVersion"
        Condition="'$(Version)' == '$(VersionFallback)'">
  <Exec Command="git describe --tags --abbrev=0" ConsoleToMSBuild="true"
        IgnoreExitCode="true" StandardOutputImportance="low">
    <Output TaskParameter="ConsoleOutput" PropertyName="_GitTag"/>
    <Output TaskParameter="ExitCode" PropertyName="_GitTagExit"/>
  </Exec>
  <PropertyGroup Condition="'$(_GitTagExit)' == '0'">
    <Version>$(_GitTag.TrimStart('v'))</Version>
  </PropertyGroup>
</Target>
```

两道 `Condition` 都是承重的，但**不是**因为「Target 内部的 PropertyGroup 会覆盖命令行传进来的全局属性」：`-p:` 传进来的是全局属性，工程内的赋值盖不掉它（除非在 `<Project>` 上写 `TreatAsLocalProperty`），所以「旧 tag 顶掉新版本号」这件事本来就不会发生。它们各自防的是别的：外层 `'$(Version)' == '$(VersionFallback)'` 让 CI 传了 `-p:Version` 时整个 Target 跳过，省掉白跑的一趟 `git describe`；内层 `'0'` 管没有 tag 的场合，少了它 `_GitTag` 就是空串，`<Version>` 被赋成空值，csproj 里那个 `$(VersionFallback)` 当场作废。

`IgnoreExitCode` 也别写成 `ContinueOnError`，后者只是把失败降级成警告，仍然每次构建刷两条 MSB3073，而仓库里没有 tag 是 CI 的常态，浅克隆默认就不带 tag。CI 里记得给 checkout 加 `fetch-depth: 0`，否则拿不到 tag。

## XAML 写错了却一路带到发版

编译成功没有覆盖所有窗口的懒加载 XAML；按 [smoke 实现及 CI 判定](dev-switches.md#--smokeci-里防-xaml-错误带到发版)逐窗构造与布局。

## 整个桌面点不动，只有杀掉桌面窗口管理器才恢复

全屏置顶覆盖窗所属的 UI 线程挂起时，系统 ghost window 可能改变点击穿透行为。先用窗口枚举确认输入被哪一层拦截，不把关闭 `dwm.exe` 当作常规排障步骤。

优先避免阻塞覆盖窗线程。确需 `DisableProcessWindowsGhosting()` 时，了解它对整个进程且不可逆的影响，并在生产和自检的覆盖窗创建前统一初始化。验证真实执行顺序，不要求调用必须写在同一个文件；公共初始化函数同样有效。自检侧隔离见 `dev-switches.md`「harness 初始化与副作用」，全局输入钩子测试见同页对应小节。

## 非模态窗口上的 IsCancel="True" 静默失效

症状：在二级窗口（设置、操作历史、关于、预设等）里写了 `<Button Content="取消" IsCancel="True" />`，点击「取消」按钮窗口毫无反应，按键盘 <kbd>Esc</kbd> 窗口也不关闭。

根因：WPF 的 `Button.IsCancel = true` 仅在**模态对话框（`ShowDialog()`）** 中会自动设置 `DialogResult = false` 并关闭窗口。在托盘小工具广泛使用的**非模态窗口（`Show()`）** 中，设置 `DialogResult` 会直接抛出 `InvalidOperationException`；WPF 在非模态下仅负责把 <kbd>Esc</kbd> 键转发给该按钮的 `Click` 事件。若按钮**没有显式绑定 `Click` 事件或 `Command`**，点击和 <kbd>Esc</kbd> 都会**静默失效（完全没有任何操作发生）**。

改法：非模态窗口的取消/关闭按钮不能偷懒，必须显式挂载 `Click="OnCancel"`（后台调用 `Close()`）或绑定 Command：

```xml
<!-- 错误：非模态窗口下静默失效，关不掉窗口 -->
<Button Content="取消" IsCancel="True" />

<!-- 正确：显式绑定 Click 或 Command -->
<Button Content="取消" IsCancel="True" Click="OnCancel" />
```

```csharp
private void OnCancel(object sender, RoutedEventArgs e)
{
    // 若绑定的 ViewModel 支持未保存改动回滚，取消时需重新从磁盘加载配置
    if (DataContext is SettingsViewModel vm)
    {
        vm.CancelCommand.Execute(null); // 内部执行 _settingsService.Load() 回滚内存改动
    }
    Close();
}
```

## DI 容器里的窗口注册成单例，关闭后第二次打开必崩

症状：开机后首次打开「设置」或「历史」窗口一切正常，点击右上角 `X` 或「取消」关闭窗口后，再次从托盘菜单或快捷键打开该窗口时，程序直接抛出未捕获异常崩溃：
`InvalidOperationException: Cannot call Show on a window after it has closed.`

根因：WPF 的 `Window.Close()` 会永久销毁 Win32 原生窗口句柄（HWND），**已被 Closed 的 Window 实例绝不可再次调用 Show**。若在依赖注入（DI）容器中把二级窗口注册为 `AddSingleton<SettingsWindow>()`，关闭后该窗口虽然脱离了可视树，但在 DI 容器中仍然活着；第二次调用 `GetRequiredService<SettingsWindow>()` 拿到的是已销毁 HWND 的死对象，调用 `.Show()` 必崩。

改法：
1. **按生命周期注册**：会 `Close()` 的窗口使用 transient 或工厂创建新实例；需要单例复用的窗口采用取消关闭并 `Hide()` 的生命周期。
2. **防重复实例的打开封装**：

```csharp
private void OpenWindow<TWindow>() where TWindow : Window
{
    if (_host is null) return;

    // 1. 若当前已有活着并显示的实例，直接激活置顶，避免重复开窗
    var existing = Application.Current.Windows.OfType<TWindow>().FirstOrDefault();
    if (existing is not null)
    {
        if (!existing.IsVisible) existing.Show();
        WindowEffects.BringToFront(existing);
        return;
    }

    // 2. 没有活着的实例，通过 DI 解析新的 Transient 实例并打开
    var window = _host.Services.GetRequiredService<TWindow>();
    window.Show();
}
```

主窗口和工具窗口都按实际关闭/隐藏策略选择生命周期，验证首次打开、关闭后重开及应用退出。

## 托盘常驻应用的临时导出/物化文件长期堆积

OLE `CF_HDROP` 拖出需要本地路径，内存或 Blob 内容必须先物化。托盘应用可能长期不退出，只在启动时清理会持续积累文件。

- 按接收方的实际读取周期选择保留期，跟踪活动拖放，避免删除仍会被使用的文件；文件未锁定不等于已无人使用。
- 在常驻任务与退出流程中清理已过期且归本应用管理的文件，隔离处理失败，不按固定时长套用所有产品。
- 手动清理覆盖同一目录与规则，刷新实际剩余占用；仍在使用或清理失败的文件如实显示，不强制归零。

## 双形态窗口在多屏切换时坐标跳跃与越界

症状：在双屏或多屏混合 DPI 环境下，迷你小窗展开成大工作台时，窗口偶尔会跳到另一台屏幕上；或者展开后窗口标题栏超出了屏幕上边界无法拖动。

根因：
1. 不同形态共用同一组坐标缓存，展开大窗时直接套用迷你窗的左上角坐标，导致大窗口右侧或底部溢出屏幕。
2. 使用 `SystemParameters.WorkArea` 误取主屏工作区，副屏上的窗口展开时被主屏工作区范围强行纠正，产生跨屏飞跃。
3. 展开时未基于 `MonitorFromWindow` 重新计算并执行安全边界钳制。

改法：
1. 按形态分别缓存坐标（如 `_compactPosition` 与 `_workbenchBounds`）。
2. 尺寸切换前通过 Win32 `MonitorFromWindow` 获取窗口当前所在的实际屏幕工作区。
3. 扩展尺寸后必须执行 `ClampToWorkArea(window)` 钳制，确保窗口右上角、标题栏永远在屏幕可视安全区内。

## 右键菜单和外壳扩展项显示 Windows 默认白纸图标

症状：应用各窗口在运行时任务栏显示正常、窗口左上角图标也对，但是在 Windows 资源管理器右键扩展菜单项（Shell Context Menu，如「加入暂存」）、发送到菜单（SendTo）、或者未固定的外部快捷方式上，却显示为 Windows 默认的通用白纸程序图标。

Explorer 读取 EXE 的 Win32 PE 图标，XAML 窗口 Icon 不会补上该资源。配置及验证统一见[应用原生图标](project-setup.md#应用原生图标)，安装器图标见 [Inno 配置](project-setup.md#inno-setup-6-最佳实践配置要点)；同时核对 Shell 注册的实际图标路径。

## WindowChrome 自定义标题栏上的按钮点不动（命中测试被吃掉）

症状：为消除 Windows 原生厚重且割裂的默认标题栏（首栏），在窗口上应用了 `WindowChrome`（如 `CaptionHeight="40"`）实现无边框沉浸式顶栏。但嵌入在顶栏中的自定义控件（关闭按钮 `✕`、置顶图钉 `📌`、操作图标按钮、拖拽手柄）点击完全没有反应，鼠标移动上去甚至没有 Hover 状态变化。

根因：`WindowChrome` 默认将 `CaptionHeight` 范围内的整个矩形区域转译为 Win32 原生 `HTCAPTION`（窗口拖拽非客户区）。操作系统捕获了 `HTCAPTION` 消息并接管了拖拽手势，导致 WPF 内部的路由事件系统（`MouseDown`、`MouseEnter`、`Click`）完全被旁路吃掉。

改法：所有需要响应鼠标点击、悬浮或拖拽手势的子元素，必须显式附加 `WindowChrome.IsHitTestVisibleInChrome="True"`。父级 Grid / Border 容器保持不设该属性，控件之间的空白区域仍可原生保留拖拽窗口与双击最大化：

```xml
<WindowChrome.WindowChrome>
    <WindowChrome CaptionHeight="40" ResizeBorderThickness="6" CornerRadius="0" GlassFrameThickness="0" UseAeroCaptionButtons="False" />
</WindowChrome.WindowChrome>

<!-- 顶栏中的交互按钮必须显式声明命中测试穿透 -->
<Button WindowChrome.IsHitTestVisibleInChrome="True" Click="OnCloseClick" ... />
```

## 提取文件原生图标卡死 UI 线程并泄漏 GDI 句柄

症状：文件列表或暂存架需要展示每个文件的 Windows 原生图标（真实关联的 Word、Excel、VS Code、PDF 等）。使用 Win32 `SHGetFileInfo(filePath, ...)` 提取图标时，遇到深层网络路径、离线 U 盘、只读受限或大文件时，UI 线程出现明显顿挫甚至数秒无响应；运行数天后程序更可能由于 GDI 句柄耗尽崩溃。

根因：
1. `SHGetFileInfo` 默认会尝试真实访问磁盘以获取属性，带来同步磁盘/网络 I/O 阻塞；
2. 提取出来的 Win32 原生 `HICON`（句柄）通过 `Imaging.CreateBitmapSourceFromHIcon` 转换为 WPF 位图后，若未显式调用 `DestroyIcon`，会造成底层 GDI/USER 句柄泄漏（Windows 单进程上限为 10,000 个）。

改法：采用合成虚拟路径并加上标志 `SHGFI_USEFILEATTRIBUTES` 配合 `FILE_ATTRIBUTE_NORMAL`。此标志让 Shell 按提供的文件属性查关联图标，目标文件可以不存在。首次加载图标和 Shell 扩展仍可能耗时，在后台线程查询并缓存结果。在 `finally` 中销毁句柄并 `Freeze()` 缓存位图：

```csharp
[DllImport("shell32.dll", CharSet = CharSet.Auto)]
static extern IntPtr SHGetFileInfo(string pszPath, uint dwFileAttributes, ref SHFILEINFO psfi, uint cbFileInfo, uint uFlags);

[DllImport("user32.dll", SetLastError = true)]
static extern bool DestroyIcon(IntPtr hIcon);

const uint SHGFI_ICON = 0x000000100;
const uint SHGFI_SMALLICON = 0x000000001;
const uint SHGFI_USEFILEATTRIBUTES = 0x000000010;
const uint FILE_ATTRIBUTE_NORMAL = 0x00000080;

private static readonly ConcurrentDictionary<string, ImageSource> _cache = new(StringComparer.OrdinalIgnoreCase);

public static ImageSource GetIconForExtension(string ext)
{
    if (string.IsNullOrWhiteSpace(ext)) ext = ".dat";
    return _cache.GetOrAdd(ext, static extension =>
    {
        var shinfo = new SHFILEINFO();
        IntPtr hImg = SHGetFileInfo("dummy" + extension, FILE_ATTRIBUTE_NORMAL, ref shinfo,
            (uint)Marshal.SizeOf(shinfo), SHGFI_ICON | SHGFI_SMALLICON | SHGFI_USEFILEATTRIBUTES);
        if (hImg == IntPtr.Zero || shinfo.hIcon == IntPtr.Zero) return FallbackIcon;
        try
        {
            var bs = Imaging.CreateBitmapSourceFromHIcon(shinfo.hIcon, Int32Rect.Empty, BitmapSizeOptions.FromEmptyOptions());
            bs.Freeze(); // 冻结位图以便安全跨线程共享
            return bs;
        }
        finally
        {
            DestroyIcon(shinfo.hIcon); // 彻底杜绝 Win32 GDI 句柄泄漏
        }
    });
}
```

## 全局热键长按疯狂连发与按键穿透（MOD_NOREPEAT 与按键录制盒）

症状：
1. **长按连发**：用户按住全局热键（如 <kbd>Win</kbd>+<kbd>Alt</kbd>+<kbd>S</kbd>）不松手时，系统按键重复触发，导致浮动小窗疯狂交替开闭闪烁，甚至热键中的字符键（如 S）被当作普通字符打入了当前活动的应用中。
2. **手动输入体验差**：设置界面用普通的 `TextBox` 让用户手打快捷键字符串，极易因空格、大小写、键名拼写错误（如 `Ctrl` vs `Control`）导致静默注册失败。

根因：
1. Win32 `RegisterHotKey` 默认在按键按住时持续发送 `WM_HOTKEY` 消息；
2. 普通文本框无法感知原始 Virtual Key 与修饰键组合状态。

改法：
1. 注册 Win32 热键时加入 `MOD_NOREPEAT = 0x4000` 标志位，由 Windows 内核直接抑制长按重复触发：

```csharp
const uint MOD_NOREPEAT = 0x4000;
RegisterHotKey(hwnd, id, modifiers | MOD_NOREPEAT, vk);
```

2. 编写专用交互式录制控件 `HotkeyBox : Control`：通过 `PreviewKeyDown` 拦截原始 `KeyEventArgs` 并设 `e.Handled = true`；提取 `Keyboard.Modifiers` 并针对 `Key.System` 获取 `e.SystemKey`，支持按 <kbd>Esc</kbd> 取消录制、按 <kbd>Backspace</kbd>/<kbd>Delete</kbd> 清除，标准化序列化为统一格式（如 `Win+Alt+S`）。

## 切换开机启动方式后，设置和系统实际状态不一致

本应用普通／管理员自启切换，统一按 [注册交互式管理员任务](startup.md#注册交互式管理员任务) 检查事务、系统回读、取消与回滚；模板结果映射见 [接入步骤](startup-template.md#接入步骤)。

接管外部启动项到自己的启动清单时，先确认清单真正保存成功，再禁用原项；`void Save()` 返回并不能证明落盘成功。禁用失败时撤销本次新增或启用变更，保存回滚结果；回滚保存也失败时如实报告。按启动类型、目标、参数和工作目录判断等价，避免把同一程序的不同启动方式吞成一条。

## 提权重试进程在跑，却没有可操作的确认框

先用阶段日志区分：是否取得管理员令牌、是否读到待确认范围、是否显示确认框、是否取消或完成。进程存活和 `RunAs` 启动成功都不能证明确认框可操作。

- **独立确认框的启动时序**：没有主窗口的 helper 若在早期 `OnStartup` 里直接进入异步／模态流程而卡住，可把这段工作排到 Dispatcher 消息循环启动后执行；例如使用 `BeginInvoke` / `ApplicationIdle` 调度。核对应用的 ShutdownMode，完成或取消后显式结束 helper；不要为了单条分支改掉整个应用的窗口生命周期。
- **没有 owner，也没有任务栏入口**：检查 ownerless 对话框的 `ShowInTaskbar`，以及另一个置顶窗口是否盖住了按钮。独立提权确认框可以显示任务栏入口；不要因此让所有普通工具窗都进任务栏。窗口可被枚举或截图，不代表当前自动化进程有能力向高权限窗口发送输入；点击无响应时交由用户操作，再核对结果。
- **提权后读到另一个数据库**：不要假设 RunAs 子进程会沿用父进程的数据目录环境。需要共享隔离数据目录时，由启动器明确传递必要参数，子进程在创建路径、设置和服务之前验证并应用。使用 `ArgumentList`，兼容旧变量名时统一处理空白值；限制专用参数只在相应 helper 模式生效。不要把父进程的全部命令行或环境不加区分地转发。

文件写回类提权重试还有一个授权边界：确认窗口显示的目标路径、动作、内容摘要应来自冻结的条目集合；批准后再核对历史记录没有改变，并校验实际写入字节。不要只凭一个操作 ID，在用户确认后重新查询并执行扩大了的失败列表。按产品权限边界决定读取和备份目标内容的时机。取消时不执行重试业务写入。实际验证方法见 `dev-switches.md`「人工交互验收」。

## 配置损坏后，自动保存把原文件覆盖成默认配置

读取配置失败后用默认值继续展示界面，随后语言解析、迁移或控件初始化又触发公共保存入口，原始损坏文件就被默认配置覆盖了。只拦退出保存，或只跳过一次保存，都挡不住这些路径。

保留独立的「原配置未读成功」状态，在共同写入入口守住；不能用「当前模型存在」代表原文件可覆盖。备份成功也不等于可以自动重置。备份失败要报告实际错误，恢复写入应沿用产品明确的修复流程。测试用临时损坏文件走读取、初始化和公共保存链，断言原始字节未变，并覆盖备份失败。

## 后台扫描完成了，筛选列表仍然卡顿

把扫描入口放进 `Task.Run` 后，搜索或切换筛选仍会卡住：筛选谓词、行属性 getter 又根据路径调用了 `File.Exists` / `Directory.Exists`。网络目录和离线路径的延迟因此重新落到 UI 线程上。

在后台扫描阶段计算分类结果，并按目录复用探测；UI 过滤读取已计算的值。若后台结果缓存跨线程共用，检查其线程安全。用注入的慢探测计数器验证同目录只查一次、后续过滤不再查磁盘；模拟延迟只能证明调用边界，真实网络盘仍需单独实测。

## 面板里已保存编辑，主窗口列表仍显示旧值

两个入口共享同一个模型，但各自持有行 ViewModel。模型就地修改后，`ObservableCollection` 本身没有增删事件，行也没有发属性通知，磁盘保存成功仍不会更新另一处展示。

沿现有保存回调通知相关列表刷新或重建行，并尽量保留选中项；局部刷新能解决时无需增加全局事件总线。用于跳过重建的签名必须覆盖显示字段及身份字段，否则内容变了仍会被当作未变。回归测试同时断言另一入口的行值已更新、保存重读一致；复制和排序还要检查重读后的父引用与执行顺序。

## 更新缓存里有 exe，却可能是上次中断留下的半成品

直接解压到最终版本目录，下次只凭 `File.Exists` 命中缓存，会把未完成提取的文件报告成可用。并发检查也可能互相覆盖暂存文件。另一个容易混淆的分支是把所有 HTTP 404 都当作「没有新版」：元数据不存在与发布资产缺失应分别处理。

在同卷唯一暂存目录内完成下载、校验与提取，确认预期 exe 后再移动到最终目录。既有缓存需要完成标记及内容核验；本地摘要能检查意外损坏，不能代替可信来源验证。替换无效旧缓存时保留恢复路径，失败后清理本次暂存目录。进程内并发用互斥保护；它不覆盖多进程竞争，先核对应用的单实例边界。

用 HTTP 替身与临时目录覆盖中断缓存、篡改、提取失败后的重试、并发调用及不同阶段的 404。不要在测试中执行下载内容，或覆盖用户正在运行的 exe。

## 安装后应用名称在系统列表中带有「version xx」

检查 Inno Setup 是否缺少 `UninstallDisplayName`；配置只保留在 [Inno 要点](project-setup.md#inno-setup-6-最佳实践配置要点)，修改后核对系统应用列表中的实际名称。

## 普通权限主进程中检测管理员身份永远返回 False（UAC 分割令牌）

设置页在弹出 UAC 前就认定本地管理员是标准用户：先区分账户资格与当前进程权限。令牌判断及模板复用入口见 [账户资格与当前权限](startup.md#账户资格与当前权限)。

## 开机提权自启错误拦截非 Program Files 路径（将推荐部署误当成平台硬性要求）

便携／自定义目录被 `StartsWith(ProgramFiles)` 或 ACL 前置校验拒绝，且尚未调用任务 API：按 [路径策略](startup.md#选择权限与部署方式) 核对产品约束与提示文案。
