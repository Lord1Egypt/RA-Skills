# SEVO Endgame 修复 Spec

OpenClaw（pm-02 子Agent） | 2026-05-22

针对终局差距扫描发现的 P1/P2 缺口，定义修复验收标准。每条 FR 引用原始编号，AC 具体到代码层面可验证。

---

## P1 — 功能不完整

### FR-29-FIX: L3 运行态验证默认检查项补全

**缺口**：`defaultRuntimeChecksForType()` 对 CLI 类型项目生成的默认检查项不足，缺少帮助输出验证、init 命令可执行性验证、demo 项目生成验证、核心命令 exit code 验证。当前 `buildCliRuntimeChecks()` 仅覆盖 `--help` 和 `--version`，未验证核心子命令的实际可执行性。

**验收标准**：

- AC-29F.1：`src/scan/default-runtime-checks.ts` 中 `buildCliRuntimeChecks()` 对 CLI 类型项目自动生成以下检查项：
  - `cli-help`：执行 `<bin> --help`，验证 exit code === 0 且 stdout 包含至少 3 个子命令名称。
  - `cli-init`：执行 `<bin> init --dry-run`（或等效的非破坏性模式），验证 exit code === 0 且 stdout 非空。
  - `cli-demo`：执行 `<bin> demo --dry-run`，验证 exit code === 0 且产出文件结构存在。
  - `cli-core-commands`：对 package.json `bin` 或内置命令列表中的每个核心命令执行 `<bin> <cmd> --help`，验证 exit code === 0。
- AC-29F.2：每个检查项的 `RuntimeDomainCheck` 定义包含 `domain`（唯一标识）、`type: 'cli'`、`command`（完整命令字符串）、`expectedExitCode: 0`、`outputValidator`（可选的 stdout 校验函数或正则）。
- AC-29F.3：`L3RuntimeVerifier.executeCheck()` 对 exit code 非 0 的命令直接判定为 `dead`，不再调用 LLM 做语义判定。
- AC-29F.4：`loadRuntimeChecks()` 在未找到 `sevo.json` 中的自定义 `runtimeChecks` 配置时，自动 fallback 到 `buildCliRuntimeChecks()` 生成的完整检查列表。
- AC-29F.5：L3 报告 `docs/gap-scan-l3.json` 中每个 entry 包含 `expectedExitCode` 和 `actualExitCode` 字段，便于自动化判定。

---

### FR-22-FIX: 角色-任务匹配独立验证模块

**缺口**：`src/role-registry/role-task-matcher.ts` 已实现匹配逻辑，但缺少独立的验证入口——当前仅在 PipelineEngine 内部调用，无法被外部工具（如 `sevo doctor`、CI 脚本）独立使用来校验角色配置正确性。缺少角色-任务匹配矩阵的可视化输出和违反约束时的结构化拒绝/警告机制。

**验收标准**：

- AC-22F.1：`src/role-registry/role-task-matcher.ts` 导出 `validateDispatchMatrix(config: RoleTaskMatcherConfig): DispatchMatrixReport` 方法，接受完整角色配置，返回所有阶段×所有 Agent 的匹配矩阵，每个单元格标注 `allowed | warned | blocked`。
- AC-22F.2：`DispatchMatrixReport` 类型定义包含：`matrix: Array<{ stageId: StageId; agentId: string; requiredRole: PipelineRole; actualRole: PipelineRole | null; decision: 'allowed' | 'warned' | 'blocked' }>`、`violations: RoleMismatchEvent[]`、`coverage: { stagesWithMatchedAgent: number; totalStages: number }`。
- AC-22F.3：`sevo doctor` 命令（`src/cli/cmd-doctor.ts`）新增角色匹配检查项：调用 `validateDispatchMatrix()`，若存在 `blocked` 且非单 Agent 环境，报告为 ERROR；若存在 `warned`，报告为 WARNING。
- AC-22F.4：PipelineEngine 在派发阶段任务前调用 `RoleTaskMatcher.match()` 时，若结果为 `blocked`，抛出 `RoleDispatchBlockedError`（包含 `RoleMismatchEvent` 详情），阻断派发并将事件写入 `dispatch-audit.jsonl`。
- AC-22F.5：PipelineEngine 在派发阶段任务前调用 `RoleTaskMatcher.match()` 时，若结果为 `warned`（单 Agent 降级），正常派发但将 `RoleMismatchEvent`（action: 'warned'）写入 `dispatch-audit.jsonl`，并在阶段执行 prompt 中注入角色降级提示。
- AC-22F.6：`src/role-registry/__tests__/role-task-matcher.test.ts` 覆盖以下场景：多 Agent 环境角色匹配通过、多 Agent 环境角色不匹配阻断、单 Agent 环境降级警告、`validateDispatchMatrix()` 输出完整矩阵。

---

### FR-11-FIX: Spec 阶段模糊检测自动触发集成

