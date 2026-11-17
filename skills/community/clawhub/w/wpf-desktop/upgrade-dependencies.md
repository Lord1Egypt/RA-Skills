# 升级 WPF 应用的依赖

按[任务入口](SKILL.md)确定范围：新项目生成骨架后核对所需依赖，整体升级覆盖应用、共享库、测试、本地工具和 CI。开始修改前用原工具链建立构建或测试基线，可复用当前会话中同一代码状态的结果。只读评估使用仓库文件、已有还原结果和包源，保持项目文件原样。

## 已采用的建议依赖必须升级

每次任务都检查[项目起手](project-setup.md#第一个项目装什么)中的已采用建议依赖，包括 `CommunityToolkit.Mvvm`、`H.NotifyIcon.Wpf`、`xunit.v3`、Serilog、`Microsoft.Windows.CsWin32`、AvalonEdit、Velopack。查询配置包源并比较实际解析值：指定大版本时取该线最新兼容稳定版，否则取满足目标 TFM／平台的最新稳定版。允许修改时，低于目标必须升级，包含局部修复及达到目标所需的跨大版本迁移；未采用的组件按实际需求引入。

例如，旧版 `xunit.v3` 更新其 PackageReference 或中央 PackageVersion，并适配 runner、适配器和测试平台，按[测试结果判定](dev-switches.md#测试运行与结果判定)验证。`xunit.v3` 是包名，其中的 v3 不是 NuGet 版本上限；这项要求也不将其他测试框架替换为 xUnit。

用户明确锁版、只读要求与仓库规则优先。已知兼容性阻碍或缺少验证环境时，记录当前／目标版本、具体阻碍和复查条件，继续其他可完成的升级。旧 pin、现有声明范围、与本次故障无关或“这是测试依赖”本身不能作为跳过理由。

## 对齐技能指定的大版本

以下 SDK、TFM 和 CI 步骤适用于新建、整体升级或确需迁移框架的任务，包括建议依赖升级的配套迁移。目标为 `net10.0-windows` 和 **10.0.x** 稳定 SDK。已采用本技能 Inno Setup 方案的仓库，每次任务也核对并升级到 **6.x** 最新兼容稳定版。

从实际构建目录运行 `dotnet --version` 并检查生效的 global.json。只查询 10.0 通道，分别记录构建 SDK 和随应用发布的运行时补丁。

```powershell
$release = Invoke-RestMethod 'https://builds.dotnet.microsoft.com/dotnet/release-metadata/10.0/releases.json'
$sdk = $release.'latest-sdk'
if ($sdk -notmatch '^10\.0\.\d+$') { throw "无法从 .NET 10 通道确认稳定 SDK" }
$release | Select-Object 'latest-sdk','latest-runtime','support-phase','eol-date'
```

1. 把 WPF 应用从旧 TFM 迁到 `net10.0-windows`，保留明确需要的 Windows 平台版本后缀。同步修改拥有 TFM 的共享属性、应用测试、发布 profile、CI 的 SDK 来源、安装包运行时检查与下载提示。纯逻辑库按消费关系使用 `net10.0` 或保留对外承诺的附加 TFM。旧 .NET Framework 工程要迁移项目格式及不兼容 API。
2. 在构建环境安装查得的 SDK，将 global.json 的版本与 rollForward 对齐到 10.0 范围（示例用 `latestFeature`、`allowPrerelease: false`）。从实际构建目录再次核验 `dotnet --version`。如保留较低的 10.0 开发 SDK 下限，在 CI 安装并验证选定补丁。发布物使用的运行时版本还要从还原或发布结果核对。[.NET SDK 选择规则](https://learn.microsoft.com/dotnet/core/tools/global-json)
3. 仓库已经使用更高大版本时，将回迁方向写清楚，在目标 10.0 工具链验证代码。厂商 SDK、API 或平台承诺确实阻断迁移时，列出具体依赖、报错和未达标目标，继续独立可完成的升级。只有构建和运行均能验证时才报告已对齐。
4. 检查项目使用的 Actions 和本地工具。保留各 Action 的 pin 形式，按技能指定的目标或未指定时的兼容稳定版更新。同步更新已有 .NET 工具清单并运行 `dotnet tool restore`。

## 更新 NuGet 包

已采用建议依赖按上节执行。其他依赖在全面维护时全量检查，局部任务沿受影响路径检查；兼容当前 TFM／平台的稳定补丁和次版本默认直接升级，不只列作建议。依据包元数据、约束和发布说明判断兼容性；其跨大版本升级按请求范围评估。存在已知破坏性变更、额外 SDK／TFM 迁移或无法验证时记录阻碍。

1. 按 NuGet.Config 的配置源和 source mapping 查询稳定版本。SDK 风格项目先还原，再用 `dotnet list <解决方案或项目> package --outdated` 盘点各目标框架中的直接依赖，另跑 `dotnet list <解决方案或项目> package --vulnerable --include-transitive`。处理大版本和开发依赖，保留明确选择的私有源。预览版只用于项目明确指定的通道。
2. 对普通 PackageReference，.NET 10+ SDK 可执行 `dotnet package update <包名>@<已核实的版本> --project <项目路径>`。中央包管理在生效的 Directory.Packages.props 中更新 PackageVersion，检查条件、VersionOverride 及所有消费项目。遇到间接 MSBuild 属性或旧 SDK，直接编辑拥有版本的属性或引用并还原。旧式 packages.config 项目用该解决方案的 NuGet 更新流程同步引用。[dotnet package update](https://learn.microsoft.com/dotnet/core/tools/dotnet-package-update) · [中央包管理](https://learn.microsoft.com/nuget/consume-packages/central-package-management)
3. 对还原、编译或运行失败的包，先更新配套包并迁移 API、资源字典、测试或打包配置。上游确实缺少目标 TFM、原生架构等支持时，选可验证的最高稳定版本，继续其他升级。传递依赖通常通过升级引入它的直接依赖解决。
4. 在本次选定的 SDK、TFM、RID 和发布属性组合下重新还原，覆盖保留的支持组合及已迁移的配置。项目有 packages.lock.json 时，用 `dotnet restore --force-evaluate` 刷新并检查差异，再验证 `dotnet restore --locked-mode`。从还原结果核对实际版本，重跑过期包和漏洞查询。包源不可用时列明查询失败的包或源。

## 验证与交付记录

允许修改的任务按仓库 runner 跑 Release 构建和测试，结果判定见[自查工具](dev-switches.md#测试运行与结果判定)。在 Windows 启动应用、打开受影响窗口；涉及单文件、原生 DLL 或托盘时，再发布对应 profile 并运行产物。只读评估报告已有证据与待验项。

交付时记录目标大版本、实际 SDK／TFM、依赖解析版本前后对比、已执行的 Windows 检查，以及未达目标的具体阻碍和复查条件。
