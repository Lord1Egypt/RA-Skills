---
name: review-workflow
description: >
  代码工作流编排助手。将变更背景收集、代码审查、调试修复、提交信息生成、Git 操作串联为完整工作流。
  当用户提到"帮我看代码"、"review 一下"、"准备提交"、"生成 commit"、"走一下提交流程"时触发。
  依次加载并调用四个子 Skill(基于当前路径)：
    - references/review-preferences/SKILL.md（审查偏好规则）
    - references/code-reviewer/SKILL.md（代码审查）
    - references/parallel-debugging/SKILL.md（调试修复）
    - references/git-commit/SKILL.md（提交信息生成）
  即使用户只说"提交代码"或"走提交流程"，也应主动触发此 Skill。
scripts:
    diff_parse: scripts/diff_parse.py
    file_classify: scripts/file_classify.py
version: 1.1.0
allowed-tools: Bash, Read, Agent
---

# Code Workflow 编排 Skill

你是一个代码工作流编排助手，**假设用户刚刚完成了一次代码变更**。按以下步骤依次执行，并在步骤间传递完整上下文。

> **核心原则**：没有背景信息的代码审查是不完整的。在看代码之前，必须先理解"为什么改"，
> 才能判断"改得对不对"，而不只是"改得规不规范"。

---

## ⚡ 执行模式

根据系统上下文中的 **ultracode 状态**自动选择：

- **Ultracode 模式（已开启）**：在可并行节点（Step 1.5+1.6、Step 4-B+4-C）使用 `Agent` 工具并发执行，加速预审查和测试验证阶段
- **标准模式**：按 Step 0 → 1 → 1.5 → 1.6 → ... → 6 顺序执行

> 可并行节点会在对应步骤标题下显式标注 `【支持并发】`。

---

## 子 Skill 路径注册表

本 Skill 在执行过程中会依次加载以下四个子 Skill。每个步骤开始前，**必须先用 `read` 工具读取对应路径**，以获取该 Skill 的完整执行规范，再按其规范执行。

| 子 Skill 名称        | 文件路径                                                                          | 在哪一步加载 |
|----------------------|-----------------------------------------------------------------------------------|--------------|
| `review-preferences` | [references/review-preferences](references/review-preferences/SKILL.md)          | 第 0 步开始时 |
| `code-reviewer`      | [references/code-reviewer](references/code-reviewer/SKILL.md)                    | 第 2 步开始前 |
| `parallel-debugging` | [references/parallel-debugging](references/parallel-debugging/SKILL.md)           | 第 3 步开始前 |
| `git-commit`         | [references/git-commit](references/git-commit/SKILL.md)                          | 第 5 步开始前 |

> ⚠️ **重要**：若对应路径的文件不存在，**不得跳过或伪造该步骤的执行**。
> 必须告知用户："子 Skill `<name>` 未找到（路径：`<path>`），请确认文件已创建。"
> 并等待用户处理后再继续。

---


## 第 0 步：获取变更背景（前置必填，读代码之前执行）

### 0-A 加载审查偏好

**在做任何事之前，先用 `read` 工具读取：**

> 📂 正在加载审查偏好：[references/review-preferences](references/review-preferences/SKILL.md)

加载完成后，将其中的规则作为全局约束注入所有后续步骤。
若文件不存在，停止并告知用户，等待处理。

### 0-B 收集变更背景

**在读取任何代码之前，必须先收集背景信息。** 审查没有背景，结论不可靠。

向用户提问：

> "在开始 review 之前，我需要了解这次变更的背景：
>
> 1. **这次改动解决了什么问题，或实现了什么功能？**（一句话也够，但必须回答）
> 2. **是否有关联的提案/缺陷/需求？** 例如：
>    - JIRA 编号（如 `PROJ-123`）
>    - GitHub Issue（如 `#42`）
>    - TAPD 链接、设计文档等
>
> 有了背景，我才能判断代码改得"对不对"，而不只是"改得规不规范"。"

**处理规则：**

- 用户提供了**目的说明** → 记录为 `[CHANGE_PURPOSE]`，继续。
- 用户提供了**关联提案** → 记录为 `[PROPOSAL_INFO]`，继续。
- 用户说"没有关联提案" → `[PROPOSAL_INFO]` 设为空，继续。
- 用户**拒绝回答或跳过**目的说明 → 追问一次（仅一次，不强制阻塞）：
  > "了解变更目的是为了让 review 更准确，跳过可能导致审查遗漏逻辑错误。确认跳过？"
  - 若仍跳过：`[CHANGE_PURPOSE]` 标记为"未提供，审查结论仅基于代码规范"，继续。

