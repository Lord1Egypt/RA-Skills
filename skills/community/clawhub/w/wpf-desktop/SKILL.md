---
name: wpf-desktop
description: Build, maintain or audit Windows WPF/XAML apps, including windows, DPI, tray, SDK/NuGet and packaging. Windows WPF 新建、维护与只读评估；新建或整体升级对齐 .NET 10，局部修复也检查已采用的建议依赖升级。SDK/TFM-only audits can use desktop-app-standard --dotnet.

metadata:
  version: "1.3.21"
  openclaw:
    homepage: https://github.com/rockbenben/aishort-skills/tree/main/skills/wpf-desktop
    emoji: "🪟"
    os: ["win32"]
    files:
      - project-setup.md
      - startup.md
      - startup-template.md
      - upgrade-dependencies.md
      - pitfalls.md
      - dev-switches.md
      - github-actions.md
      - templates/ci.yml
      - templates/package-release.ps1.txt
      - templates/UpdatePackage.cs
      - templates/ElevatedStartup.cs
      - templates/ElevatedStartup.Tests/ElevatedStartup.Tests.csproj.txt
      - templates/ElevatedStartup.Tests/Program.cs
      - templates/test-startup.ps1.txt
---

# WPF desktop apps

Start with the WPF project, its effective SDK and target framework, and the user-visible behavior involved. Follow the user's version, platform, component and read-only constraints.

## Choose the scope

| Request | Action and verification |
| --- | --- |
| Skill and repository only, or general maintenance | Review SDK, NuGet packages, startup, window/tray lifecycle, DPI, publish profiles and CI. Apply the startup and delivery checks below. Confirm gaps with existing smoke checks or targeted probes, then fix those with demonstrated impact and a way to verify the result. |
| New app, whole-project upgrade or adoption of the full standard | Use [项目起手与发布配置](project-setup.md) for component choices, project structure, SDK/test configuration, publish profiles and the distribution matrix. Apply upgrades across the solution, tools and CI. |
| Feature or specific fault | Follow the affected code and required companion changes; verify the feature/fix and any dependency changes. Use the diagnostic guide below for symptom-specific checks. |
| Read-only assessment or plan | Inspect project files, existing results and configured feeds. Report findings, evidence and proposed checks, preserving the working tree. If available, use `desktop-app-standard`'s `audit.mjs <repo> --dotnet` for static SDK, TFM and CI checks. |

Every task follows [依赖升级](upgrade-dependencies.md): check all adopted recommended dependencies, including `xunit.v3`, and upgrade versions below their selected targets in write-enabled tasks, including focused fixes. That guide owns version selection, required major migrations, other dependency scope and blocker reporting. Add absent components only when needed; user version constraints and read-only scope take precedence.

## Default logon-startup maintenance check

For new apps and general maintenance, read [自启部署与排查](startup.md) and assess plain startup, resident administrator startup and occasional UAC needs. Implement applicable missing controls, registration, repair, removal and state/error feedback within the authorized scope; preserve read-only and product constraints. Keep startup opt-in and support portable paths as the guide specifies.

Adapt existing registration code first. When adopting or changing [ElevatedStartup.cs](templates/ElevatedStartup.cs), read [模板接入与隔离测试](startup-template.md) for entry-point dispatch, API results, configuration and the isolated runner. Ordinary tests use substitutes; real UAC and logon checks use an isolated integration environment.

## CI and release adoption

For new apps, general maintenance and full-standard adoption, check the [distribution matrix](project-setup.md#发布包组织三轨分发矩阵安装包--便携-zip--框架依赖精简版) and identify the actual delivery channel. For GitHub Releases, follow [发布工作流](github-actions.md) to adapt the CI and shared packaging script, validate assets and inspect PR/tag runs. That guide also covers signing, winget, update integration and upgrade/uninstall checks. For stores, internal delivery or manual publication, record the corresponding path. Public publication and external service configuration follow the user's requested scope.

## Find a diagnostic or release guide

| Task or symptom | Where to start |
| --- | --- |
| White flash, slow startup, focus, multi-monitor placement, buttons off screen, RTL text, shell icons or hotkeys | [按症状查 WPF 故障](pitfalls.md). Search its headings, e.g. 「副屏上窗口位置算错」 or 「德语界面上控件被挤没」. |
| Stale lists, blocking filters, config recovery or update caching | [按症状查 WPF 故障](pitfalls.md), e.g. 「后台扫描完成了，筛选列表仍然卡顿」. |
| Lazy-loaded XAML, WPF test hosts, layout screenshots, phase timing, intermittent activation or translation coverage | [开发期自查工具](dev-switches.md). Use the probe that exposes the symptom. |
| Administrator logon startup, account/path rejection, single-file task paths or stale startup settings | [自启部署与排查](startup.md). For template adoption or changes, continue to [模板接入与隔离测试](startup-template.md). |
| Elevated helper has no usable confirmation, RunAs uses the wrong data directory, or a retry changes its approved scope | [按症状查 WPF 故障](pitfalls.md)「提权重试进程在跑，却没有可操作的确认框」. For real consent, Explorer drag/drop or crash-recovery evidence, read [开发期自查工具](dev-switches.md)「人工交互验收」. |
| Component choices, SDK/test configuration, profiles, installer or EXE icon | [项目起手与发布配置](project-setup.md). |
| GitHub Actions, packaging, checksums, signing, publication, winget or download updates | [发布工作流](github-actions.md). |

## Verify the result

Apply the checks relevant to the selected scope, including required dependency changes. Read-only assessments use existing results and report proposed checks; they do not run restore, build, tests, registration or publication that could change project or system state.

- **Build and tests.** Restore and build with the effective SDK; use the repository's runner and [test-result checks](dev-switches.md#测试运行与结果判定). On Windows, exercise affected windows and tray lifecycle, including close/reopen. Use the [smoke harness](dev-switches.md#--smokeci-里防-xaml-错误带到发版) when available.
- **Layout or DPI.** Use [layout acceptance checks](dev-switches.md#截图的盲区) on the affected monitor and state; screenshots alone do not prove controls are reachable.
- **Startup or intermittent failures.** Use the [timing probe](dev-switches.md#分段计时探针定位启动耗时) or [repeated trials](dev-switches.md#间歇性问题跑-n-轮记比分), and report comparable results.
- **Logon startup.** Report the need, changes or reason not applicable, and the evidence level from [自启验收](startup.md#验证结果). Template changes also run the [isolated tests](startup-template.md#隔离验证).
- **Delivery.** Follow [产物验证](github-actions.md#产物验证) and the relevant installer/update checks; distinguish local checks, hosted runs and actual device execution.
- **Dependency upgrade.** Include the [upgrade verification record](upgrade-dependencies.md#验证与交付记录).
- **Report.** State what you checked, what you found, what you changed and how you verified it. Include comparable measurements for performance claims and identify checks that still need a device, runner or published build.
