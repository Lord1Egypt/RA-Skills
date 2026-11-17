# WPF 第三方 UI 组件库与配套库

> wpf-developer 技能参考文件。主流 UI 库选型表、接入步骤、图标/图表/托盘等配套生态。

## 目录

1. [UI 库选型总表](#1-ui-库选型总表)
2. [各库接入步骤](#2-各库接入步骤)
3. [配套库（图标/图表/托盘/行为等）](#3-配套库图标图表托盘行为等)
4. [组合与冲突处理](#4-组合与冲突处理)
5. [商业库](#5-商业库)

---

## 1. UI 库选型总表

版本为 2026-10 快照，**用前以 NuGet 为准**。

| 库 | 风格 | 控件丰富度 | 维护状态 | 许可证 | 适合场景 |
|---|---|---|---|---|---|
| **MaterialDesignInXamlToolkit** | Google Material Design（MD2/MD3） | 高（全控件重绘 + Cards/DialogHost/Clock/FAB） | 活跃（5.3.2，2026-05） | MIT | 追求现代感、需要换肤/深浅色、原型与产品皆宜 |
| **HandyControl** | 扁平现代化，融合 Material + Ant Design 理念 | 很高（80+ 控件，中文文档） | 活跃（3.x，国内用户多） | MIT | 管理系统、工控软件、工具类后台 |
| **WPF-UI**（lepoco） | Fluent Design / Win11 原生观感 | 中高（NavigationView/ContentDialog/TitleBar/InfoBar） | 活跃（4.3.0，支持 .NET 10） | MIT | 想贴近 Win11 原生又不手写模板 |
| **MahApps.Metro** | Metro（Win8/10 早期风） | 中（MetroWindow/ToggleSwitch 等） | 一般 | MIT | 老牌 Metro 项目、工业控制领域存量大 |
| **ModernWpf** | WinUI 控件移植到 WPF | 中（ColorZone/ProgressRing/InfoBar） | 一般 | MIT | 老项目低成本焕新、纯 XAML 无侵入 |
| **Panuon.WPF.UI** | 在 HandyControl 基础上增强 | 高（倒计时/遮罩/自定义弹窗/卡片） | 活跃 | MIT | 快速搭建国产后台、表单密集场景 |
| **AduSkin** | 美观动效向 | 中 | 社区 | MIT | 重视觉表现的项目 |
| **AdonisUI** | 轻量，专注深浅主题切换 | 低（不堆控件） | 一般 | MIT | 只要干净界面 + 丝滑换肤，不想引重库 |
| **ReoGrid** | Excel 式电子表格 | 专精表格 | 活跃 | MIT | 数据录入、公式、大屏看板表格 |

**选择决策**：
1. 要 Material 风格/换肤 → **MaterialDesignInXamlToolkit**；
2. 国产后台/管理系统、控件要全 → **HandyControl**（或 Panuon.WPF.UI）；
3. 要 Win11 原生观感（NavigationView 侧边导航）→ **WPF-UI**；
4. 老项目轻量焕新 → **ModernWpf** 或 **AdonisUI**；
5. 只需要主题切换不换控件 → **AdonisUI**。

---

## 2. 各库接入步骤

### 2.1 MaterialDesignInXamlToolkit（5.3.2）

```powershell
dotnet add package MaterialDesignThemes
```

**App.xaml**：

```xml
<Application x:Class="MyApp.App"
             xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             xmlns:materialDesign="http://materialdesigninxaml.net/winfx/xaml/themes">
    <Application.Resources>
        <ResourceDictionary>
            <ResourceDictionary.MergedDictionaries>
                <materialDesign:BundledTheme BaseTheme="Light" PrimaryColor="DeepPurple" SecondaryColor="Lime" />
                <ResourceDictionary Source="pack://application:,,,/MaterialDesignThemes.Wpf;component/Themes/MaterialDesign2.Defaults.xaml" />
                <!-- MD3 改用：/Themes/MaterialDesign3.Defaults.xaml（MD3 Demo 覆盖度仍在完善，采用前评估） -->
            </ResourceDictionary.MergedDictionaries>
        </ResourceDictionary>
    </Application.Resources>
</Application>
```

**MainWindow.xaml**：窗口套 `MaterialDesignWindow` 样式，控件用 `materialDesign:` 前缀：

```xml
<Window Style="{StaticResource MaterialDesignWindow}"
        xmlns:materialDesign="http://materialdesigninxaml.net/winfx/xaml/themes"
        Title="MainWindow" Height="450" Width="800">
    <materialDesign:Card Padding="16" Margin="8">
        <StackPanel>
            <TextBox materialDesign:HintAssist.Hint="请输入关键字" />
            <Button Content="保存" Style="{StaticResource MaterialDesignRaisedButton}" />
        </StackPanel>
    </materialDesign:Card>
</Window>
```

要点与坑：
- **DialogHost / Snackbar / Clock / Cards** 是该库招牌控件，配方见 xaml-recipes.md；
- `materialDesignInternal` 命名空间（`http://materialdesigninxaml.net/winfx/xaml/themes-internal`）是内部实现，**不保证版本兼容，禁止依赖**；
- 升级必须全量视觉回归：主题经 MergedDictionaries + 窗口样式生效，版本变更会改变全应用控件模板；
- 可与 MahApps / Dragablz 组合（官方有 MahAppsDragablzDemo）。

### 2.2 HandyControl（3.x）

```powershell
dotnet add package HandyControl
```

**App.xaml**（官方推荐的字典合并，具体键名以官方 Wiki 为准）：

```xml
<Application.Resources>
    <ResourceDictionary>
        <ResourceDictionary.MergedDictionaries>
            <ResourceDictionary Source="pack://application:,,,/HandyControl;component/Themes/Theme.xaml"/>
            <ResourceDictionary Source="pack://application:,,,/HandyControl;component/Themes/SkinDefault.xaml"/>
            <!-- 深色：SkinDark.xaml -->
        </ResourceDictionary.MergedDictionaries>
    </ResourceDictionary>
</Application>
```

窗口可用 `hc:Window` 或应用库内窗口样式（`WindowWin10` / `WindowWin11` 等，键名随版本变化，**以官方 Demo 为准**），命名空间 `xmlns:hc="https://handyorg.github.io/handycontrol"`。

要点：中文文档友好；控件命名直观（`hc:Button` 系列、`hc:Growl` 通知、`hc:Dialog`）；主题基于 ResourceDictionary 动态合并，换肤成熟。

### 2.3 WPF-UI 4.3.0（Fluent / Win11 观感）

```powershell
dotnet add package WPF-UI
# 需要 DI/托管集成时：
dotnet add package WPF-UI.DependencyInjection
```

> 4.0–4.2 多个版本因严重缺陷被 NuGet 标记 deprecated，**直接用 4.3.0 或更新稳定版**。

**App.xaml**：

```xml
<Application xmlns:ui="http://schemas.lepo.co/wpfui/2022/xaml">
    <Application.Resources>
        <ResourceDictionary Source="pack://application:,,,/WPF-UI;component/ControlsDictionary.xaml"/>
    </Application.Resources>
</Application>
```

**MainWindow.xaml**：用 `ui:FluentWindow` 获得 Win11 标题栏/圆角/系统 backdrop：

```xml
<ui:FluentWindow xmlns:ui="http://schemas.lepo.co/wpfui/2022/xaml"
                 Title="MainWindow" Height="450" Width="800">
    <ui:NavigationView MenuItemsSource="{Binding ViewModel.MenuItems}">
        <ui:NavigationView.ContentOverlay>
            <ContentControl Content="{Binding ViewModel.NavigationService.CurrentView}"/>
        </ui:NavigationView.ContentOverlay>
    </ui:NavigationView>
</ui:FluentWindow>
```

要点：`NavigationView` + `INavigationService` + `INavigationAware` 是一套轻导航方案（配方见 xaml-recipes.md）；`ContentDialog`、`SnackbarPresenter`、`InfoBar`、`TitleBar`、`ProgressRing`、`iTaskbarProgress` 齐备；内置 Fluent System Icons（`FontIcon`/`SymbolIcon`）；`ApplicationThemeManager` 做深浅切换；`WindowBackdropType.Mica` 仅 Win11，需降级。

### 2.4 MahApps.Metro

```powershell
dotnet add package MahApps.Metro
```

App.xaml 合并 `MahApps.Metro;component/Styles/Controls.xaml` 等字典，窗口用 `MetroWindow`（`xmlns:metro="http://metro.mahapps.com/winfx/xaml/controls"`）。图标另装 `MahApps.Metro.IconPacks`（一套覆盖 Material/FontAwesome 等 10+ 图标集，见 3.1）。与 MaterialDesignInXamlToolkit 可叠加（库作者提供组合 Demo）。

### 2.5 ModernWpf / Panuon.WPF.UI / AdonisUI

- **ModernWpf**：`Install-Package ModernWpf`，App.xaml 合并 `pack://application:,,,/ModernWpf;component/Themes/Light.xaml`（或 Dark），旧项目无侵入焕新，纯 XAML 实现启动友好。
- **Panuon.WPF.UI**：`Install-Package Panuon.WPF.UI`，中文文档，增强型控件（倒计时、遮罩层、自定义弹窗、卡片视图）。
- **AdonisUI**：`Install-Package AdonisUI` + 合并 `adonisThemes:` 相关字典，主打浅/深主题丝滑切换，控件增强少。

---

## 3. 配套库（图标/图表/托盘/行为等）

### 3.1 图标

| 库 | 说明 |
|---|---|
| MahApps.Metro.IconPacks | 一个包集成 Material/FontAwesome/Feather 等十余套图标，`iconPacks:PackIconMaterial` |
| FontAwesome.Sharp | WPF 专用 FontAwesome，`fa:FontAwesome` + `ImageAwesome` |
| WPF-UI 内置 | Fluent System Icons，`ui:FontIcon`/`ui:SymbolIcon`，无需额外包 |
| MDIT 自带 | `materialDesign:PackIcon`，Material Design Icons 全集 |

### 3.2 图表

| 库 | NuGet | 特点 |
|---|---|---|
| LiveCharts2 | `LiveChartsCore.SkiaSharpView.WPF` | 动画好、MVVM 友好，活跃 |
| ScottPlot | `ScottPlot.WPF` | 大数据量性能强，科学/实时曲线 |
| OxyPlot | `OxyPlot.Wpf` | 老牌轻量，API 稳定 |

### 3.3 其他常用配套

| 需求 | 库 | NuGet |
|---|---|---|
| 托盘图标 | H.NotifyIcon.WPF | `H.NotifyIcon.Wpf` |
| 行为/触发器（替代 System.Windows.Interactivity） | Microsoft.Xaml.Behaviors.Wpf | `Microsoft.Xaml.Behaviors.Wpf` |
| 列表拖拽排序 | gong-wpf-dragdrop | `gong-wpf-dragdrop` |
| GIF 支持 | XamlAnimatedGif | `XamlAnimatedGif` |
| Excel 式表格 | ReoGrid | `ReoGrid.Wpf` |
| 表单验证 | FluentValidation（服务端/VM 侧） | `FluentValidation` |

---

## 4. 组合与冲突处理

- **可以组合**：如 WPF-UI 做窗口壳 + MDIT 做内容控件，官方与社区均有组合先例；但两套控件模板会互相覆盖，合并顺序「先壳后内容」，具体控件逐个用 `BasedOn` 修正。
- **冲突排查**：同基类控件两库都定义了隐式样式时，后合并的字典生效——不确定时显式指定 `Style="{StaticResource ...}"`，不要依赖隐式覆盖。
- **原则**：一个项目**主 UI 库只选一个**，其余按需单点引入（图表/表格/托盘），避免样式战争。

## 5. 商业库

| 厂商 | 亮点 | 费用 |
|---|---|---|
| Syncfusion | 控件全家桶 + Community License（个人/年收入 <100 万美元企业免费） | 免费档够用 |
| Telerik (Progress) | 专业 DataGrid、报表、调度 | 商业授权 |
| DevExpress | 专业 DataGrid、报表、仪表盘 | 商业授权 |

需要专业表格/报表/排程且预算允许时再引入；开源库 + 自研模板能覆盖 80% 场景，不默认上商业库。