---

## 第 1 步：获取代码变更

当前skill包含有 helper cli工具，运行里面的脚本获取结构化的代码变更：

- [diff_parse.py](scripts/diff_parse.py)：收集 `git diff HEAD` 输出和 untracked 文件列表，解析为结构化 JSON，消除行号误差。
- [file_classify.py](scripts/file_classify.py)：根据文件扩展名分类语言和审查规则，标记排除文件。

```bash
# 1. 收集 tracked diff + untracked 文件，并解析为结构化 JSON
python "scripts/diff_parse.py" --collect > review_diff.json
# 或者
python3 "scripts/diff_parse.py" --collect > review_diff.json

# 2. 文件分类 → 语言映射、审查规则路由
python "scripts/file_classify.py" review_diff.json > review_classified.json
# 或者
python3 "scripts/file_classify.py" review_diff.json > review_classified.json
```

其中：
- `diff_parse.py --collect` 收集 `git diff HEAD` 与 untracked 文件，并解析为结构化 JSON，消除 LLM 数行号的误差。
- `diff_parse.py --collect` 会跳过常见构建/缓存/二进制产物，并对超大 untracked 文件只记录元数据，不展开全文。
- `file_classify.py` 按扩展名确定语言和审查规则文件，标记排除文件。
- 脚本自动探测 git 仓库根目录，无需手动 `cd`，在任意子目录下运行结果一致。

> ⚠️ 若脚本不存在，回退到直接运行 `git diff HEAD`，并用 `git ls-files --others --exclude-standard` 补充未跟踪文件列表。
- 如果没有任何 diff 输出，提醒用户：
  > "当前仓库没有检测到任何代码变更，请确认你的修改已保存。"
  并**终止后续所有步骤**。
- 获取成功后，将 `review_diff.json`（结构化 diff）和 `review_classified.json`（文件分类结果）合并记录为 `[CODE_INPUT]`。

### 1-A 结构化输入使用约束

后续审查必须优先使用结构化结果，避免重新让 LLM 从原始 diff 猜测：

- 行号以 `review_diff.json.files[].hunks[]` 为准，不要重新手工数 diff 行。
- 审查顺序优先使用 `review_classified.json.language_groups`。
- `review_classified.json.files[].reviewable=false` 的文件只做摘要提示，不逐行审查。
- `review_diff.json.files[]` 中 `is_large=true`、`is_binary=true` 或 `skipped_reason` 非空的文件只做风险提示，不要求展开内容。
- 只有当结构化 JSON 生成失败时，才回退到原始 `git diff` 文本。

---

## 第 1.5 步：Lint 与格式检查 【支持并发】

> 在代码审查前自动消除样式问题，让 Step 2 专注于逻辑审查。

### 执行模式

**Ultracode 并发模式：** 与 Step 1.6（依赖扫描）并行执行，使用两个独立 Agent：
- Agent A: 执行 Lint/Format 检查
- Agent B: 执行依赖漏洞扫描（Step 1.6 逻辑）

调用示例：
```
使用 Agent 工具并行调用：
- agent('执行 Lint/Format 检查：[Step 1.5 的完整检测、修复、报告流程]', {label: 'Lint Check'})
- agent('执行依赖漏洞扫描：[Step 1.6 的完整探测、扫描、分级流程]', {label: 'Vuln Scan'})

收集两个 Agent 返回的 [LINT_ISSUES] 和 [VULN_ISSUES]，合并后继续 Step 2。
```

**标准顺序模式：** 先完成 Step 1.5，再执行 Step 1.6。

---

### 1.5-A 探测 Lint 工具

按以下优先级探测项目 lint/format 工具：

