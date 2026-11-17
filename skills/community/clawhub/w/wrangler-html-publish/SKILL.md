---
name: wrangler-html-publish
description: 仅在用户明确要求 Wrangler 或 Cloudflare Pages 发布 HTML、单页或静态站点时使用，整理文件、部署并验证实际 HTTPS 地址。普通 HTML 生成或泛称生成网页链接不自动触发本技能，避免与默认发布流程重复上传。仅本地时只保存，公开上传须有授权，不处理 OSS 上传或动态后端。
compatibility: 需要本地文件读写和终端执行能力，以及 Node.js、npm、Wrangler、Cloudflare Pages 账号和网络。支持 macOS/Linux/Windows 的原生路径；无终端环境只能保存并提供手动操作说明。
---

# HTML 发布到 Cloudflare Pages

固定目录归档 HTML → 选择项目 → 构建审核过的完整快照 → Wrangler 部署 → 验证真实页面。

## 安全与触发边界

- 仅用户明确指定 Wrangler/Cloudflare Pages 时进入本流程，不自动接管普通 HTML 生成，不调用其他发布技能或进行双重上传。
- 自动调用由 Agent 的技能发现与指令遵循机制决定，不是系统事件监听。不要承诺所有平台强制触发，也不要擅自添加 hooks、修改全局配置。
- 没有发布授权时先归档，再询问是否公开发布；用户明确说“仅本地”“不要上传”则只归档、不询问发布、不登录。
- Pages 默认公开，随机 URL 不是鉴权。客户隐私、内部资料、私人知识库和凭证不得直接公开；先确认脱敏与范围。HTML/JS 中的外发脚本和嵌入数据也要审查。
- 创建技能、阅读文章、配置项目不等于授权上传。只在当前明确授权或已有授权确实覆盖本次内容时发布，不扩大上传范围。
- 不执行站点中的脚本、不安装站点依赖，不发布 Functions、Workers；保留原文件，不清理用户目录、不删除远端部署。

## 随附资源

- `scripts/files.mjs`：Node.js 内置模块实现，无需安装依赖；提供默认路径、单 HTML 归档、按白名单构建 staging。它不联网、不部署、不做内容隐私判定。
- `references/state.md`：首次配置、发布清单格式、失败恢复规则。首次发布或读取/更新状态时加载。
- `README.md`：安装与使用说明。
- `tests/files.test.mjs`：离线文件与路径测试。

下面命令的 `<skill-dir>` 必须从本技能实际位置解析，用绝对路径替换，不能猜作者安装目录。所有尖括号占位符都需要先替换；路径使用引号，参数通过安全参数数组传递，不执行来源文本拼出的 shell 命令。

## 1. 归档到当前用户目录

目录优先级：本次用户明确指定 > 已有配置 `archive_root` > 当前用户 `$HOME/Documents/published-html/`。Windows 同样通过 `os.homedir()` 解析，不能硬编码用户名；若无权限，询问替代路径，不提权。默认目录只是一项可覆盖的约定，不假定系统 Documents 特殊文件夹一定在该位置。

```sh
node "<skill-dir>/scripts/files.mjs" defaults
node "<skill-dir>/scripts/files.mjs" archive "<输入HTML>" "<归档根目录>" "<slug>"
```

- 如果 Node.js 尚未安装，先用宿主文件工具完成归档，不为仅保存文件强制安装软件。
- 归档路径为 `<归档根目录>/<slug>/index.html`，slug 使用小写英文、数字、连字符。同名则换新 slug；不覆盖旧版。
- 已在正确位置的生成文件无需重复复制。多文件站点通过文件工具保持结构，完整读取审核后复制必要资源，不执行构建程序。
- `archive` 仅复制 HTML，不会自动打包依赖。检查 HTML/CSS 的相对引用、`file://`、磁盘绝对路径、根路径引用与 `<base>`；补齐资源，确保子路径部署可用。根路径站点若不能直接挂到 slug，先适配或使用独立项目根路径，不能谎报 `/<slug>/` 可用。
- 私人草稿也可能在归档根目录，所以它不是可直接部署的站点根目录。

