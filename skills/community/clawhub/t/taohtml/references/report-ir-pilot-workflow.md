# Report IR 工程工作流

仅在当前工程或项目已有明确的 Report IR 授权时读取本文件。Report IR 是正式可用的工程路线，
不是客户需要理解、选择或确认的新产品步骤。没有授权时，继续执行 `SKILL.md` 中现有的
direct-HTML 默认流程；不得根据项目类型、模型偏好或 Report IR 文件存在来推断授权。

## 路由合同

Report IR 授权必须是当前任务根目录内的 JSON 文件，且只包含以下字段：

```json
{
  "schema_version": "1.0",
  "authorization_type": "report_ir_engineering_pilot",
  "status": "authorized",
  "scope": "project",
  "task_id": "与 production state 完全相同的任务标识",
  "route": "report_ir_pilot",
  "authorization_ref": "当前工程授权的稳定引用"
}
```

向客户继续使用原有想法、Word/PDF、PPT/HTML 入口、材料理解、设计选择和简报确认流程。
不要询问“是否使用 IR”，不要展示 JSON 字段，也不要增加一次 IR 确认。Report IR 授权是
内部工程状态，不是客户决策。授权文件一旦传给编排器，就已选择该工程路线；任何后续失败
都必须留在该路线修正或停止，禁止回退 direct HTML。JSON 内的 `pilot` 值仅为兼容既有
编排器的机器字段，不代表 Report IR 处于试点状态。

## 从已确认简报派生 IR

只有 `check_production_authorization.py --action formal-html` 对当前任务、当前文件返回允许后，
才创建 Report IR。读取 `references/report-ir-v1.md`，从已确认简报和已有选择派生 Report IR：

- 新建 Report IR 工程使用 `report_ir_version=1.1`，把简报中已确认的主 Workflow Profile
  稳定 id、`definition_version=2.0`、语义选择依据和 bounded capability overlays
  写入一个通用顶层 `workflow_profile`；不复制完整 Profile 或场景特有简报；
- 既有 `1.0` 工程仅作为 `legacy_unbound` 继续验证/编译，不从简报、标题、主题、
  企业 Profile 或材料内容补猜 binding；升级必须由上游明确生成新的 `1.1` IR；

- 从交付用途派生 `delivery_mode`、报告原型、信息密度和 Runtime 目标模式；
- 从证据边界派生 evidence rigor、Claim—Evidence—Source 关系和待核实项；
- 从 Production Authorization 已记录的设计决定派生八套内置系统之一、客户参考 Project Theme 或企业模板绑定，以及 `minimal | moderate | rich` 动效密度；不得用 IR 重选或覆盖；
- 从内容结构派生章节、叙事单元、页面任务、Visual Intent 和必要的 State Sequence；
- 把当前简报的任务内相对路径和 SHA-256 分别写入
  `traceability.design_brief_ref` 与 `traceability.design_brief_sha256`。

不得重复询问这些已知选择。内置视觉路线仍执行 `references/visual-systems.md`：客户未明确
缩小范围时先完整展示八套；客户参考、企业模板和企业档案的优先级不变。主题与动效未由
客户选择或明确委托时，Production Authorization 必须先阻塞，不能由 IR 补猜。模型负责把
已确认内容表达成 IR，但不得在 IR 之后再次完整手写 HTML。

Profile binding、设计简报确认、Report IR 授权与 current-file Production Authorization 是
独立事实：binding 不授权 Report IR 工程，Report IR 授权不确认简报，简报确认也不替代
Production Authorization。普通 direct-HTML 路由不读取或创建 binding。

## 确定性编排

首次构建运行：

```bash
python scripts/orchestrate_report_ir_pilot.py \
  --artifact-root <current-task-root> \
  --status-output <current-task-root>/records/report-ir-pilot-status.json \
  --pilot-authorization <current-task-root>/gates/report-ir-pilot-authorization.json \
  --production-state <current-task-root>/gates/production-state.json \
  --report-ir <current-task-root>/report-ir.json \
  --output-dir <current-task-root>/build
```

客户参考或企业模板路线另传已验证的 `--project-theme-dir`。编排器会按顺序：

1. 验证项目级 Report IR 授权并绑定 `task_id`；
2. 复用 Production Authorization 检查当前 confirmed brief、其绑定当前主题/不适用状态与动效决定的 canonical digest，以及 `formal-html` 权限；
3. 要求 IR 的简报路径和哈希、内置主题（适用时）及动效密度与当前 Production Authorization 决定完全一致；
4. 复用 Report IR Validator 的四层结果；
5. 调用本地 `compile_report_ir.py` 编译核心并记录 HTML、规范化 IR、Manifest 哈希及
   `workflow_profile.binding_state/binding_sha256`；
6. 把 QA 与 Handoff 明确记录为 `not_executed`，直到真实记录被提供。

`compiled_pending_qa_handoff` 只说明本地 Compiler 已产生候选 HTML，不表示完成浏览器 QA、
可交付或已发布。出现无效 IR、主题不匹配、编译失败或文件漂移时，读取状态文件的
`diagnostics` 修正同一路由；不得让模型改走完整手写 HTML。

## 既有 QA 与 Handoff

对编译后的 `build/index.html` 执行 `SKILL.md` 已有 asset QA、browser profile、浏览器 QA、
Runtime/editor、追踪和 delivery verification 流程。使用现有 Project Handoff 合同生成记录，
不要复制检查实现。Handoff 的 current HTML 必须：

- 使用 Project Handoff `schema_version=1.1`；
- `locator` 指向当前 `build/index.html` 并绑定其 SHA-256；
- `versions.compiler_version` 等于 Build Manifest 的 Compiler 版本；
- `report_ir_ref` 以 `portable_path` 指向当前 `build/report.ir.normalized.json` 并绑定其 SHA-256；
- `current_build.artifact_ref` 指向上述 current HTML；
- `current_build.build_manifest_ref` 以 `portable_path` 指向刚生成的
  `build/build-manifest.json` 并绑定其文件 SHA-256；
- `current_build.workflow_profile` 只抄录刚生成 Manifest 的 binding state、主 Profile id、
  definition version 与 binding hash，不复制 selection basis、overlays 或 Profile 全文。

记录完成后，使用同一命令加上：

```bash
  --handoff <current-task-root>/project-handoff.json
```

编排器复用 `validate_project_handoff.py`，分别保留 `schema_valid`、`bindings_valid`、
`continuation_ready` 和 `delivery_ready`。它只验证已有 QA/Handoff 记录，状态始终保留
`not_executed_by_orchestrator` 与 Validator 的 `not_executed_by_validator` 声明；不得因此声称
编排器或 Validator 执行过浏览器 QA。提供 Handoff 时，编排器还要求这份最小记录与本次
刚生成的 HTML、规范化 IR、Build Manifest、Compiler version 和 Workflow Profile binding
完全一致；旧 `1.0` Handoff 不能冒充本次 build binding。只有当前 Handoff 自身记录为
`delivery_ready=true`，
才可进入既有正式交付动作。

## 普通流程不变

不传 `--pilot-authorization` 时，编排器只写入 `direct_html_unchanged`，不读取 IR、不创建
build，也不改变现有正式制作流程。普通项目不需要运行本脚本；保留该直接路由主要用于审计
和自动化验证，不能把它当作启用 Report IR 的默认入口。