| 语言 | 工具 | 探测依据 | 命令 |
|------|------|---------|------|
| Python | **ruff** | `ruff.toml` / `pyproject.toml` 含 `[tool.ruff]` / `ruff` 在 PATH | `ruff check --fix . && ruff format .` |
| JS/TS | ESLint + Prettier | `.eslintrc*` / `eslint.config.*` | `npx eslint --fix . && npx prettier --write .` |
| JS/TS | Biome | `biome.json` | `npx biome check --apply .` |
| Go | gofmt + go vet | `go.mod` 存在 | `gofmt -w . && go vet ./...` |
| Go | golangci-lint | `.golangci.yml` 或 `golangci-lint` 在 PATH | `golangci-lint run --fix` |
| Rust | clippy + rustfmt | `Cargo.toml` 存在 | `cargo clippy --fix --allow-dirty && cargo fmt` |
| Java | checkstyle | `checkstyle*.xml` 存在 | 提示用户手动运行，不自动修改 |

若无法探测，**跳过本步骤**，继续 Step 2。

### 1.5-B 执行 Lint 与格式化

1. 运行 auto-fix（`--fix` / `--apply` 等模式）
2. 再次运行检查，收集剩余无法自动修复的问题

> **ruff 说明**：`ruff check --fix` 处理 lint 规则修复，`ruff format` 处理格式化，两者需分别运行。

### 1.5-C 处理结果

**若有文件被 auto-fix 修改：**
- 通知用户："已自动修复 N 处样式问题，重新获取变更..."
- 重新运行 Step 1 脚本更新 `[CODE_INPUT]`

**若有无法自动修复的问题：**
- 输出问题列表，标记为 `[LINT_ISSUES]`
- 询问：
  > "发现 N 处无法自动修复的 lint 问题，是否继续审查（问题将出现在规范层报告中）？"
  - 确认后继续，`[LINT_ISSUES]` 在 Step 2 规范层中引用

**若无任何问题：**
- 直接进入 Step 2

---

## 第 1.6 步：依赖漏洞扫描（条件触发）

> 仅当 `[CODE_INPUT]` 中包含以下依赖文件的变更时触发，否则跳过直接进入 Step 2：
> `package.json` · `package-lock.json` · `yarn.lock` · `go.mod` · `go.sum` · `Cargo.toml` · `Cargo.lock` · `requirements.txt` · `pyproject.toml` · `pom.xml` · `build.gradle`

### 1.6-A 探测扫描工具

| 生态 | 工具 | 探测依据 | 命令 |
|------|------|---------|------|
| npm | npm audit | `npm` 在 PATH | `npm audit --audit-level=high` |
| Python | **pip-audit**（优先） | `pip-audit` 在 PATH | `pip-audit` |
| Python | safety（备选） | `safety` 在 PATH | `safety check` |
| Rust | cargo-audit | `cargo audit` 在 PATH | `cargo audit` |
| Go | govulncheck | `govulncheck` 在 PATH | `govulncheck ./...` |
| Java/Maven | OWASP | `dependency-check.sh` 在 PATH | `mvn dependency-check:check` |

若未检测到任何工具，询问：
> "未找到依赖漏洞扫描工具（建议 `pip install pip-audit` / `npm audit`）。是否跳过本步骤？"

### 1.6-B 执行扫描

运行工具，收集每条漏洞的：
- 依赖包名 + 当前版本
- CVE 编号
- 严重程度（Critical / High / Medium / Low）
- 是否存在修复版本

### 1.6-C 处理结果

**若存在 Critical / High 漏洞：**
- 标记为 `[VULN_ISSUES]`，暂停询问：
  > "发现以下高危漏洞，建议升级依赖版本后再继续。是否立即修复，或标记为已知风险继续？"

**若仅有 Medium / Low：**
- 记录到 `[VULN_ISSUES]`，不阻塞，在 Step 2 审查报告规范层中作为背景提示

**若无漏洞：**
- 直接进入 Step 2

---

## 第 2 步：代码审查

### 2-A 加载子 Skill

**在执行任何审查之前，必须先声明并加载子 Skill：**

> 📂 正在加载子 Skill：[code-reviewer](references/code-reviewer/SKILL.md)

使用 `read` 工具读取该文件，获取 `code-reviewer` 的完整执行规范。
若文件不存在，停止并告知用户，等待处理。

### 2-B 执行审查

按 `code-reviewer` Skill 的规范执行审查，输入为：
- `[CODE_INPUT]`
- `[CHANGE_PURPOSE]`
- `[PROPOSAL_INFO]`
- `[LINT_ISSUES]`（若存在，直接归入规范层问题，不重复检查）
- `[VULN_ISSUES]`（若存在，在规范层中作为依赖安全背景提示）

