# WPF XAML 常用配方

> wpf-developer 技能参考文件。对话框、Snackbar、导航、验证、托盘、DataGrid 等高频场景的落地写法。

## 目录

1. [对话框（MaterialDesign DialogHost）](#1-对话框materialdesign-dialoghost)
2. [消息提示（Snackbar）](#2-消息提示snackbar)
3. [WPF-UI 导航与 ContentDialog](#3-wpf-ui-导航与-contentdialog)
4. [数据模板与选择器](#4-数据模板与选择器)
5. [输入验证](#5-输入验证)
6. [DataGrid 与大数据列表](#6-datagrid-与大数据列表)
7. [托盘图标](#7-托盘图标)
8. [窗口标题栏与现代化效果](#8-窗口标题栏与现代化效果)
9. [本地化与文案管理](#9-本地化与文案管理)
10. [快捷键与输入绑定](#10-快捷键与输入绑定)

---

## 1. 对话框（MaterialDesign DialogHost）

App 级放置 `DialogHost`（通常包住整个窗口内容），用 `DialogHost.OpenDialogCommand` / `CloseDialogCommand` 配合 `DialogSession`：

```xml
<materialDesign:DialogHost Identifier="RootDialog" CloseOnClickAway="True">
    <!-- 主内容 -->
    <Grid>
        <Button Content="删除" Command="{Binding DeleteCommand}" />
    </Grid>
</materialDesign:DialogHost>
```

```csharp
// ViewModel 中（注入 IDialogHost 抽象或直接用 MVVM 方式）
// 社区常用做法：DialogHostHelper 单例封装 Show/Close
await DialogHost.Show(new ConfirmView { DataContext = new ConfirmViewModel("确定删除？") }, "RootDialog");
```

ViewModel 侧不直接引用 DialogHost 的通用做法：定义 `IDialogService.ShowConfirm(msg, Action<bool> callback)`，实现类在 View 层注入 DialogHost，保持 VM 可测试。

## 2. 消息提示（Snackbar）

```xml
<materialDesign:Snackbar x:Name="MainSnackbar" MessageQueue="{materialDesign:MessageQueue}" />
```

```csharp
// VM 侧：经 SnackbarService 抽象，或 View code-behind 转发 VM 的消息事件
MainSnackbar.MessageQueue?.Enqueue("保存成功");
```

## 3. WPF-UI 导航与 ContentDialog

```csharp
// App 启动注册（WPF-UI.DependencyInjection）
services.AddSingleton<INavigationService, NavigationService>();
services.AddSingleton<IWindow, MainWindow>();   // WPF-UI 4 的窗口抽象

// 导航到页
_navigationService.NavigateWithHierarchy(typeof(Views.OrderPage));

// 页面 VM 实现 INavigationAware 接收参数
public void OnNavigatedTo(NavigationContext context) =>
    Id = context.GetParameter<long>("id");
```

```xml
<!-- 模态对话框 -->
<ui:ContentDialog x:Name="ConfirmDialog" Title="确认"
                  PrimaryButtonText="确定" CloseButtonText="取消">
    <TextBlock Text="确定删除这条记录吗？" />
</ui:ContentDialog>
```

```csharp
await ConfirmDialog.ShowAsync();
```

## 4. 数据模板与选择器

```csharp
public class TypeTemplateSelector : DataTemplateSelector
{
    public DataTemplate TextTemplate { get; set; } = null!;
    public DataTemplate ImageTemplate { get; set; } = null!;

    public override DataTemplate SelectTemplate(object item, DependencyObject container)
        => item is ImageItem ? ImageTemplate : TextTemplate;
}
```

```xml
<ListBox ItemsSource="{Binding Items}">
    <ListBox.Resources>
        <local:TypeTemplateSelector x:Key="Sel">
            <local:TypeTemplateSelector.TextTemplate>
                <DataTemplate><TextBlock Text="{Binding Name}" /></DataTemplate>
            </local:TypeTemplateSelector.TextTemplate>
            <local:TypeTemplateSelector.ImageTemplate>
                <DataTemplate><Image Source="{Binding Path}" Height="48" /></DataTemplate>
            </local:TypeTemplateSelector.ImageTemplate>
        </local:TypeTemplateSelector>
    </ListBox.Resources>
    <ListBox.ItemTemplateSelector>{StaticResource Sel}</ListBox.ItemTemplateSelector>
</ListBox>
```

## 5. 输入验证

**VM 级（推荐，可测试）**：CommunityToolkit 的 `ObservableValidator`

```csharp
public partial class EditViewModel : ObservableValidator
{
    [ObservableProperty]
    [NotifyDataErrorInfo]
    [Required(ErrorMessage = "名称不能为空")]
    [MinLength(2, ErrorMessage = "至少 2 个字符")]
    private string _name = string.Empty;
}
```

```xml
<TextBox Text="{Binding Name, UpdateSourceTrigger=PropertyChanged, ValidatesOnDataErrors=True, NotifyOnValidationError=True}" />
```

**XAML 级**：`ValidationRule`（适合与业务无关的格式校验，如手机号正则）。

**自定义错误样式**：覆盖 `Validation.ErrorTemplate`：

```xml
<Style TargetType="TextBox" BasedOn="{StaticResource MaterialDesignOutlinedTextBox}">
    <Setter Property="Validation.ErrorTemplate">
        <Setter.Value>
            <ControlTemplate>
                <DockPanel>
                    <TextBlock DockPanel.Dock="Right" Foreground="Red" FontSize="14"
                               Text="{Binding [0].ErrorContent}" Margin="4,0" />
                    <AdornedElementPlaceholder />
                </DockPanel>
            </ControlTemplate>
        </Setter.Value>
    </Setter>
</Style>
```

## 6. DataGrid 与大数据列表

```xml
<DataGrid ItemsSource="{Binding Orders}" AutoGenerateColumns="False"
          EnableRowVirtualization="True" EnableColumnVirtualization="True"
          VirtualizingStackPanel.IsVirtualizing="True"
          VirtualizingStackPanel.VirtualizationMode="Recycling"
          IsReadOnly="True" SelectionMode="Single" SelectionUnit="FullRow">
    <DataGrid.Columns>
        <DataGridTextColumn Header="订单号" Binding="{Binding OrderNo}" Width="160" />
        <DataGridTextColumn Header="金额" Binding="{Binding Amount, StringFormat=N2}" Width="*" />
    </DataGrid.Columns>
</DataGrid>
```

- 超过 1 万行优先**分页/增量加载**，虚拟化只是兜底；
- 批量刷新集合：先 `List<T>` 组装再整体替换 `ObservableCollection`，避免逐条 Add 触发 N 次 UI 刷新（或实现 RangeObservableCollection）；
- 需要 Excel 式交互（公式、冻结、单元格合并）→ ReoGrid，别硬拗 DataGrid。

## 7. 托盘图标

```powershell
dotnet add package H.NotifyIcon.Wpf
```

```xml
<tb:TaskbarIcon x:Key="TrayIcon"
                IconSource="/Assets/app.ico"
                ToolTipText="MyApp"
                DoubleClickCommand="{Binding ShowMainWindowCommand}"
                LeftClickCommand="{Binding ShowMainWindowCommand}">
    <tb:TaskbarIcon.ContextMenu>
        <ContextMenu>
            <MenuItem Header="显示主窗口" Command="{Binding ShowMainWindowCommand}" />
            <Separator />
            <MenuItem Header="退出" Command="{Binding ExitCommand}" />
        </ContextMenu>
    </tb:TaskbarIcon.ContextMenu>
</tb:TaskbarIcon>
```

（在 App.xaml 或窗口 Resources 中声明；最小化到托盘 = `Hide()`，还原 = `Show()` + `Activate()`。注意 `Closing` 事件里按配置决定取消关闭。）

## 8. 窗口标题栏与现代化效果

- MDIT：`Style="{StaticResource MaterialDesignWindow}"`；
- WPF-UI：`ui:FluentWindow` + `WindowBackdropType.Mica`（Win11）；
- HandyControl：`hc:Window` 或库窗口样式；
- 自绘标题栏：`WindowChrome` + `WindowStyle="None"`，注意保留系统菜单（`SystemMenu`）与双击最大化/还原。

Win11 效果（Mica/圆角）通过 Win11 API 实现，库通常已封装；**必须提供降级路径**（Win10 下不崩、不变形）。DPI：app.manifest 声明 `<dpiAware>true/PM</dpiAware>`，布局用 `UseLayoutRounding="True"`。

## 9. 本地化与文案管理

- 方案 A（推荐）：文案进 `Resources/Strings.zh-CN.xaml` 等资源字典，界面用 `{DynamicResource Key}`，运行时换字典即可切语言；
- 方案 B：`.resx` + 自定义 MarkupExtension/Binding 到 LocalizationProvider，适合与后端返回文案混合的场景；
- 禁止把中文硬编码在 XAML 的 `Content="保存"` / 后台 `MessageBox.Show("确定？")` 里。

## 10. 快捷键与输入绑定

```xml
<Window.InputBindings>
    <KeyBinding Key="S" Modifiers="Ctrl" Command="{Binding SaveCommand}" />
    <KeyBinding Key="F5" Command="{Binding RefreshCommand}" />
</Window.InputBindings>
```

- `CanExecute` 与按钮同步刷新用 `[NotifyCanExecuteChangedFor]`；
- 全局热键（窗口失焦也响应）需 `RegisterHotKey` Win32 API 或 H.NotifyIcon 生态方案。
