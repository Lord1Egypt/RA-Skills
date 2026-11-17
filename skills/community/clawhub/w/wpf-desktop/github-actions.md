# WPF CI 与直接发布

本页适用于 GitHub Releases。新建、通用维护与整体采用先按[三轨分发矩阵](project-setup.md#发布包组织三轨分发矩阵安装包--便携-zip--框架依赖精简版)确认产物及明确例外；专项修复检查受影响的发布路径。缺少合适工作流时，将 [ci.yml](templates/ci.yml) 复制到 `.github/workflows/ci.yml` 并适配。默认 Windows test → release：测试通过后构建、签名、打包，再由 `softprops/action-gh-release` 以 `draft: false` 直接公开。审批、草稿、provenance 和 SBOM 按项目要求配置。

沿用现有项目结构、测试框架、安装器与可用的 reusable workflow，并追溯复用实现及源 revision。版本迁移统一按[依赖升级](upgrade-dependencies.md)执行。适配入口如下：

| 输入 | 适配方法 |
| --- | --- |
| 应用与版本 | 替换 Xxx、src/tests 路径，保留实际版本源；模板接受稳定 tag `vX.Y.Z`。 |
| 测试 | 模板使用 MTP；已有 VSTest 沿用原方式。命令、配置与实际用例数判定见[测试运行与结果判定](dev-switches.md#测试运行与结果判定)。 |
| 发布与安装器 | 按矩阵同步 publish、签名路径、ZIP 清单和下载说明；安装范围或提权方式变化也同步说明。模板要求四份 profile 和安装器；有明确包型例外时，同时适配工作流与打包脚本，不能只删除安装器步骤。 |
| 签名 | 按下节配置服务与验证要求。 |

## 签名

可使用 [Azure Artifact Signing](https://azure.microsoft.com/products/artifact-signing)（前身 Trusted Signing）。按服务当前身份、地区与证书要求核对发布者资格，配置 Azure 联合身份及仓库变量。应用 exe 在封装安装器前签名，安装器生成后再签名；所有最终签名先于打包和摘要生成。启用签名时给打包脚本传 `-RequireSigning`，任一应用或安装器签名无效即失败。

未配置签名时模板跳过该步骤，在 release 说明中披露未签名状态及可能出现的未知发布者提示，并提供 SHA256；摘要不能替代发布者身份验证。

## 共用打包入口

将 [package-release.ps1.txt](templates/package-release.ps1.txt) 复制为 `tools/package-release.ps1`，本地和 CI 调用同一脚本，要求 PowerShell 7.4+。`.txt` 后缀用于让 skill 发布包保留脚本原文。构建 profile 和安装器后运行，例如：

```powershell
./tools/package-release.ps1 -AppName Xxx -Tag v1.2.3 -PublishRoot src/Xxx.App/bin/Release -Installer artifacts/Xxx-v1.2.3-setup.exe -OutputDirectory artifacts/release -RequiredFiles e_sqlite3.dll
```

| 参数／行为 | 接入要求 |
| --- | --- |
| `RequiredFiles` | 填实际外置资源和原生库，无此依赖时省略；脚本逐 profile 检查存在性及 exe 的 PE 架构。 |
| `SmokeEnvironment`／`SmokeMarker` | 配置应用自有数据路径、禁止 Shell 集成开关及 marker 名，避免测试注册热键、启动项、右键菜单或访问真实数据。脚本已隔离 TEMP/TMP/APPDATA/LOCALAPPDATA，并使用独立解包目录。smoke 实现见[自查工具](dev-switches.md#--smokeci-里防-xaml-错误带到发版)。 |
| ZIP 与摘要 | 收录干净 publish 目录的文件和子目录，保留资源及原生库，排除调试文件与开发数据。`SHA256SUMS.txt` 使用 LF；摘要和上传来自同一明确资产列表，`fail_on_unmatched_files: true` 使缺资产失败。 |

## 产物验证

| 阶段 | 检查与证据边界 |
| --- | --- |
| 脚本回归 | 用临时目录调用同一打包入口，覆盖缺安装器、缺外置资源、架构错误和已要求签名却签名无效；安装器编译覆盖带空格路径。控制台夹具只证明打包与进程启动。 |
| 发布包运行 | 从独立解包目录运行 x64 自包含／框架依赖包，smoke 实际读取资源并完成 WPF 窗口布局。ARM64 用可用 runner／设备验证启动、原生库与更新；交叉构建和 PE 检查不算设备运行，缺环境记为待验。 |
| GitHub 送达 | 检查 PR 门禁和同一 tag 的 release run，沿 needs 追踪测试、构建、签名、打包与上传。公开后从干净目录下载实际资产，与本次构建清单、SHA256、所选架构及 latest／下载入口核对，并按上行复验下载包。 |
| 安装与更新 | 按[安装器配置](project-setup.md#inno-setup-6-最佳实践配置要点)核验英文安装／卸载向导，再执行下文升级卸载或应用内更新检查。 |

发布说明给出本版本变更、实际下载类型、运行时要求、架构与签名状态。默认自动生成版本说明；维护 changelog 时链接真实版本段。交付记录区分本地检查、hosted runner 与设备运行，注明 release run、所选包和待验项。

## SDK、权限与重跑

SDK 来源及 `global.json` 配置见[项目起手](project-setup.md#sdk-固定globaljson-一处说了算)，CI 从实际构建目录确认版本。PR 使用 `contents: read`，release job 才获得 `contents: write`，签名 OIDC 按需使用 `id-token`。

Release Action 使用 `make_latest: legacy`，按 GitHub 版本规则判断 latest。同一 tag 重跑沿 Action 的资产覆盖语义处理；immutable releases 或特殊发布策略须核对服务端限制与 Action 支持。

## winget 送达检查

只保留一个提交来源。默认由中央 winget-manifests 的 `apps.json` 登记并统一提交，发布仓完成 GitHub Release；既有项目自行提交时，在 release 验证成功后调用原工具，首次提交和 token 配置沿用项目流程。`GITHUB_TOKEN` 发布的 Release 不会触发其他 `on: release` 工作流。

核对实际登记状态、包标识、公开源、所选资产、架构、安装器类型及 ARP 身份。安装器支持[静默开关](project-setup.md#inno-setup-6-最佳实践配置要点)；框架依赖 ZIP 仅在声明 Desktop Runtime 依赖时作为目标。已有 portable 包改用安装器时，沿原包标识验收迁移与用户更新路径；`winget upgrade` 另核对 ProductCode、Scope 和版本识别。

直接公开上传后，中央巡检等待所选文件和完成标记齐备，再计算真实 URL／散列并提交。尚无公开资产的新包保留待发布登记，不生成虚构版本或摘要；发布仓只在既有要求下触发中央提交。

## 升级与卸载验收

已有安装用户时，用隔离 AppId、安装目录及用户文件哨兵验证 N→N+1：设置与用户文件保留，受管文件和 Shell 注册按产品约定清理。全新安装／卸载与旧版升级后卸载分别验收。

### 修了卸载规则，旧版升级后仍会删除用户文件

历史安装器卸载日志可能在覆盖升级时沿用。修改清理规则后，确认旧日志的迁移方式，并在上述两条路径分别核对用户文件保留和受管文件清理。

## 应用内更新

按产品实际能力验收：打开 Release 页提示、下载校验后手动替换、安装器自动升级和纯离线手动更新分别处理；离线应用不引入更新服务。使用 `releases/latest` 时核对它指向已公开的预期稳定版，不以草稿或预发布代替。

下载与缓存可采用 [UpdatePackage.cs](templates/UpdatePackage.cs)：按 `ProcessArchitecture` 精确选择自包含 ZIP，以架构和版本隔离缓存，拒绝未知架构及非法版本。模板只负责选包和路径，不联网、验签、提取或替换；接入层在解包前校验 SHA256，成功提取后才标记缓存完成，并处理失败清理与重试。中断、并发及缓存复用故障见 [pitfalls.md](pitfalls.md#更新缓存里有-exe却可能是上次中断留下的半成品)。

静态候选可用 `desktop-app-standard` 的 `audit.mjs <repo> --dotnet --ci-only` 检查 SDK、已知缓存、打包和英文安装器漂移；它不能替代以上运行与交付验收。