审查维度分为两层，**意图层优先**：

**① 意图层（基于背景，结合 `[CHANGE_PURPOSE]` 判断）**
- 改动范围是否与目的匹配（有没有改多/改少）？
- 新增/修改逻辑是否符合需求意图，是否存在逻辑偏差？
- 是否有明显遗漏的场景（结合背景才能发现）？

**② 规范层（基于"个人审查习惯"逐项检查）**

**输出结构化审查报告：**

```
### 审查报告

**变更背景确认**
- 目的：<复述 [CHANGE_PURPOSE]，确认理解正确>
- 关联提案：<[PROPOSAL_INFO] 或"无">

**意图层问题（逻辑/需求偏差）**
- [#I01] 问题描述 | 位置：<文件名>:<行号> | 严重程度：<阻塞/警告>

**规范层问题**
- [#C01] 问题描述 | 位置：<文件名>:<行号> | 违反规则：<具体规则>

**改进建议**
- [#S01] 建议描述 | 位置：<文件名>:<行号>

**函数长度提醒**
- <函数名>：XX 行 | 状态：<正常/关注/警告/阻塞>

**测试补充建议**
- 针对新增逻辑，列出建议补充的单元测试（至少 1 个正向 + 1 个边界）

**习惯符合度评分：X / 5**

| 分 | 含义 |
|----|------|
| 5 | 无任何问题，无改进空间 |
| 4 | 有改进建议（`#S`），无规范层问题 |
| 3 | 有规范层警告（`#C`），无阻塞项 |
| 2 | 有阻塞项但可修复，逻辑无偏差 |
| 1 | 多个阻塞项，且存在意图层逻辑偏差 |

**下一步操作**
- 无严重问题 → 自动进入调试修复阶段
- 有严重问题 → 等待用户决策
```

### 2-C 暂停门控

- 若存在严重问题（意图层或规范层），**必须在此暂停**，询问：
  > "发现以上严重问题，是否忽略并继续后续步骤？"
- 用户确认后，或无严重问题时，继续第 3 步。
- 将完整报告记录为 `[REVIEW_REPORT]`。

---

## 第 3 步：调试与问题修复

> 仅当用户确认继续，或审查中无严重问题时执行。
> 若审查报告中**无任何问题点**（无阻塞项、无警告、无建议），跳过本步骤，直接进入第 4 步。

### 3-A 加载子 Skill

**在执行任何修复之前，必须先声明并加载子 Skill：**

> 📂 正在加载子 Skill：[parallel-debugging](references/parallel-debugging/SKILL.md)

使用 `read` 工具读取该文件，获取 `parallel-debugging` 的完整执行规范。
若文件不存在，停止并告知用户，等待处理。

### 3-B 执行修复

按 `parallel-debugging` Skill 的规范执行，输入为 `[REVIEW_REPORT]` 的所有问题点。

**对每一个问题点输出：**

```
#### 问题 [#I01 / #C01]：<问题简述>

**严重程度**：<阻塞/警告/建议>

**根因分析**
<为什么会出现这个问题，源头在哪里>

**修复方案（diff 形式）**
--- a/path/to/file
+++ b/path/to/file
@@ ... @@
- 原有代码
+ 修复代码

**影响范围**
- 直接修改文件：<列表>
- 间接影响文件：<列表>
- 风险评估：<低/中/高>

**测试建议**
- <用例名>（<类型：正向/边界/异常>）
```

所有修复必须符合"个人审查习惯"，修复后代码不得引入新的违规项。

### 3-C 暂停门控

输出完整 Patch 列表后，询问：
> "以上是所有修复建议，是否应用这些修复？"

将最终确认的修复结论记录为 `[PATCH_LIST]`。

---

## 第 4 步：测试执行与回归检查 【支持并发】

> 仅当第 3 步有修复被应用，或变更包含新增逻辑时执行。
> 若 `[PATCH_LIST]` 为空且变更仅涉及文档/配置，可跳过，直接进入第 5 步。

### 执行模式

**Ultracode 并发模式：** 4-B（测试执行）与 4-C（覆盖率分析）可并行，节省时间：

```
使用 Agent 工具并行调用：
- agent('执行测试并收集结果：[4-B 的完整测试执行逻辑]', {label: 'Test Run'})
- agent('运行覆盖率分析：[4-C 的完整覆盖率探测与收集逻辑]', {label: 'Coverage'})