**缺口**：`src/clarification/` 模块已实现模糊检测和澄清记录写入逻辑，但 PipelineEngine 在 Specify 阶段的执行链路中未自动调用 ambiguity-detector。当前依赖外部手动调用，spec 阶段产出的工件可能包含未检测的模糊点。

**验收标准**：

- AC-11F.1：PipelineEngine 在 Specify 阶段执行完成后、进入 Spec Review Gate 之前，自动调用 `AmbiguityDetector.scan(specPackagePath)` 对 spec 工件做模糊检测。
- AC-11F.2：模糊检测结果写入阶段工件目录 `<project>/specs/clarification-scan.json`，格式为 `{ scannedAt: string; ambiguities: Array<{ location: string; signal: string; type: ClarificationType; severity: 'blocking' | 'non-blocking' }> }`。
- AC-11F.3：检测到 `blocking` 级别模糊点时，PipelineEngine 阻断向 Spec Review Gate 的推进，状态设为 `awaiting-clarification`，并通过 Adapter 向用户/上游发送澄清请求。
- AC-11F.4：检测到仅 `non-blocking` 级别模糊点时，PipelineEngine 正常推进，但在 Spec Review Gate 的输入中附带模糊点列表供审查者参考。
- AC-11F.5：`src/orchestrator/` 或 `src/stages/` 中的 Specify 阶段 handler 包含对 `AmbiguityDetector` 的显式调用，调用位置在 spec 工件写入之后、门禁评估之前。
- AC-11F.6：`AmbiguityDetector.scan()` 的模糊检测规则从配置文件加载（`sevo.config.json` 的 `clarification.rules` 字段），支持用户扩展检测维度而不修改源码（对应 AC-4.53）。

---

### FR-14-FIX: 单 Agent 降级场景角色自动分配

**缺口**：`sevo init` 的角色自动分配逻辑（AC-14.12）在检测到多个 Agent 但无法识别角色时进入交互模式，但未覆盖「只有一个 Agent」的场景——此时应自动将所有角色分配给该唯一 Agent，无需交互。

**验收标准**：

- AC-14F.1：`src/cli/cmd-init.ts` 中的角色分配逻辑新增单 Agent 检测分支：当 OpenClaw 环境中只有一个可用 Agent 时，自动将所有角色（product、ux、architect、coder、auditor）分配给该 Agent，跳过交互式角色分配。
- AC-14F.2：单 Agent 自动分配后，输出明确提示：`"检测到单 Agent 环境（<agentId>），已自动分配所有角色。流水线将以降级模式运行。"`
- AC-14F.3：生成的角色配置文件（`sevo.config.json` 的 `roles` 字段）中，所有角色池均填入同一个 agentId，与 FR-15 L0 的单 Agent 降级行为一致。
- AC-14F.4：`sevo doctor` 在单 Agent 环境下不报角色缺失为 ERROR，而是报为 INFO 级别提示（"单 Agent 降级模式，所有角色由 <agentId> 承担"）。
- AC-14F.5：`src/cli/__tests__/cmd-init.test.ts` 新增测试用例：模拟单 Agent 环境，验证自动分配所有角色、无交互提示、输出降级提示信息。

---

### FR-15-FIX: CLI 分层配置交互深化

**缺口**：`src/progressive-disclosure/` 模块定义了 L0-L3 配置层级，但 CLI 层面缺少显式的分层暴露命令。用户无法通过命令行切换配置可见级别，也缺少零配置默认值的显式声明机制。

**验收标准**：

- AC-15F.1：`src/cli/cmd-config.ts` 实现 `sevo config --level <basic|advanced|expert>` 子命令，按级别显示/编辑配置项：
  - `basic`（对应 L0-L1）：显示路由阈值、门禁严格度、通知渠道、发布目标。
  - `advanced`（对应 L2）：显示自定义阶段、自定义门禁规则、阶段顺序。
  - `expert`（对应 L3）：显示 API/SDK 配置、自定义 Adapter、自定义执行器。
- AC-15F.2：`sevo config` 不带 `--level` 参数时默认显示 `basic` 级别，附带提示 `"使用 --level advanced|expert 查看更多配置项"`。
- AC-15F.3：`src/progressive-disclosure/index.ts` 导出 `getDefaultConfig(): SevoConfig` 函数，返回所有配置项的零配置默认值，每个字段附带 JSDoc 注释说明用途和合法值范围。
- AC-15F.4：`sevo config --show-defaults` 输出所有配置项的默认值（JSON 格式），用户可据此了解零配置状态下的行为。
- AC-15F.5：`sevo config set <key> <value>` 在设置前校验 key 是否属于当前 level 可见范围，设置高级配置项时输出警告提示。

---

### FR-16-FIX: Demo 项目自动推进到 Spec 阶段产出

**缺口**：`sevo demo` 当前仅展示 pipeline 阶段流转结构（dry-run 模式）或启动 pipeline 但未验证能自动推进到 Spec 阶段并产出有意义的 spec 工件。5 分钟内看到结果的承诺未被验证。

