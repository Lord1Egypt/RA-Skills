# WPF 项目起手：装什么、建什么、怎么发布

这页负责组件选型、项目与发布配置。版本目标和升级流程见[依赖升级](upgrade-dependencies.md)，故障见 [pitfalls.md](pitfalls.md)，验证工具见 [dev-switches.md](dev-switches.md)，CI 与交付验收见 [github-actions.md](github-actions.md)。

## 第一个项目装什么

下表用于选择组件，示例中的具体 SDK 和 NuGet 补丁号按依赖升级流程重新解析。

| 位置       | 选它                                          | 什么时候才该换                                                        |
| ---------- | --------------------------------------------- | --------------------------------------------------------------------- |
| 目标框架 | `net10.0-windows` | 适用于新建、整体升级或确需框架迁移；局部修复按[升级范围](upgrade-dependencies.md#对齐技能指定的大版本)执行，保留所需 Windows 最低版本。 |
| SDK 版本 | global.json 记录完整 SDK 版本及 rollForward 策略 | 构建环境安装并验证目标稳定 SDK。项目需兼容较低开发 SDK 时，在 CI 单独安装目标补丁。 |
| 依赖锁 | 示例使用精确 PackageReference；已有锁文件保留 | 单文件发布时验证 SDK 隐式依赖与锁文件是否一致，见下文「NuGet 锁文件与单文件发布」。 |
| 开发环境   | VS 2026 Community 加「.NET 桌面开发」工作负载 | 手里已经有 Rider 就用 Rider。面向 net10.0 的 IDE 至少需要 VS 18.0，见下文的 SDK 对应表 |
| 编辑器扩展 | 先用 IDE 已有能力 | 按实际缺口增加，例如多语言资源管理。 |
| MVVM       | `CommunityToolkit.Mvvm`                       | 窗口少、状态简单的小工具，直接 code-behind 也成立                     |
| 托盘图标   | `H.NotifyIcon.Wpf`                            | 工程本来就开了 `UseWindowsForms` 时，用内建的 NotifyIcon              |
| 界面主题 | 可先试自带 Fluent 与语义资源 | 按所需控件、导航和维护成本选择库，保留已有主题方案。 |
| 配置文件 | 默认 System.Text.Json | 已有格式和迁移兼容性优先。 |
| 日志       | 自己往文件里追加一行                          | 需要多个输出目标或结构化查询时上 Serilog                              |
| 依赖注入   | 不用                                          | 服务多到互相依赖、构造顺序开始绕时再上                                |
| Win32 调用 | 少量调用可手写 DllImport | 结构体与签名维护复杂时考虑 Microsoft.Windows.CsWin32。 |
| 测试 | 新项目可用 xunit.v3 和内置 Assert | 已有 runner 沿用；增加断言库前核对许可与实际价值。 |
| 多语言 | resx 与绑定包装 | 沿用已验证的资源方案；LocBaml 是[示例工具](https://learn.microsoft.com/dotnet/desktop/wpf/advanced/how-to-localize-an-application)，采用前核对生产适用性。 |
| 发布 | pubxml 按 x64/ARM64、自包含/框架依赖分开 | 按分发矩阵和实际原生依赖验证，各 profile 独立输出。 |
| 自动更新 | 已有联网更新需求时，查 `releases/latest` 后提示并打开 Release 页；离线应用保留手动更新 | 需要下载安装替换时评估 Velopack；选包、缓存及交付验收见 [更新集成](github-actions.md#应用内更新)。 |
| 代码签名 | 有资格时使用 [Azure Artifact Signing](https://azure.microsoft.com/products/artifact-signing) | 资格、配置与未签名交付方式见 [签名](github-actions.md#签名)。 |

按需引入，不为采用本技能替换已有可用组件；已有建议依赖的版本维护统一按[依赖升级](upgrade-dependencies.md#已采用的建议依赖必须升级)执行。

### 开发环境

Visual Studio 安装“.NET 桌面开发”工作负载即可获得 SDK、XAML 设计器和调试工具。已有 Rider 或命令行工作流可以继续使用；VS Code 的 XAML 可视化能力与完整 IDE 不同。

目标 net10.0 的 IDE/MSBuild 支持需按 [SDK 与 MSBuild/VS 对应表](https://learn.microsoft.com/dotnet/core/porting/versioning-sdk-msbuild-vs) 核对；仅安装 SDK 不代表旧 IDE 已支持该目标。

### 托盘图标：看工程里有没有 WinForms

分界线不是菜单长短，是工程有没有已经拖进 WinForms。

纯 WPF 工程使用 [H.NotifyIcon.Wpf](https://www.nuget.org/packages/H.NotifyIcon.Wpf) 时，托盘和菜单可放进 `App.xaml` 资源，在启动时用 `FindResource` 取出并显式创建：

```csharp
_tray = (TaskbarIcon)FindResource("Tray");
if (!_tray.IsCreated)
    _tray.ForceCreate(enablesEfficiencyMode: false);   // 资源里的 TaskbarIcon 不进可视树，永远不 Loaded
// …OnExit 里 _tray?.Dispose()，把 shell 图标交还回去
```

资源字典中的 `TaskbarIcon` 不进入可视树，不能依赖 `Loaded` 自动创建。[官方签名](https://github.com/HavenDV/H.NotifyIcon)为 `ForceCreate(bool enablesEfficiencyMode = true)`；热键响应敏感时可显式关闭效率模式并测量影响。独立验证创建、显示、图标资源、语言切换时的菜单刷新及 `Dispose`；常规窗口 smoke 不一定覆盖托盘路径。

已有 WinForms 的工程也可沿用 `NotifyIcon`，同时处理菜单样式、语言更新和 DPI。不要仅为托盘或剪贴板无条件增加/移除一套 UI 框架。

### MVVM：`CommunityToolkit.Mvvm`，或者干脆 code-behind

WPF 自带的 `INotifyPropertyChanged` 要手写一堆 `OnPropertyChanged(nameof(X))`，`ICommand` 还得自己实现一个类。`CommunityToolkit.Mvvm` 是微软官方维护的 MVVM 工具包，用源生成器减少通知与命令样板；仍需验证项目实际绑定与发布行为：

```csharp
public partial class MainViewModel : ObservableObject
{
    [ObservableProperty]
    private string _keyword = "";

    [RelayCommand]
    private async Task SearchAsync() { /* ... */ }
}
```

`_keyword` 生成公开的 `Keyword`，`SearchAsync` 生成 `SearchCommand`，XAML 直接绑这两个名字。窗口少、状态简单的小工具直接 code-behind 加事件处理也完全成立——别为了模式而模式，等绑定和通知的手写量超过引包的成本再换。

同一套 `Microsoft.Extensions.*` 里的依赖注入可以先不上。小工具三五个服务，窗口互相 `new`、配置做成静态单例完全撑得住。等到出现「设置被五个窗口读、其中两个还要在设置改了之后刷新」这种关系再引。

### 界面主题与控件库

先检查项目已有主题。新项目可试 WPF 自带 Fluent 的 `ThemeMode`，再用 `Theme.xaml` 补语义画刷与未覆盖样式；需要运行时切换的资源使用 `DynamicResource`，`StaticResource` 不会随资源字典替换重新求值。[WPF 资源](https://learn.microsoft.com/dotnet/desktop/wpf/systems/xaml-resources-overview)

按实际控件、导航、可访问性与维护成本选择控件库，不把“零依赖”当目标。已有库不为风格重写，避免在同一应用保留两套互不协调的主题控制。代码编辑器可考虑 AvalonEdit；自定义 `.xshd` 作为 EmbeddedResource 发布，并在安装版验证加载。

### 按边界组织工程与测试

```
src/Xxx.App/          net10.0-windows, UseWPF   只放窗口和交互
src/Xxx.Core/         net10.0                   业务逻辑
tests/Xxx.Core.Tests/ net10.0, OutputType=Exe   xunit.v3
```

`src/` 和 `tests/` 这两层不是洁癖，`github-actions.md` 里的每一条路径都按这个约定写；换成扁平布局记得同步改 CI。

下面是 App 工程的起点；保留项目所需的其他属性，发布专用配置放入 profile：

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>WinExe</OutputType>
    <TargetFramework>net10.0-windows</TargetFramework>
    <UseWPF>true</UseWPF>
    <Nullable>enable</Nullable>
    <AssemblyName>Xxx</AssemblyName>
    <ApplicationManifest>app.manifest</ApplicationManifest>
    <VersionFallback>0.0.1</VersionFallback>
    <Version>$(VersionFallback)</Version>
  </PropertyGroup>
</Project>
```

配置要点：

- `AssemblyName` 决定产物叫 `Xxx.exe` 而不是 `Xxx.App.exe`：默认取工程名，不设这行发版脚本里的文件名全对不上。
- `VersionFallback` 是那个 target 的 Condition 判据，必须定义，否则 target 永不触发；真正的版本从 git tag 取，见 pitfalls.md「版本号发出去还是上一版」。
- 这里故意没有 `RuntimeIdentifier(s)`、`SelfContained`、`PublishSingleFile`（全在 pubxml），锁文件按下文「NuGet 锁文件与单文件发布」选择。

将不依赖 Windows API、WPF 或 Windows 专用包的业务逻辑放在普通 net10.0 库，便于跨平台测试；平台边界按实际 API/包依赖判断，不只看命名空间。UI 行为需要 Windows/WPF 宿主测试，见 [自查工具](dev-switches.md)。

更小的工具可以压成两个工程：Core 做成 app 工程里的一个文件夹，测试工程直接引用 app 工程、配合 `InternalsVisibleTo` 测 internal。代价是测试工程也得跟着 `net10.0-windows` 加 `UseWPF`（好处是测试里能构造真窗口）。

新项目可用适配目标 SDK 的 xUnit v3/MTP 模板（测试平台 1.7 或更高），已有工程沿用测试框架。断言库按许可和需求选择，默认使用框架内置 Assert。运行命令及用例数判定统一见[测试运行与结果判定](dev-switches.md#测试运行与结果判定)。

### SDK 固定：global.json 一处说了算

在选定 SDK 下运行 `dotnet new wpf -n MyApp -f net10.0`，按需用 `dotnet add MyApp/MyApp.csproj package <包名> --version <稳定版本>` 添加依赖。下例的 test 段仅适用于选择 MTP 的项目。[Microsoft 测试运行模式](https://learn.microsoft.com/dotnet/core/testing/unit-testing-with-dotnet-test)

```json
{
  "sdk": {
    "version": "10.0.404",
    "rollForward": "latestFeature",
    "allowPrerelease": false
  },
  "test": { "runner": "Microsoft.Testing.Platform" }
}
```

- `sdk.version` 写完整版本，将 `10.0.404` 替换为本次选定值；迁移范围与核验步骤见[依赖升级](upgrade-dependencies.md#对齐技能指定的大版本)。
- `latestFeature` 在已安装 SDK 中允许选择较新的 10.0 feature band；`disable` 要求精确版本。提高下限可能使贡献者旧 SDK 无法构建，应覆盖项目所需能力，不静默放弃能力要求。
- CI 的 `setup-dotnet` 可通过 `global-json-file` 安装 `sdk.version`，但不要假设 Action 会替应用执行 `rollForward`。实际 SDK 取决于 Action 与 runner 预装环境；保留较低开发下限时，在 CI 单独安装期望 SDK，并核验实际选择和自包含产物运行时补丁。

#### MTP 测试模式

使用 MTP 的 `dotnet test` 模式时保留 `"test": {"runner":"Microsoft.Testing.Platform"}`；缺少它可能切回 VSTest，使 MTP 专用参数失败。怀疑 SDK 能力或配置未生效时，在隔离目录用指定 SDK 运行目标命令，并比较开启/关闭该配置的行为，避免只凭源码位置或成功退出码推断。

同一配置作用域内参与本次 `dotnet test` 的项目须支持所选模式。混合 MTP／VSTest 方案沿各自兼容入口运行，勿为套用示例直接覆盖全仓库的 `test.runner`。[模式兼容性](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-with-dotnet-test#mtp-mode-of-dotnet-test)

### NuGet 锁文件与单文件发布

单文件发布会启用 `EnableSingleFileAnalyzer`，可能隐式引用 `Microsoft.NET.ILLink.Tasks`；普通 restore 生成的锁文件不一定覆盖 publish 所需依赖。遇到 `NU1004` 时，比较还原与发布的 SDK、RID、profile 和 `EnableSingleFileAnalyzer`，检查锁文件中的隐式依赖，而非直接删除锁文件。

已有锁文件沿用原策略。SDK 补丁变化导致隐式包不匹配时，可固定完整 SDK，或按可复现性要求调整策略；刷新与 locked restore 步骤见[依赖升级](upgrade-dependencies.md#更新-nuget-包)，覆盖各 publish profile。[SDK 隐式依赖与锁文件讨论](https://github.com/dotnet/sdk/issues/48795)

### 发布：四份 pubxml（x64 / arm64 × 自包含 / 框架依赖），csproj 一个发布属性都不放

放 `src/Xxx.App/Properties/PublishProfiles/` 下，文件名就是 `-p:PublishProfile=` 要用的名字。为什么不能放 csproj，见 `pitfalls.md`「测试工程引用 App 就报 NETSDK1151」。

`win-x64.pubxml`（自包含，下载即用）：

```xml
<Project>
  <PropertyGroup>
    <Configuration>Release</Configuration>
    <TargetFramework>net10.0-windows</TargetFramework>
    <RuntimeIdentifier>win-x64</RuntimeIdentifier>
    <SelfContained>true</SelfContained>
    <PublishSingleFile>true</PublishSingleFile>
    <IncludeNativeLibrariesForSelfExtract>true</IncludeNativeLibrariesForSelfExtract>
    <EnableCompressionInSingleFile>true</EnableCompressionInSingleFile>
    <DebugType>none</DebugType>
    <PublishDir>bin\Release\publish-x64\</PublishDir>
  </PropertyGroup>
</Project>
```

`win-x64-needs-dotnet10.pubxml`（框架依赖，体积小得多）：只把 `SelfContained` 改成 `false`、`PublishDir` 改成 `bin\Release\publish-x64-needs-dotnet10\`，并删除 `EnableCompressionInSingleFile`，该压缩选项要求自包含。`IncludeNativeLibrariesForSelfExtract` 则按实际原生依赖选择：需要嵌入并提取原生 DLL 时可保留；留作外置文件时删除，并随 ZIP 完整打包。框架依赖不等于没有应用自己的原生 DLL。[单文件原生库](https://learn.microsoft.com/dotnet/core/deploying/single-file/overview#native-libraries)

arm64 两份是上面两份的复制，只改两行：

| 文件 | `RuntimeIdentifier` | `SelfContained` | `PublishDir` |
| --- | --- | --- | --- |
| `win-x64.pubxml` | `win-x64` | `true` | `bin\Release\publish-x64\` |
| `win-x64-needs-dotnet10.pubxml` | `win-x64` | `false` | `bin\Release\publish-x64-needs-dotnet10\` |
| `win-arm64.pubxml` | `win-arm64` | `true` | `bin\Release\publish-arm64\` |
| `win-arm64-needs-dotnet10.pubxml` | `win-arm64` | `false` | `bin\Release\publish-arm64-needs-dotnet10\` |

各 profile 使用独立输出目录，避免互相覆盖；修改名称或 `PublishDir` 时同步[本地与 CI 打包入口](github-actions.md#共用打包入口)。检查手写 P/Invoke 结构体布局、硬编码 x64 路径和原生包的架构支持；构建、解包运行与 ARM64 验收见[产物验证](github-actions.md#产物验证)。


### 发布包组织：三轨分发矩阵（安装包 + 便携 ZIP + 框架依赖精简版）

新建、通用维护和整体采用时，按下表补齐安装包及 x64／ARM64 两种 ZIP；历史包型较少不自动构成例外。用户当前明确限制或可验证的架构兼容问题决定实际例外，并记录原因。同一 exe 已在 ZIP 中时，不重复提供独立下载项。

| 渠道 | 产物命名 | 内核形态 | 适用受众与优势 |
| :--- | :--- | :--- | :--- |
| 安装包 | `Xxx-<tag>-setup.exe` | Inno Setup 6 封装自包含 x64 应用 | 快捷方式、标准卸载与静默部署；不需预装 .NET。 |
| 自包含便携包 | `Xxx-<tag>-win-{x64,arm64}.zip` | 自包含单文件及所需外置文件 | 解压运行，不需预装 .NET。 |
| 框架依赖精简包 | `Xxx-<tag>-win-{x64,arm64}-needs-dotnet10.zip` | 框架依赖单文件及所需外置文件 | 下载说明注明需预装 .NET 10 Desktop Runtime。 |

#### Inno Setup 6 最佳实践配置要点

写 `.iss` 脚本时有以下配置要点：

1. **按权限需求选择安装范围**：普通按用户安装可免提权：
   ```ini
   PrivilegesRequired=lowest
   DefaultDirName={localappdata}\Programs\{#MyAppName}
   ```
   默认按用户安装到 `AppData\Local\Programs`。明确需要管理员登录自启或机器级部署时，可改用提权安装到受保护目录：
   ```ini
   [Setup]
   PrivilegesRequired=admin
   DefaultDirName={autopf}\{#MyAppName}
   ```
   两段配置按部署模式选择，不能直接叠加。`admin` 控制安装器权限，应用自启权限仍需单独配置。便携包可从原位置配置管理员自启；路径策略、受保护部署与更新统一见 [自启部署与排查](startup.md#选择权限与部署方式)。[Inno Setup 安装权限](https://jrsoftware.org/ishelp/topic_setup_privilegesrequired.htm)
2. **显式声明卸载显示名称（避免安装后应用名称附带版本号）**：
   ```ini
   [Setup]
   UninstallDisplayName={#MyAppName}
   ```
   省略时默认名称含 `version {#MyAppVersion}`；显式设置以保持系统应用列表中的产品名称简洁。
3. **支持 winget 静默安装与企业部署**：
   脚本必须兼容 Inno Setup 标准开关 `/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-`，供 winget、Chocolatey、Scoop 或企业批量脚本自动化推送。
4. **卸载时干扫尾**：
   仅清理安装器管理的文件、确认可丢弃的缓存和本应用注册的 Shell 关联。用户文件与配置按产品约定保留；旧版升级再卸载也需验证，见 [卸载日志](github-actions.md#修了卸载规则旧版升级后仍会删除用户文件)。
5. **安装包图标绑定与旧指令规避**：
   `UninstallIconFile` 自 Inno Setup 5.0.0 起已废弃。安装器用 `SetupIconFile=app.ico`，系统卸载列表用 `UninstallDisplayIcon={app}\Xxx.exe`，快捷方式在 `[Icons]` 中指定图标；这三种用途分别配置。[旧指令](https://jrsoftware.org/ishelp/topic_setup_uninstalliconfile.htm)、[卸载列表图标](https://jrsoftware.org/ishelp/topic_setup_uninstalldisplayicon.htm)
6. **安装与卸载界面统一英文**：
   在现有 `.iss` 对应节中合并以下配置，`[Languages]` 仅保留英文：
   ```ini
   [Setup]
   ShowLanguageDialog=no

   [Languages]
   Name: "english"; MessagesFile: "compiler:Default.isl"
   ```
   自定义页面、任务选项、按钮、`[Messages]` / `[CustomMessages]` 和代码弹窗也使用英文，不随系统或应用语言切换。生成安装包后，在中文 Windows 上检查安装及卸载向导均为英文。[Inno Setup 语言配置](https://jrsoftware.org/ishelp/topic_languagessection.htm)

CI 记录实际 ISCC.exe 路径和编译横幅，版本目标与升级要求见[依赖升级](upgrade-dependencies.md#对齐技能指定的大版本)。[Inno Setup 编译器参数](https://jrsoftware.org/ishelp/topic_compilercmdline.htm)

### 应用原生图标

在 App 的 csproj 设置 `<ApplicationIcon>Resources\app.ico</ApplicationIcon>`；XAML 的窗口 Icon 不会替代 EXE 的 PE 图标。编译后检查发布 exe、安装快捷方式及 Shell 条目的实际图标来源。故障机制见 [白纸图标](pitfalls.md#右键菜单和外壳扩展项显示-windows-默认白纸图标)。