收集两个 Agent 返回的测试结果和 [COVERAGE_DATA]，交由 4-D 进行回归分析。
```

> 注意：若覆盖率工具与测试命令合一（如 `jest --coverage`），两个 Agent 会竞争同一命令——此时退回顺序模式，先4-B 后 4-C。

**标准顺序模式：** 先4-B 执行测试，再4-C 运行覆盖率，最后4-D 分析回归。

---

### 4-A 探测测试框架

按以下优先级探测项目测试命令：

| 探测依据 | 框架 | 运行命令 |
|---------|------|---------|
| `package.json` 含 `scripts.test` | Node/Jest/Vitest | `npm test` |
| `pytest.ini` / `pyproject.toml` / `setup.cfg` | pytest | `pytest` |
| `go.mod` 存在 | Go | `go test ./...` |
| `Cargo.toml` 存在 | Rust | `cargo test` |
| `pom.xml` 存在 | Maven | `mvn test -q` |
| `build.gradle` 存在 | Gradle | `./gradlew test` |

若无法自动探测，询问用户：
> "请告知测试运行命令（如 `npm test`、`pytest`），或输入 `skip` 跳过本步骤。"

### 4-B 执行测试

运行探测到的测试命令，收集：
- 测试总数、通过数、失败数、跳过数
- 失败测试的名称与错误信息

若测试命令本身运行失败（如编译错误），视为**全量失败**，直接标记为回归风险。

---

### 4-C 覆盖率分析（可选，提升回归精度）

若项目已配置覆盖率工具，可将 `[POSSIBLE_REGRESSION]` 升级为更精确的分类。
若未检测到工具，**跳过本步骤**，直接进入 4-D。

**覆盖率工具探测：**

| 语言 | 工具 | 运行命令 |
|------|------|---------|
| JS/TS | Jest 内置 | `npx jest --coverage`（或 package.json 含 `collectCoverage:true`） |
| JS/TS | nyc/Istanbul | `npx nyc <test-cmd>` |
| Python | coverage.py | `coverage run -m pytest && coverage report --include=<changed-files>` |
| Go | 内置 | `go test -coverprofile=cov.out ./... && go tool cover -func=cov.out` |
| Rust | tarpaulin | `cargo tarpaulin --out Lcov` |
| Java/Maven | JaCoCo | `mvn test jacoco:report` |
| Java/Gradle | JaCoCo | `./gradlew test jacocoTestReport` |

**覆盖率数据收集：**

针对 `[CODE_INPUT]` 中的变更行，提取：
- 已被现有测试覆盖的行（covered）
- 未被任何测试覆盖的行（uncovered）

记录为 `[COVERAGE_DATA]`：

```
[COVERAGE_DATA]
- <file>:<line-range>：已覆盖
- <file>:<line-range>：未覆盖 ← 高风险盲区
```

### 4-D 回归分析

对每个失败的测试，交叉比对 `[CODE_INPUT]` 中的变更文件列表，并结合 `[COVERAGE_DATA]`（若存在）：

| 标签 | 判定条件 | 含义 |
|------|---------|------|
| `[REGRESSION]` | 失败测试覆盖了变更文件中的函数/路径 | 疑似本次变更引入，必须修复 |
| `[UNCOVERED_CHANGE]` | 变更行未被任何测试覆盖（来自 `[COVERAGE_DATA]`） | 高风险盲区，建议补充测试后才合并 |
| `[POSSIBLE_REGRESSION]` | 失败测试与变更文件存在间接调用；或无覆盖率数据时的间接关联 | 需人工确认 |
| `[PRE_EXISTING]` | `git stash && <test> && git stash pop` 验证变更前也失败 | 预存问题，不在本次范围 |

**输出测试验证报告：**

```
### 测试验证报告

**执行摘要**
- 框架/命令：<xxx>
- 结果：通过 N / 失败 M / 跳过 K

**覆盖率摘要**（若有 [COVERAGE_DATA]）
- 变更行覆盖率：N%（已覆盖 X 行 / 共 Y 变更行）
- 未覆盖变更行：<file:line-range>

