# WPF 性能优化与故障排查

> wpf-developer 技能参考文件。性能清单、内存泄漏排查、绑定调试、常见故障 FAQ、迁移坑。

## 目录

1. [性能优化清单](#1-性能优化清单)
2. [内存泄漏排查](#2-内存泄漏排查)
3. [绑定调试](#3-绑定调试)
4. [常见故障 FAQ](#4-常见故障-faq)
5. [工具](#5-工具)

---

## 1. 性能优化清单

按出现频率排序，改代码前先过一遍：

### 1.1 列表虚拟化（头号卡顿源）

```xml
<!-- ItemsControl 默认模板是 StackPanel（不虚拟！大数据量必须显式开虚拟化） -->
<ListBox ItemsSource="{Binding Items}"
         ScrollViewer.IsDeferredScrollingEnabled="True"
         VirtualizingStackPanel.IsVirtualizing="True"
         VirtualizingStackPanel.VirtualizationMode="Recycling" />
```

- `VirtualizationMode=Recycling`：复用容器，避免为每项新建 UI 元素；
- 自设 `ItemsPanel` 时换成 `VirtualizingStackPanel`；
- 万级以上：分页 / 增量加载（滚动到底部加载下一页），虚拟化只是兜底；
- 列表项模板本身要轻：避免嵌套深层面板、避免项内 `Effect`（DropShadow 逐项绘制极贵）。

### 1.2 集合更新方式

- `ObservableCollection` 逐条 `Add` = N 次 UI 刷新。批量场景先 `List<T>` 组装，再一次 `Clear()+Add()` 或整体替换 ItemsSource；
- 集合属性用 `[ObservableProperty]` 整体替换，UI 只刷新一次。

### 1.3 绑定

- .NET 9+ WPF 支持 **XAML 编译绑定（`x:Bind` 源生成器）**：编译期生成、无反射，大数据量界面优先用；.NET 10 进一步完善；
- 避免超长 `Path`（`A.B.C.D`）与深层 `RelativeSource FindAncestor`；
- 高频更新（进度条、实时曲线）用 `Binding.IsAsync` 或直接写 DependencyProperty/事件驱动，别走完整通知链。

### 1.4 线程与启动

- IO/计算全部 `await Task.Run(...)`；VM 内 `ConfigureAwait(false)`（库代码）防死锁；
- 启动路径轻量：App 构造、首窗构造、EF 迁移、预热全放后台，UI 先出；
- 资源字典合并顺序固定，避免重复解析大字典。

### 1.5 渲染

- 慎用 `AllowsTransparency="True"`（软件渲染、无硬件加速，且兼容性差）；
- 静态内容用 `BitmapCache`；`Freezable`（Brush/Geometry）能冻结就冻结（跨线程 + 省内存）；
- 动画优先 `DoubleAnimation` 组合 Transform，避免逐帧改布局属性（Width/Height 触发布局传递）。

## 2. 内存泄漏排查

高频根因（按命中率）：

1. **事件未解绑**：`+=` 后对象生命周期长于订阅者 → 用 `WeakEventManager` 或 behaviors；
2. **静态引用/静态事件**：静态集合、`Messenger` 未 `Unregister`（CommunityToolkit 的 `WeakReferenceMessenger` 默认弱引用，风险较低；Prism EventAggregator 用 `Unsubscribe`）；
3. **BitmapImage 锁文件**：不 `CacheOption=OnLoad` 会持有文件流 → 设置 `BitmapCacheOption.OnLoad`；
4. **DispatcherTimer / 动画不停**：窗口关闭后仍 tick → `Closing` 里 `Stop()`；
5. **DataTemplate/控件缓存**：模板里的父级引用未释放；
6. **定时快照对比**：VS 诊断工具 / dotMemory 隔 30s 拍快照，看哪些类型实例数只增不减。

## 3. 绑定调试

- Output 窗口（Debug）看绑定错误：`BindingExpression path error` 会打出属性名与源对象；
- 加重症trace：`xmlns:diag="clr-namespace:System.Diagnostics;assembly=WindowsBase"` + `diag:PresentationTraceSources.TraceLevel=High`；
- **Snoop / WPF Inspector**：运行时附魔，看可视树、DataContext、实际生效样式——排查「样式没生效」「DataContext 不是我以为的那个」神器；
- 设计器数据：`d:DataContext="{d:DesignInstance Type=vm:Xxx, IsDesignTimeCreatable=True}"`，VM 构造器里 `DesignerProperties.GetIsInDesignMode` 分支返回假数据。

## 4. 常见故障 FAQ

| 症状 | 排查 |
|---|---|
| 界面整体模糊/发虚 | app.manifest 未声明 per-monitor DPI（`<dpiAware>true/PM</dpiAware>`）；或用了 AllowsTransparency 软件渲染 |
| 库样式「没生效」 | MergedDictionaries 顺序错（自定义在库前）；同名隐式样式被后合并库覆盖；pack URI 大小写 |
| 打包后缺资源 | 资源 Build Action 不是 Page/Resource；URI 大小写（.NET Core 起区分大小写） |
| 主题切换崩溃/不彻底 | 运行时替换 MergedDictionaries 必须整体替换库字典实例；只改个别 Brush 会漏 |
| 弹窗不置顶/跑到主窗后面 | `Owner` 未设置；用 `ShowDialog()` 或设 `Topmost` |
| 中文输入法异常（候选框位置、无法输入） | 检查自定义控件是否吞了 `TextComposition`；自绘 TextBox 需保留 IME 消息链 |
| 点击按钮无反应 | Command 的 CanExecute 恒 false；Button 的 `IsEnabled` 被父级覆盖；`CommandParameter` 传了 null 但 VM 未判空 |
| 异步命令重复触发 | `AsyncRelayCommand` 被禁用并发时按钮应自动禁用；自写 ICommand 忘实现 CanExecute |
| 升级 .NET 后 XAML 报错 | `System.Windows.Interactivity` 命名空间失效 → 换 `Microsoft.Xaml.Behaviors.Wpf`；`clr-namespace` 程序集名变更 |
| 设计器崩溃/卡死 | VM 构造器里有真实 IO；改用 `IsDesignTimeCreatable=False` + `d:DataContext` 静态实例 |
| 多显示器不同 DPI 花屏 | WPF 每窗口 DPI 感知 + 窗口迁移监听 `DpiChanged`（库窗口基类一般已处理） |

## 5. 工具

| 用途 | 工具 |
|---|---|
| CPU/启动/GC 剖析 | PerfView、VS 诊断工具（性能探查器） |
| 内存泄漏 | VS 快照 / dotMemory |
| 运行时可视树/Style | Snoop、WPF Inspector |
| UI 自动化测试 | FlaUI（UIA3） |
| 绑定/资源静态检查 | ReSharper/Rider XAML 分析、`xamllint` 类工具 |

使用顺序：**先工具测量定位，再改代码**；凭感觉优化（换控件库、加缓存）是 WPF 性能调优最常见的浪费。