**验收标准**：

- AC-16F.1：`src/cli/cmd-demo.ts` 中 `sevo demo`（非 dry-run 模式）在有 LLM 环境中执行时，自动推进内置示例项目的 pipeline 到 Specify 阶段完成，产出 `demo-project/specs/product-requirements.md` 文件。
- AC-16F.2：demo pipeline 的 Specify 阶段使用内置的示例需求描述（硬编码在 `src/cli/demo-fixtures/` 中），不依赖用户输入。
- AC-16F.3：`sevo demo` 执行完成后输出包含：pipeline 经过的阶段列表、每个阶段耗时、产出的工件路径列表、总耗时。
- AC-16F.4：`sevo demo` 总耗时超过 5 分钟时，输出警告 `"Demo 耗时超过预期（${elapsed}s），可能是 LLM 响应慢或网络问题"` 并附带排查建议。
- AC-16F.5：`sevo demo --dry-run` 产出的示例工件结构包含完整的目录树（specs/、contract/、reports/），每个目录下有 mock 文件（非空，包含示例内容），让用户理解 pipeline 各阶段的产出物。
- AC-16F.6：`src/cli/__tests__/cli-demo.test.ts` 新增集成测试：验证 dry-run 模式产出完整目录结构和 mock 文件、验证非 dry-run 模式（mock LLM）能推进到 Specify 完成。

---

## P2 — 体验优化

### FR-13-FIX: PipelineEngine 代码目录统一

**缺口**：项目中存在 `src/pipeline/pipeline-engine.ts` 和 `src/pipeline-engine/pipeline-engine.ts` 两个目录残留，导致 import 路径混乱，新开发者不确定哪个是真正入口。

**验收标准**：

- AC-13F.1：项目中只保留一个 PipelineEngine 入口目录。统一为 `src/pipeline-engine/` 作为唯一入口（或 `src/pipeline/`，取决于当前主要引用路径），另一个目录完全删除。
- AC-13F.2：`src/index.ts`（或包的 main exports）中 PipelineEngine 的 re-export 路径指向唯一入口，无歧义。
- AC-13F.3：全项目 `grep -r "pipeline/pipeline-engine\|pipeline-engine/pipeline-engine"` 结果中，所有 import 路径统一指向同一个目录，无残留的旧路径引用。
- AC-13F.4：`npm run build`（tsc 编译）零错误通过，确认路径统一后无断裂引用。
- AC-13F.5：删除的目录不残留在 git 工作区中（`git status` 无 untracked 残留）。

---

### FR-08a-FIX: 商用化门禁检查清单扩展

**缺口**：FR-08a 第一层「代码清洁度」的检查项在实现中覆盖不完整。缺少：文档完整性的细粒度检查、错误处理覆盖率验证、配置外部化验证、`console.log` 残留扫描、`TODO/FIXME` 残留扫描。

**验收标准**：

- AC-08aF.1：商用化门禁的第一层检查（代码清洁度）实现中，新增以下扫描器（在 `src/gate/` 或 `src/commercialization/` 目录下）：
  - `console-log-scanner`：扫描 `src/**/*.ts` 中的 `console.log`/`console.debug`/`console.warn`（排除测试文件和明确标注为生产日志的调用），发现则报告为 FAIL 并列出文件:行号。
  - `todo-fixme-scanner`：扫描 `src/**/*.ts` 中的 `TODO`/`FIXME`/`HACK`/`XXX` 注释，发现则报告为 FAIL 并列出文件:行号:内容。
  - `config-externalization-checker`：检查源码中是否存在硬编码的配置值（通过模式匹配：硬编码端口号、硬编码 URL、硬编码文件路径），发现则报告为 WARNING 并建议外部化。
- AC-08aF.2：商用化门禁的第三层检查（文档质量）实现中，新增细粒度检查：
  - 每个导出的公共 API 函数/类在 README 或 API 文档中有对应说明。
  - `CHANGELOG.md` 存在且最新版本条目非空。
  - 配置项文档（环境变量列表、配置文件模板）存在且与代码中实际使用的配置项一致。
- AC-08aF.3：商用化门禁新增第六层「错误处理覆盖」检查：
  - 扫描所有 async 函数，验证存在 try-catch 或 `.catch()` 错误处理（或调用链上游有统一错误处理）。
  - 扫描所有对外 API 入口（CLI command handler、hook handler），验证有顶层错误捕获且错误信息对用户友好（非 raw stack trace）。
  - 覆盖率低于 80% 时报告为 WARNING，低于 50% 时报告为 FAIL。
- AC-08aF.4：每个新增扫描器独立为一个函数/类，接受 `projectRoot: string` 参数，返回 `{ status: 'pass' | 'fail' | 'warning'; items: Array<{ file: string; line: number; message: string }> }`。
- AC-08aF.5：`sevo scan --commercialization` 命令触发完整商用化门禁检查（含新增项），输出结构化 JSON 报告。