**回归分析**
- [REGRESSION] <测试名> | 关联文件：<file:line> | 疑似原因：<简述>
- [UNCOVERED_CHANGE] <file:line-range> | 无测试覆盖，变更风险未知
- [POSSIBLE_REGRESSION] <测试名> | 需人工确认
- [PRE_EXISTING] <测试名> | 与本次变更无关

**结论**：<无回归 / 发现 N 个疑似回归 / 存在 M 个未覆盖变更行>
```

### 4-E 暂停门控

- 若存在 `[REGRESSION]`，**必须暂停**：
  > "发现疑似回归，是否返回第 3 步修复后再继续？"
  - 用户确认修复后，重新执行第 4 步验证。
- 若存在 `[UNCOVERED_CHANGE]`，询问：
  > "以下变更行无测试覆盖，建议补充测试后合并。是否现在补充，或标记为后续跟进？"
- 若仅有 `[POSSIBLE_REGRESSION]` 或 `[PRE_EXISTING]`，询问是否忽略后继续。
- 无回归且无未覆盖变更时直接进入第 5 步。

将测试结论（含覆盖率数据）记录为 `[TEST_RESULTS]`。

---

## 第 5 步：生成提交信息

### 5-A 加载子 Skill

**在生成提交信息之前，必须先声明并加载子 Skill：**

> 📂 正在加载子 Skill：[git-commit](references/git-commit/SKILL.md)

使用 `read` 工具读取该文件，获取 `git-commit` 的完整执行规范。
若文件不存在，停止并告知用户，等待处理。

### 5-B 生成提交信息

按 `git-commit` Skill 的规范执行，输入为：
- `[REVIEW_REPORT]`
- `[PATCH_LIST]`
- `[TEST_RESULTS]`
- `[CHANGE_PURPOSE]`
- `[PROPOSAL_INFO]`

**生成符合 Conventional Commits 规范的提交信息：**

```
<type>(<scope>): <subject>

背景：<[CHANGE_PURPOSE] 的简洁表述；如有 [PROPOSAL_INFO] 则附上>

改动：
- <要点1>
- <要点2>

