# 项目架构、启动与打包

> wpf-developer 技能参考文件。分层结构、Generic Host 启动模板、DI/配置/日志、XAML 资源组织、打包发布。

## 目录

1. [推荐项目结构](#1-推荐项目结构)
2. [Generic Host 启动模板](#2-generic-host-启动模板)
3. [配置与日志](#3-配置与日志)
4. [DI 注册约定](#4-di-注册约定)
5. [XAML 资源组织](#5-xaml-资源组织)
6. [.NET Framework 迁移清单](#6-net-framework-迁移清单)
7. [打包与发布](#7-打包与发布)

---

## 1. 推荐项目结构

```text
src/
├── MyApp/                     # WPF 启动项目
│   ├── App.xaml(.cs)          # Host 组装 + 全局资源
│   ├── appsettings.json
│   ├── Views/                 # Window/UserControl（XAML + 最小 code-behind）
│   ├── ViewModels/            # 与 Views 一一对应
│   └── Assets/                # 图片/字体/图标
├── MyApp.Core/                # 实体、接口、基类、枚举（零外部依赖）
├── MyApp.Application/         # 服务、DTO、验证、业务编排
├── MyApp.Infrastructure/      # EF Core/Dapper、文件、外部 API、序列化
└── MyApp.Contracts/           # （可选）跨进程/WCF/gRPC 契约
tests/
├── MyApp.Tests/               # 单元测试（VM/服务可测）
└── MyApp.UITests/             # FlaUI 自动化（按需）
```

- 大型项目按功能拆 Module（Prism 场景），每个 Module 自带 Views/ViewModels，Shell 只做组装。
- Views ↔ ViewModels 严格同名同目录；禁止 View 引用 ViewModel 具体类型（经 DataContext + 绑定，或构造注入）。

## 2. Generic Host 启动模板

**App.xaml.cs**

```csharp
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Serilog;

public partial class App : Application
{
    private IHost _host = null!;

    protected override void OnStartup(StartupEventArgs e)
    {
        base.OnStartup(e);

        _host = Host.CreateApplicationBuilder()
            .ConfigureAppConfiguration((ctx, cfg) =>
            {
                cfg.AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
                   .AddJsonFile($"appsettings.{ctx.Hosting.EnvironmentName}.json",
                                optional: true, reloadOnChange: true);
            })
            .ConfigureServices((ctx, services) =>
            {
                // 配置绑定（Options 模式）
                services.Configure<AppOptions>(ctx.Configuration.GetSection("App"));

                // 基础设施
                services.AddSingleton<IOrderService, OrderService>();
                services.AddDbContext<AppDbContext>(o =>
                    o.UseSqlServer(ctx.Configuration.GetConnectionString("Default")));

                // 窗口与 VM
                services.AddSingleton<MainWindow>();
                services.AddTransient<MainViewModel>();
            })
            .UseSerilog((ctx, cfg) => cfg
                .ReadFrom.Configuration(ctx.Configuration)
                .WriteTo.Console()
                .WriteTo.File("logs/log-.log", rollingInterval: RollingInterval.Day))
            .Build();

        // 启动前置校验：配置、数据库连通性、许可证
        _host.Services.GetRequiredService<MainWindow>().Show();
    }

    protected override void OnExit(ExitEventArgs e)
    {
        _host.Dispose();   // 触发 IHostedService/IHostApplicationLifetime 清理
        base.OnExit(e);
    }
}
```

注意：
- 启动路径只做组装和首窗显示；**数据库迁移、预热、检查放后台任务**（`Task.Run` + 启动画面），避免阻塞 UI 线程导致「白屏假死」。
- 单实例需求：命名 Mutex 或 `SingleInstance` 社区包，二次启动时唤起已有窗口。

## 3. 配置与日志

**appsettings.json**

```json
{
  "App": { "Theme": "Light", "AutoUpdate": true },
  "ConnectionStrings": { "Default": "Server=.;Database=MyApp;Trusted_Connection=True;" },
  "Serilog": {
    "MinimumLevel": "Information",
    "WriteTo": [{ "Name": "Console" }]
  }
}
```

- 读取：`IOptions<AppOptions>` / `IOptionsSnapshot<T>`（支持热更新）/ `IOptionsMonitor<T>`；禁止到处 `Configuration["x:y"]` 裸取。
- 环境区分：`DOTNET_ENVIRONMENT=Development|Production`，配 `appsettings.{Environment}.json`。
- 日志：统一 Serilog 输出模板，异常带上下文（`Log.ForContext<MainViewModel>()`）；发布版本可接 Seq/ELK。

## 4. DI 注册约定

| 类型 | 生命周期 |
|---|---|
| Window / App / 导航宿主 | Singleton |
| ViewModel | Transient |
| 无状态服务（查询/API 客户端） | Singleton |
| 有状态服务（DbContext/工作单元） | Scoped（WPF 无请求作用域，用「窗口作用域」或每次操作 `CreateScope`） |
| 缓存/配置 | Singleton |

> WPF 没有 Web 的请求作用域，DbContext 类 Scoped 服务需自行管理作用域（如每个业务操作 `using var scope = _host.Services.CreateScope()`），否则单例窗口捕获 Scoped 服务会 captive dependency。

## 5. XAML 资源组织

```text
MyApp/
├── App.xaml                       # 只合并入口字典
└── Themes/
    ├── Entry.xaml                 # 入口：合并下面所有
    ├── Libraries/                 # 每个第三方库一个文件
    │   ├── MaterialDesign.xaml    # MDIT 的 BundledTheme + Defaults
    │   └── HandyControl.xaml
    ├── Base/                      # 基础样式（字号/间距/颜色常量）
    ├── Controls/                  # 自定义控件样式与模板
    └── Converters.xaml            # 全局转换器
```

- 合并顺序：**先库后自定义**（自定义 BasedOn 库样式才能生效）。
- 隐式样式只放全局通用键；控件私有样式放控件 `Resources`，防止全局污染。
- 换肤方案：深浅主题 = 两套 Brush 资源字典运行时替换（每个库的字典要整体换，不能只改几个 Brush）。
- XAML 文件保存为 **UTF-8 with BOM**，避免中文资源在部分工具链下乱码。

## 6. .NET Framework 迁移清单

老项目（.NET Framework 4.x）升级 .NET 8/10 的固定动作：

1. `try-convert` 工具转 SDK 风格项目，失败则手工重写 csproj（`<Project Sdk="Microsoft.NET.Sdk">` + `UseWPF`）。
2. 依赖替换：
   - `System.Configuration.ConfigurationManager` → `Microsoft.Extensions.Configuration` + `IOptions<T>`；
   - `System.Windows.Interactivity` → `Microsoft.Xaml.Behaviors.Wpf`；
   - `App.config` → `appsettings.json`；
   - `EntityFramework` → `EF Core`（注意 API 差异）。
3. 程序集信息从 `AssemblyInfo.cs` 移入 csproj。
4. 检查 GAC 依赖、COM 互操作、CAS 假设（.NET Core 起无 CAS）。
5. `pack://application:,,,/` 资源 URI 语法不变，但**区分大小写**，注意大小写修正。
6. 升级后跑全量视觉回归（第三方库资源字典对 TFM 敏感）。

## 7. 打包与发布

| 方式 | 命令/工具 | 适用 |
|---|---|---|
| 框架依赖 | `dotnet publish -c Release` | 目标机已装 .NET 运行时，体积最小 |
| 独立部署 | `dotnet publish -c Release -r win-x64 --self-contained true` | 目标机免装运行时 |
| 单文件 | 加 `-p:PublishSingleFile=true` | 分发一个 exe（WPF 对 trimming 支持有限，慎开裁剪） |
| MSIX | VS「发布 → MSIX」或 `msix-packaging` | 自动更新、干净卸载、Win11 首选 |
| ClickOnce | VS 发布向导 | 每用户免管安装，.NET 起需 bootstrapper 或迁 MSIX |

发布检查项：版本号策略（`<Version>`/`<AssemblyVersion>`）、PDB 与符号、日志目录可写、自动更新通道（MSIX 或自研 + `--url` 参数）、安装目录权限（Program Files 只读，用户数据写 `%APPDATA%`）。
