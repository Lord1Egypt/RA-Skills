# 配置本机清理策略

[策略模板](cleanup-policy.example.json) 的清理清单为空。首次使用时，将模板复制到当前用户的本地目录。升级技能时继续使用这份本机配置。先核对源码清单、构建命令、目标路径和启动入口，再填写已获批准的项目。仅查磁盘增长时可以跳过配置。

```powershell
$dir = Join-Path $env:LOCALAPPDATA 'WindowsDiskCare'
[IO.Directory]::CreateDirectory($dir) | Out-Null
$policy = Join-Path $dir 'policy.json'
if (-not (Test-Path -LiteralPath $policy)) {
    Copy-Item -LiteralPath '.\references\cleanup-policy.example.json' -Destination $policy
}
```

- `Repository` 填已获授权的本地 Git 工作副本根绝对路径。程序根据 Git 列出属于该仓库的工作树。默认报告目录为 `%LOCALAPPDATA%\WindowsDiskCare\reports`，也可用 `ReportDirectory` 指定单独的本地目录。
- `ApplicationNames` 填允许处理的 Electron 应用可执行文件基名，可以为空。只支持各工作树的 `.local\desktop-package\build-<字母或数字>\<名称>-win32-x64` 布局，且需要匹配的 EXE 和 `resources\app.asar`。每个工作树按构建目录最后写入时间保留 `KeepValidPackages` 份有效包，默认两份。可用 `MinimumAgeDays` 延后淘汰。只处理应用负载，保留外层验收记录。
- `RustTargetDefinitions` 中每项包含 `TargetRoot`、对应的 `SourceManifest`（Cargo.toml 的绝对路径）和 `Profiles` 数组。核对该项目实际使用的 Cargo target 和其中的 `CACHEDIR.TAG`。支持 `debug`、`release` 和 `x86_64-pc-windows-msvc/release`，仅处理各 profile 的 `incremental`、`deps`、`build` 下确认可再生的单硬链接编译文件。适用的空闲时长由 `RustMinimumIdleHours` 控制，默认 24 小时。工作树内采用 `.local\upstream-build\target-windows` 布局的旧项目也可通过 `RustCaches` 单独登记具体缓存目录。
- `ProtectedPaths` 可放置须保留的固定制品及用户目录。程序检查 Windows 桌面和开始菜单。其他实际使用的快捷方式目录可加入 `ShortcutRoots`。用 `.keep` 或 `PINNED` 标注仍需验收的构建。
- 运行 [Measure-Growth.ps1](../scripts/Measure-Growth.ps1) 时可用 `-PolicyPath` 让监测自动采用同一仓库、已登记 Cargo 目标及报告目录。单独监测某一路径不会授予清理权限。保留最近 32 次增长采样，每次预检及执行各有独立报告。