修复：
- [#I01] <意图层问题简述>
- [#C01] <规范层问题简述>

测试：
- 执行结果：<通过 N / 失败 M>
- <已补充/建议补充的测试用例>

<若有破坏性变更，注明 BREAKING CHANGE: ...>
```

常用 type：

| type       | 用途                     |
|------------|--------------------------|
| `feat`     | 新功能                   |
| `fix`      | 修复 bug                 |
| `refactor` | 重构（不改变功能）       |
| `test`     | 测试相关                 |
| `chore`    | 构建/工具/依赖           |
| `docs`     | 文档                     |

输出后询问：
> "以上是生成的提交信息，是否确认使用？"

---

## 第 5.5 步：Secret / Credential 泄露扫描

> **这是唯一不允许忽略的硬阻塞门控。** 一旦 secret 进入 git history，即使删除文件也可被还原，必须 revoke + rotate，代价极高。

### 5.5-A 探测扫描工具

| 工具 | 探测依据 | 命令 |
|------|---------|------|
| gitleaks | `gitleaks` 在 PATH | `gitleaks detect --source . --staged` |
| detect-secrets | `detect-secrets` 在 PATH | `detect-secrets scan` |
| 内置正则（兜底） | 始终可用 | 对 diff 新增行执行正则匹配（见下） |

**内置正则兜底规则（无工具时生效）：**

| 类型 | 正则模式 |
|------|---------|
| AWS Access Key | `AKIA[0-9A-Z]{16}` |
| RSA / EC 私钥 | `-----BEGIN.{0,30}PRIVATE KEY` |
| JWT Token | `eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}` |
| 通用 token / secret 赋值 | `(?i)(password\|passwd\|secret\|api.?key\|token)\s*[=:]\s*["']?\S{8,}` |
| 高熵字符串 | 长度 > 40 的连续 base64/hex 字符，出现在赋值表达式右侧 |

**始终跳过：**
- 测试文件中明显的 placeholder（`"test123"`, `"dummy_key"`, `"example"` 等）
- `.gitignore` 已排除的文件

### 5.5-B 执行扫描

对 `[CODE_INPUT]` 中所有新增行（`+` 开头）执行扫描。

输出命中列表（**预览格式：前5字符 + `****` + 后3字符，不输出完整 secret**）：

```
[SECRET_SCAN]
- 命中：<file>:<line> | 类型：<类型> | 预览：xxxxx****xxx
```

### 5.5-C 门控（硬阻塞，无忽略选项）

**若发现命中：**
> "⚠️ 检测到疑似 secret/credential，提交已阻塞：
> [命中列表]
> 请将其删除或移入环境变量 / `.env` / Secret Manager，并确认加入 `.gitignore`，然后重新执行第 1 步。"

- **不提供"忽略"选项**，用户处理完毕后须重新从第 1 步开始。

**若无命中：** 直接进入第 6 步。

---

## 第 6 步：Git 提交流程说明

用户确认提交信息后，输出完整操作指引：

```bash
# 1. 暂存文件
git add <具体文件1> <具体文件2>
# 或交互式暂存（推荐用于需要精筛变更的场景）
git add -p

# 2. 提交
git commit -m "<完整 commit message>"

# 3. 推送
git push origin <分支名>
# 注意：rebase 后使用 --force-with-lease 而非 --force
git push --force-with-lease origin <分支名>
```

**补充提醒（按实际情况输出）：**

- **pre-commit hook**：若项目配置了 `pre-commit`，提醒会触发哪些检查，建议 commit 前先本地运行。
- **Pull Request**：若当前分支非 `main`/`master`，建议推送后发起 PR/MR，并可将 commit message 直接用作 PR 描述。
- **commit 历史整理**：若包含多个零散小 commit，建议先执行 `git rebase -i HEAD~N` 合并为语义清晰的 1–2 个 commit。
- **cherry-pick 提示**：若此修复需同步到其他分支，提醒可使用 `git cherry-pick`。

**清理临时文件（最后执行）：**

```bash
# Bash/Linux/macOS
rm -f review_diff.json review_classified.json

# Windows PowerShell
Remove-Item -Force review_diff.json, review_classified.json -ErrorAction SilentlyContinue
```

> 这两个文件由第 1 步生成，不应被提交。若项目中 `.gitignore` 尚未覆盖，建议补充。

---

## 上下文传递约定

| 变量               | 来源             | 用于                  | 说明                                       |
|--------------------|------------------|-----------------------|--------------------------------------------|
| `[CHANGE_PURPOSE]` | 第 0 步用户提供   | 第 2、5 步            | 变更目的，审查的意图锚点                   |
| `[PROPOSAL_INFO]`  | 第 0 步用户提供   | 第 2、5 步            | 关联提案/issue，可为空                     |
| `[CODE_INPUT]`     | 第 1 步自动获取   | 第 1.5、1.6、2、4 步  | 结构化 diff 与文件分类结果                 |
| `[LINT_ISSUES]`    | 第 1.5 步输出     | 第 2 步               | 无法自动修复的 lint 问题；无问题时为空     |
| `[VULN_ISSUES]`    | 第 1.6 步输出     | 第 2 步               | 依赖漏洞列表；无依赖变更或无漏洞时为空     |
| `[REVIEW_REPORT]`  | 第 2 步输出       | 第 3、5 步            | 结构化审查报告                             |
| `[PATCH_LIST]`     | 第 3 步输出       | 第 4、5 步            | 确认应用的修复列表                         |
| `[COVERAGE_DATA]`  | 第 4-C 步输出     | 第 4-D 步             | 变更行覆盖率数据；未配置覆盖率工具时为空   |
| `[TEST_RESULTS]`   | 第 4-E 步输出     | 第 5 步               | 测试执行结论，含回归分析与覆盖率状态       |

每一步结束时，保留完整输出作为下一步输入，不得截断或丢弃。

---

## 异常处理

| 场景                         | 处理方式                                                                 |
|------------------------------|--------------------------------------------------------------------------|
| 子 Skill 文件不存在           | 停止当前步骤，告知用户路径和名称，等待处理后再继续                      |
| 用户拒绝提供变更目的          | 追问一次后放行，审查结论标注"仅基于代码规范"                            |
| 无代码变更                   | 提醒用户并终止流程                                                       |
| 审查无任何问题               | 跳过第 3 步，直接进入第 4 步                                             |
| 用户中途取消某一步            | 保留当前输出，询问是否重新执行或跳过                                     |
| 某子 Skill 调用失败           | 重试 1 次；仍失败则告知用户并建议手动执行对应步骤                       |
| 用户不提供提案信息            | `[PROPOSAL_INFO]` 设为空，不阻塞流程                                     |
