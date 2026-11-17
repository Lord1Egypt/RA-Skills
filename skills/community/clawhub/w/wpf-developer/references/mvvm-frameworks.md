# MVVM 框架选型与模板

> wpf-developer 技能参考文件。三种主流 MVVM 方案对比、选择决策与最小可用模板。

## 目录

1. [三框架对比与选择](#1-三框架对比与选择)
2. [CommunityToolkit.Mvvm（默认推荐）](#2-communitytoolkitmvvm默认推荐)
3. [Prism（模块化场景）](#3-prism模块化场景)
4. [ReactiveUI（重响应式场景）](#4-reactiveui重响应式场景)

---

## 1. 三框架对比与选择

| 维度 | CommunityToolkit.Mvvm | Prism.DryIoc | ReactiveUI |
|---|---|---|---|
| 包 | `CommunityToolkit.Mvvm`（8.4.x） | `Prism.Wpf` + `Prism.DryIoc`（稳定 7.2.x） | `ReactiveUI.WPF` |
| 核心理念 | 源生成器消除样板 | 模块化 + 区域 + 导航 + 对话框服务 | 一切皆 Observable |
| 属性通知 | `[ObservableProperty]` 编译期生成 | `BindableBase.SetProperty` 手写 | `RaiseAndSetIfChanged` |
| 命令 | `[RelayCommand]` / `AsyncRelayCommand` | `DelegateCommand` | `ReactiveCommand`（可执行性由 IObservable 驱动） |
| 导航 | 无（自建或配 Prism） | Region + `RequestNavigate`，能力最全 | 自建 |
| 对话框 | 无（用 DialogHost/IDialogService） | `IDialogService` 内置 | 自建（Interaction<T>） |
| 模块化 | 无 | `IModule` 按需加载 | 无 |
| 消息 | `WeakReferenceMessenger` 内置 | `EventAggregator` | `MessageBus` |
| 验证 | `ObservableValidator` | 无内置 | 无内置 |
| 学习曲线 | 低 | 中高 | 高（需 Rx 基础） |
| 适合 | 中小项目、绝大多数新项目 | 大项目、插件化/模块化、多团队 | 数据流复杂、强响应式 UI |

**选择决策**：
- 默认选 **CommunityToolkit.Mvvm** + Microsoft.Extensions.DependencyInjection，除非：
- 需要**模块化加载 / Region 导航 / 内置对话框服务** → **Prism**；
- 界面状态是复杂事件流驱动（搜索联想、实时数据、防抖节流组合）→ **ReactiveUI**；
- MvvmLight 已归档、Caliburn.Micro 社区冷清，**新项目不再选用**。

---

## 2. CommunityToolkit.Mvvm（默认推荐）

### 2.1 安装与铁律

```powershell
dotnet add package CommunityToolkit.Mvvm
```

- 使用 `[ObservableProperty]` / `[RelayCommand]` 的类**必须声明 `partial`**，否则生成器报错（MVVMTK0008/MVVMTK0042）。
- 8.4+ 推荐 **partial property 模式**（`public partial string Name { get; set; }`），字段模式（`private string _name;`）仍兼容；VS 提供一键迁移菜单。
- 命名空间：
  - `CommunityToolkit.Mvvm.ComponentModel` → `ObservableObject`、`[ObservableProperty]`
  - `CommunityToolkit.Mvvm.Input` → `[RelayCommand]`、`AsyncRelayCommand`
  - `CommunityToolkit.Mvvm.Messaging` → `WeakReferenceMessenger`、`IRecipient`
  - `CommunityToolkit.Mvvm.DependencyInjection` → `Ioc`（仅玩具/小项目用；正式项目直接用 MS DI）

### 2.2 最小完整模板

**App.xaml.cs（Generic Host 启动）**

```csharp
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

public partial class App : Application
{
    private IHost _host = null!;

    protected override void OnStartup(StartupEventArgs e)
    {
        base.OnStartup(e);

        _host = Host.CreateApplicationBuilder()
            .ConfigureServices((context, services) =>
            {
                // 服务层
                services.AddSingleton<IOrderService, OrderService>();

                // ViewModel
                services.AddTransient<MainViewModel>();

                // 窗口（单例）
                services.AddSingleton<MainWindow>();
            })
            .Build();

        _host.Services.GetRequiredService<MainWindow>().Show();
    }

    protected override void OnExit(ExitEventArgs e)
    {
        _host.Dispose();
        base.OnExit(e);
    }
}
```

**MainWindow.xaml**

```xml
<Window x:Class="MyApp.Views.MainWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
        xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
        mc:Ignorable="d"
        Title="MainWindow" Height="450" Width="800"
        d:DataContext="{d:DesignInstance Type=vm:MainViewModel, IsDesignTimeCreatable=True}">
    <StackPanel Margin="16">
        <TextBox Text="{Binding Keyword, UpdateSourceTrigger=PropertyChanged}" />
        <Button Content="查询" Command="{Binding SearchCommand}" />
        <TextBlock Text="{Binding ResultText}" />
    </StackPanel>
</Window>
```

**MainWindow.xaml.cs（唯一职责：注入 DataContext）**

```csharp
public partial class MainWindow : Window
{
    public MainWindow(MainViewModel vm)
    {
        InitializeComponent();
        DataContext = vm;
    }
}
```

**MainViewModel.cs**

```csharp
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

public partial class MainViewModel : ObservableObject
{
    private readonly IOrderService _orderService;

    public MainViewModel(IOrderService orderService)
    {
        _orderService = orderService;
    }

    // 8.4+ partial property 模式
    [ObservableProperty]
    private string _keyword = string.Empty;

    [ObservableProperty]
    [NotifyPropertyChangedFor(nameof(Summary))]
    private int _count;

    public string Summary => $"共 {Count} 条";

    [RelayCommand]
    private async Task SearchAsync(CancellationToken token)
    {
        var list = await _orderService.QueryAsync(Keyword, token);
        Count = list.Count;
    }

    // CanExecute + 依赖属性变化自动刷新
    [RelayCommand(CanExecute = nameof(CanSave))]
    private void Save() { /* ... */ }

    private bool CanSave() => Count > 0;

    [ObservableProperty]
    [NotifyCanExecuteChangedFor(nameof(SaveCommand))]
    private bool _isDirty;
}
```

### 2.3 常用能力速查

| 需求 | 写法 |
|---|---|
| 属性联动通知 | `[NotifyPropertyChangedFor(nameof(Summary))]` |
| 命令可用性联动 | `[NotifyCanExecuteChangedFor(nameof(SaveCommand))]` |
| 异步命令带取消 | `private async Task XxxAsync(CancellationToken token)` + `[RelayCommand(IncludeCancelCommand = true)]` |
| 异步命令防重入 | `AsyncRelayCommand` 默认禁止并发；`[RelayCommand(AllowConcurrentExecutions = true)]` 放开 |
| 窗口/页面间通信 | `WeakReferenceMessenger.Default.Send(new TMessage())` + 接收方 `IRecipient<TMessage>` + `WeakReferenceMessenger.Default.Register<TMessage>(this)` |
| 表单验证 | 继承 `ObservableValidator`，属性加 `[ObservableProperty]` + `[NotifyDataErrorInfo]`，方法内 `ValidateProperty(value, ...)` |

---

## 3. Prism（模块化场景）

### 3.1 安装

```powershell
dotnet add package Prism.Wpf
dotnet add package Prism.DryIoc   # 容器按需：Prism.Unity 亦可
```

> Prism 7.x 起按「平台 × 容器」拆包；NuGet 稳定版为 7.2.x，8.x 为先行版，采用前评估。

### 3.2 启动（PrismApplication 替代旧 Bootstrapper）

```csharp
public partial class App : PrismApplication
{
    protected override Window CreateShell() => Container.Resolve<MainWindow>();

    protected override void RegisterTypes(IContainerRegistry containerRegistry)
    {
        containerRegistry.RegisterSingleton<IOrderService, OrderService>();
        containerRegistry.RegisterForNavigation<OrderView, OrderViewModel>();
    }

    protected override void ConfigureModuleCatalog(IModuleCatalog moduleCatalog)
    {
        moduleCatalog.AddModule<OrderModule>();
    }
}
```

### 3.3 模块与导航模板

```csharp
// IModule：模块注册视图与区域
public class OrderModule : IModule
{
    public void OnInitialized(IContainerProvider containerProvider)
    {
        var regionManager = containerProvider.Resolve<IRegionManager>();
        regionManager.RegisterViewWithRegion("MainRegion", typeof(OrderView));
    }

    public void RegisterTypes(IContainerRegistry containerRegistry)
    {
        containerRegistry.RegisterForNavigation<OrderView, OrderViewModel>();
    }
}

// 导航（VM 中注入 IRegionManager）
_regionManager.RequestNavigate("MainRegion", "OrderView");

// 对话框服务
_dialogService.ShowDialog("ConfirmDialog", new DialogParameters("msg=确定删除？"), _ =>
{
    // 回调
});
```

```xml
<!-- Shell 窗口放区域 -->
<Window xmlns:prism="http://prismlibrary.com/"
        ...>
    <DockPanel>
        <ContentControl prism:RegionManager.RegionName="MainRegion" DockPanel.Dock="Right" />
    </DockPanel>
</Window>
```

### 3.4 ViewModel 基类模式

```csharp
public class OrderViewModel : BindableBase, INavigationAware
{
    private string _title = "订单";
    public string Title
    {
        get => _title;
        set => SetProperty(ref _title, value);
    }

    public DelegateCommand SaveCommand => new(() => { /* ... */ });

    public void OnNavigatedTo(NavigationContext context) { /* 入参：context.Parameters["id"] */ }
    public bool IsNavigationTarget(NavigationContext context) => true;
    public void OnNavigatedFrom(NavigationContext context) { }
}
```

---

## 4. ReactiveUI（重响应式场景）

```powershell
dotnet add package ReactiveUI.WPF
```

```csharp
public class SearchViewModel : ReactiveObject
{
    private readonly IOrderService _svc;

    public SearchViewModel(IOrderService svc)
    {
        _svc = svc;

        // 输入流：关键字变化 → 节流 300ms → 去重 → 触发查询
        this.WhenAnyValue(x => x.Keyword)
            .Throttle(TimeSpan.FromMilliseconds(300))
            .DistinctUntilChanged()
            .ObserveOn(RxApp.MainThreadScheduler)
            .InvokeCommand(SearchCommand);
    }

    [Reactive] public string Keyword { get; set; } = string.Empty;

    public ReactiveCommand<Unit, List<OrderDto>> SearchCommand { get; }

    // 命令可执行性本身也是流
    // var canSave = this.WhenAnyValue(x => x.IsDirty);
}
```

适用信号：实时数据推送、复杂联动筛选、防抖搜索、多源合并 UI 状态。普通 CRUD 管理界面使用它属于过度设计。
