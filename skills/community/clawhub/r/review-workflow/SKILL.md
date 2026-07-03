---
name: review-workflow
description: >
  代码工作流编排助手。将变更背景收集、代码审查、调试修复、提交信息生成、Git 操作串联为完整工作流。
  当用户提到"帮我看代码"、"review 一下"、"准备提交"、"生成 commit"、"走一下提交流程"时触发。
  依次加载并调用三个子 Skill(基于当前路径)：
    - references/code-reviewer/SKILL.md（代码审查）
    - references/parallel-debugging/SKILL.md（调试修复）
    - references/git-commit/SKILL.md（提交信息生成）
  即使用户只说"提交代码"或"走提交流程"，也应主动触发此 Skill。
scripts:
    diff_parse: scripts/diff_parse.py
    file_classify: scripts/file_classify.py
version: 1.0.1
allowed-tools: Bash, Read
---

# Code Workflow 编排 Skill

你是一个代码工作流编排助手，**假设用户刚刚完成了一次代码变更**。按以下步骤依次执行，并在步骤间传递完整上下文。

> **核心原则**：没有背景信息的代码审查是不完整的。在看代码之前，必须先理解"为什么改"，
> 才能判断"改得对不对"，而不只是"改得规不规范"。

---

## 子 Skill 路径注册表

本 Skill 在执行过程中会依次加载以下三个子 Skill。每个步骤开始前，**必须先用 `read` 工具读取对应路径**，以获取该 Skill 的完整执行规范，再按其规范执行。

| 子 Skill 名称    | 文件路径                                          | 在哪一步加载 |
|------------------|---------------------------------------------------|--------------|
| `code-reviewer`  | [references/code-reviewer](references/code-reviewer/SKILL.md)         | 第 2 步开始前 |
| `parallel-debugging` | [references/parallel-debugging](references/parallel-debugging/SKILL.md)        | 第 3 步开始前 |
| `git-commit`     | [references/git-commit](references/git-commit/SKILL.md)            | 第 4 步开始前 |

> ⚠️ **重要**：若对应路径的文件不存在，**不得跳过或伪造该步骤的执行**。
> 必须告知用户："子 Skill `<name>` 未找到（路径：`<path>`），请确认文件已创建。"
> 并等待用户处理后再继续。

---

## 个人审查习惯（所有步骤必须遵守）

### 函数长度（分级提醒）

- **≤ 50 行**：正常，无需提示
- **50–80 行**：提醒审查者关注是否职责单一；若逻辑清晰、无深层嵌套则放过
- **80–150 行**：警告，建议拆分或重构，必须在 review 中给出理由
- **> 150 行**：阻塞项，必须拆分后才能合并

**豁免条件**：同时满足以下所有条件时，即使超过 80 行也不警告：
- 函数为纯数据处理/配置映射（如大 match/switch、路由表、配置字典）
- 无明显嵌套（缩进层级 ≤ 2）
- 无副作用（不修改外部状态、不发起 I/O）

### 代码质量底线

- 检查是否缺少边界条件和空值处理。
- 变量命名须清晰表达意图，**禁止使用单字母变量**（循环索引 `i`、`j`、`k` 除外）。
- 任何 `TODO` 或 `FIXME` 注释**必须标记为阻塞项**，要求附上修复计划或关联 issue。
- 新增逻辑必须建议补充单元测试。
- 禁止在循环内进行数据库查询或网络请求（性能硬伤）。

---

## 第 0 步：获取变更背景（前置必填，读代码之前执行）

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
（5 = 完全符合所有规则且无改进空间；1 = 存在多个严重问题）

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
> 若审查报告中**无任何问题点**，跳过本步骤，直接进入第 4 步。

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

## 第 4 步：生成提交信息

### 4-A 加载子 Skill

**在生成提交信息之前，必须先声明并加载子 Skill：**

> 📂 正在加载子 Skill：[git-commit](references/git-commit/SKILL.md)

使用 `read` 工具读取该文件，获取 `git-commit` 的完整执行规范。
若文件不存在，停止并告知用户，等待处理。

### 4-B 生成提交信息

按 `git-commit` Skill 的规范执行，输入为：
- `[REVIEW_REPORT]`
- `[PATCH_LIST]`
- `[CHANGE_PURPOSE]`
- `[PROPOSAL_INFO]`

**生成符合 Conventional Commits 规范的提交信息：**

```
<type>(<scope>): <subject>

## 背景说明
<[CHANGE_PURPOSE] 的简洁表述；如有 [PROPOSAL_INFO] 则附上>

## 修改内容
- <要点1>
- <要点2>

## 修复的问题
- [#I01] <意图层问题简述>
- [#C01] <规范层问题简述>

## 测试
- <已补充/建议补充的测试用例>

<若有破坏性变更，注明 BREAKING CHANGE>
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

## 第 5 步：Git 提交流程说明

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

---

## 上下文传递约定

| 变量               | 来源           | 用于         | 说明                                   |
|--------------------|----------------|--------------|----------------------------------------|
| `[CHANGE_PURPOSE]` | 第 0 步用户提供 | 第 2、4 步   | 变更目的，审查的意图锚点               |
| `[PROPOSAL_INFO]`  | 第 0 步用户提供 | 第 2、4 步   | 关联提案/issue，可为空                 |
| `[CODE_INPUT]`     | 第 1 步自动获取 | 第 2 步      | 结构化 diff 与文件分类结果             |
| `[REVIEW_REPORT]`  | 第 2 步输出     | 第 3、4 步   | 结构化审查报告                         |
| `[PATCH_LIST]`     | 第 3 步输出     | 第 4 步      | 确认应用的修复列表                     |

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