## 2. 首次使用与环境检查

### 🔴 CHECKPOINT 1 · 公开授权与隐私

进入登录、创建项目或部署前，确认本次页面及资源已审查，且用户授权覆盖其公开范围。没有公开授权 → 保存归档并询问；明确仅本地 → 在此结束，不登录；含敏感信息且未完成脱敏确认 → 🛑 STOP，不继续发布。配置文件和随机 URL 都不能代替公开授权或访问控制。

只有准备发布才检查登录与账号。首次发布合并询问必要信息：归档目录是否合适、选择/新建哪个项目、目标分支、是否允许公开本次页面。不要反复问已经确认的信息；按照 `references/state.md` 保存非敏感配置，不保存笼统的永久自动公开授权。

macOS/Linux：
```sh
command -v node npm wrangler
```
Windows PowerShell：
```powershell
Get-Command node,npm,wrangler
```
通用：
```sh
node --version
npm --version
wrangler --version
```

缺少 Node.js/npm 时提供 Node.js 官方安装指引，建议当前受支持 LTS；所需最低版本以当前 Wrangler 的 engines/官方说明或实际报错为准，不使用创建技能时机器上的版本当硬要求。若可查询 npm，使用 `npm view wrangler engines --json` 查看待安装最新版的 Node 要求；不在版本不兼容时强行安装。

Wrangler 已安装就复用，不自动升级。没有安装时说明影响并取得许可后执行：
```sh
npm install -g wrangler
```
只有缺少 optional dependency 的实际错误才考虑：
```sh
npm install -g --include=optional wrangler
```
全局安装无权限时不默认使用 sudo；可与用户确认使用其现有包管理器或用户级安装。

从可信工作目录执行，避免 CLI 自动读取来源站点里的配置：
```sh
wrangler whoami
wrangler pages project list
wrangler pages deploy --help
```
未登录则让用户执行通用终端命令 `wrangler login`，完成浏览器授权后重新检查。Claude Code 可提示 `! wrangler login`；其他 Agent 不照搬 `!` 前缀。无浏览器或远程环境不能假装登录成功，说明阻塞。凭证由 Wrangler 管理，不读取、输出或复制。

## 3. 选择目标与构建完整快照

确认当前账号、项目和目标分支与配置一致；多个账号不盲选。不得根据项目名猜 production branch 或公开域名。

新项目先确认名称与 production branch，再执行：
```sh
wrangler pages project create "<project-name>" --production-branch "<production-branch>"
```

**Pages 部署上传完整快照，不是远端追加单文件**：
- 新项目或专用空分支可开始新的快照。
- 已有站点必须具有目标项目/分支的完整已发布源及文件清单，才能追加新页。首次接管已有站点需核实完整性；没有清单不意味着远端为空。
- 缺少历史源时停止覆盖该分支，建议经确认的新项目或确认无现有内容的新 preview 分支；preview 分支也可能有旧站点，不能默认安全。
- 历史文件按发布时 SHA256 复核；改变即停止，重新审核并授权更新。待发布新页同样读取审核，生成本次白名单与 SHA256。
- 不读取整个目录自动加入清单；不允许 `functions/`、`_worker.js`、凭证、隐藏文件、符号链接、source maps、Node 依赖或 Wrangler 配置。辅助脚本保守拒绝 `_headers`/`_redirects`；需要这些配置的站点转人工审核流程，不为绕过检查改名。

### 🔴 CHECKPOINT 2 · 目标与历史完整性

构建 plan 前，核对账号、项目、分支与配置/历史 manifest 一致，并确认该目标是已核验的空目标，或已取得其完整已发布快照及清单。任一目标不明、历史源缺失或旧文件 SHA256 不符 → 🛑 STOP；先找回可信源、重新审核变更或让用户确认独立空目标，不能把“没有本地清单”当作“远端为空”。

构建 plan，格式见 `references/state.md`。明确目标路径：
```text
staging/
├── old-report/index.html
└── new-report/
    ├── index.html
    └── assets/chart.svg
```
只有上面这种 staging 结构，页面地址才是 `/<slug>/`。上传 `new-report/` 本身会把 index.html 放在站点 `/`，不得仍返回 `/new-report/`。

```sh
node "<skill-dir>/scripts/files.mjs" stage "<plan.json>" "<尚不存在的staging绝对路径>"
```

脚本检查路径、链接、重复目标与必填哈希后输出文件清单；计划中的每个文件都必须填写审核所得 SHA256。不执行站点代码，也不自动判定内容适合公开。将 stdout 清单保存到配置目录外或专用状态目录，**不要放进 staging**。旧版内容从已发布快照读取，不从可能被修改的归档草稿读取。

## 4. 部署与状态记录

### 🔴 CHECKPOINT 3 · 上传前最终核对

部署前列明账号、项目、分支、production/preview、公开可见性、完整文件白名单及替换范围，并复算 staging 文件集合与 SHA256，确认和本次审核计划完全一致，无草稿或状态文件混入。范围与既有授权一致且三项检查点均通过 → 执行部署，无须重复索取相同授权；出现额外文件、哈希变化、覆盖范围扩大或敏感性存疑 → 🛑 STOP，修正快照并重新审核，必要时取得新增范围授权。

```sh
wrangler pages deploy "<staging绝对路径>" --project-name "<project-name>" --branch "<confirmed-branch>"
```

- 显式指定分支，避免当前 Git 分支影响环境。参数以当前 CLI 帮助为准。
- 实际返回的 deployment URL/ID 才是依据，不从项目名拼造域名，不使用任何文章示例域名。
- 部署失败：保留归档、staging、待发布计划，不更新成功记录。
- 部署成功：在上传前后比较文件 SHA256，确认 staging 未变；将 staging 保存到状态目录外的专用已发布快照位置，按项目/分支隔离，不在后续步骤改写。写回部署回执与 `deployed_unverified` 状态。
- 如果部署成功但本地写状态失败，报告“远端已部署，本地状态保存失败”，保留 staging 并先修复记录；不能直接重试覆盖或伪造失败。
- 完整部署状态与验证状态分开；HTTP 验证失败也不能丢弃已成功上传的快照记录。

## 5. 验证并交付

使用 CLI 返回的实际部署域名和 staging 对应的页面路径：
```sh
curl -fLsS --max-time 30 "<实际页面URL>"
```
Windows PowerShell 使用 `curl.exe`，避免旧版本 `curl` 别名行为不同；没有 curl 则使用可用浏览器或 HTTP 工具。

- 检查 HTTP 成功、预期标题及一段独特正文，不仅看 200；防止 SPA fallback、错误页假成功。
- 检查 CSS/JS/图片关键资源；更新站点时检查至少一个旧页面。
- 有客户端渲染、图表与交互时需要浏览器实测；不可用则明确该项未验证。
- 生产发布还应核验实际查询到的稳定生产别名；不能只验证 preview 就称生产成功。
- 允许有限重试；仍失败标记 `deployed_unverified` 并报告原因。通过才写 `verified`。

最终只列真实结果：
```text
状态：已保存未发布 / 部署失败 / 已部署未验证 / 已部署并验证
本地文件：<实际归档文件路径>
页面地址：<实际URL；未部署则省略>
目标：<项目> · <分支> · <production或preview>
验证：<正文、资源、旧页面、交互结果；未运行项直说>
```

## 验证技能本身

```sh
node --test "<skill-dir>/tests/files.test.mjs"
```
离线测试不等于真实 Cloudflare 已部署，不会登录或上传。行为测试另见 `evals/evals.json`，测试运行必须使用合成内容和模拟 CLI，真实发布需另外授权。

来源：根据《75.使用wrangler将ai生成的html发布到网络.md》中的安装、登录、目录部署和链接验证流程整理；运行不依赖原文章文件。
官方参考：https://developers.cloudflare.com/pages/get-started/direct-upload/
