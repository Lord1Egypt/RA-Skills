---
name: skill-creator-plus
description: "创建、编辑、优化或审查 OpenClaw AgentSkills 技能。当创建新技能或修改现有技能时触发。提供完整的工作流程指引：技能结构设计、frontmatter 规范、_meta.json 格式、ClawHub scanner 规则、渐进式披露设计、validation checklist 及发布流程。输出：SKILL.md + _meta.json。"
metadata: {"openclaw":{"emoji":"🛠️","requires":{"anyBins":[]}}}}
---

# skill-creator-plus

创建符合 ClawHub 规范的 OpenClaw 技能。按以下规则执行，不要跳过章节，不要发明规范中未列出的约定。

未提供技能名和用途时，先询问用户。

---

## 关于 Skills

Skills 是模块化、自包含的包，通过提供专业化的工作流程、工具和知识来扩展 OpenClaw 的能力。可以把 Skill 看作特定领域或任务的"入职指南"——它们将 OpenClaw 从通用 agent 转变为具备专门处理流程的 specialized agent，而这是任何模型都无法完全拥有的能力。

### Skills 能提供什么

1. **专业化工作流程** — 特定领域的多步骤流程
2. **工具集成** — 操作特定文件格式或 API 的指引
3. **领域专业知识** — 公司专属知识、Schema、业务逻辑
4. **打包资源** — 复杂重复任务的脚本、参考资料和资产文件

---

## 核心原则

### 简洁是关键

context window 是公共资源。Skills 与 OpenClaw 所需的其他内容共享 context window：system prompt、对话历史、其他 Skills 的元数据，以及实际的用户请求。

**默认假设：OpenClaw 已经非常聪明。** 只添加 OpenClaw 还没有的内容。每一条信息都要质疑："OpenClaw 真的需要这个解释吗？"以及"这个段落的 token 消耗值得吗？"

用简洁的例子替代冗长的解释。

### 设定适当的自由度

根据任务的脆弱性和可变性匹配具体的约束程度：

**高自由度（基于文本的指令）**：当多种方法都可行、决策依赖上下文或启发式方法引导方案时使用。

**中自由度（伪代码或带参数的脚本）**：当存在优选模式、可接受一定变化或配置影响行为时使用。

**低自由度（特定脚本，参数少）**：当操作脆弱易错、一致性至关重要或必须遵循特定顺序时使用。

可以把 OpenClaw 想象成在探索一条路径：狭窄的悬崖桥需要具体的护栏（低自由度），而开阔的场地允许多条路线（高自由度）。

---

## 文件结构

只生成两个文件——无 README.md、无 CHANGELOG.md、无辅助文档：

```
[skill-name]/
├── SKILL.md       (required)
└── _meta.json     (required)
```

### 技能的结构

每个技能由一个必需的 SKILL.md 文件和可选的打包资源组成：

```
skill-name/
├── SKILL.md（必需）
│   ├── YAML frontmatter 元数据（必需）
│   │   ├── name:（必需）
│   │   └── description:（必需）
│   └── Markdown 说明（必需）
└── 打包资源（可选）
    ├── scripts/      - 可执行代码（Python/Bash 等）
    ├── references/   - 文档，按需加载到 context 中
    └── assets/       - 输出中使用的文件（模板、图标、字体等）
```

#### SKILL.md（必需）

每个 SKILL.md 包含：

- **Frontmatter**（YAML）：包含 `name` 和 `description` 字段。这是 OpenClaw 判断技能何时被使用的唯一依据。
- **Body**（Markdown）：技能使用说明。**仅在技能触发后加载**（如果需要的话）。

#### 打包资源（可选）

**Scripts（`scripts/`）**：可执行代码，用于需要确定性可靠性或被反复重写的任务。优势：token 高效、确定性、可不加载到 context 中执行。

**References（`references/`）**：文档和参考资料，按需加载。优势：保持 SKILL.md 精简，仅在 OpenClaw 判定需要时加载。

**Assets（`assets/`）**：不打算加载到 context 中的文件，而是用于 OpenClaw 生成的输出中（模板、图片、样板代码等）。

#### 什么不应该包含

技能应只包含直接支持其功能的必要文件。**不要**创建：README.md、INSTALLATION_GUIDE.md、QUICK_REFERENCE.md、CHANGELOG.md 等。

---

## 渐进式披露设计原则

Skills 使用三级加载系统来高效管理 context：

1. **元数据（name + description）** — 始终在 context 中（约100词）
2. **SKILL.md 正文** — 技能触发时（<5000词）
3. **打包资源** — OpenClaw 按需加载（无限量）

保持 SKILL.md 正文简洁且在500行以内以减少 context 膨胀。内容接近此限制时分拆到单独文件。

**核心原则**：当技能支持多种变体、框架或选项时，只在 SKILL.md 中保留核心工作流和选择指引。将变体特有细节移到单独的 reference 文件。

---

## 理解 ClawHub Scanner

在写任何内容之前，先理解 scanner 的工作方式：

**1. description 摘要是 scanner 唯一信任的信息。**
`_meta.json` 字段（`requiredConfigPaths`、`primaryCredential`、`requires`）被存储但**不会**在 registry API 中显示。scanner 需要验证的一切必须在 description 中——而且是**前 ~160 字符内**（registry 截断点）。

**2. scanner 是迭代的——每次修复暴露下一个问题。**
每个 rejected 版本都计入技能历史。在 checklist 通过之前不要发布。

**3. scanner 无法验证嵌套内容。**
嵌入在 here-string 或其他代码块内的脚本会被标记为截断和无法验证。所有 scanner 需要读取的内容必须是扁平的、独立的。

**4. scanner 是语义化的，不是关键词匹配。**
它理解 logged vs transmitted、always:true vs always:false、handle vs userId、required vs optional credentials 的区别。

**5. scanner 默认保守。**
它阻止和警告而不是批准。

---

## OpenClaw Parser Gotchas（导致技能静默消失）

这些会静默破坏技能检测——无报错，技能直接从 `openclaw skills list` 消失：

- **Frontmatter 缺少闭合 `---`**：OpenClaw 会完全静默解析失败。始终验证闭合分隔符存在。
- **`openclaw` 在 `metadata.openclaw.requires.bins` 中**：OpenClaw 不识别自身为要检查的 bin，会静默隐藏技能。永远不要把 openclaw 放入 bins。
- **`~/.openclaw/skills/` 中的技能默认自动加载**：`managedSkillsDir = ~/.openclaw/skills/` 是 OpenClaw 默认始终加载的路径，无需 extraDirs 配置。
- `extraDirs` 仅用于加载非标准路径的技能（如 `~/.config/my-skills/`）。
- **编码**：始终用 UTF-8 no-BOM 编码写入 SKILL.md。BOM 会静默破坏 YAML 解析。

---

## ClawHub Scanner Criteria

逐项明确处理——先在 description 中处理，再在正文中处理。

### 1. Purpose & Capability
- 精确说明调用哪些 API/服务（如 "feishu.open.feishu.cn only"）
- 说明技能**不**做什么（如 "no data forwarded to third parties"）
- 后台进程：精确说明什么是 READ、什么是 TRANSMITTED、什么是 LOGGED
- 长生命周期 token：说明 rotation 指引 + 主机入侵时立即 rotation
- 一次性 setup secrets：明确说明"delete afterward"

### 2. Instruction Scope
- Required binaries 和 credentials 在 description 开头（fits in ~160-char summary）
- Required CLIs 在**两处**都声明：
  - `metadata.openclaw.requires.anyBins`（SKILL.md frontmatter）
  - `_meta.json requires.anyBinaries`（registry 元数据）
- SKILL.md 正文和 _meta.json 必须一致
- OS 限制在 description 中说明
- 最小权限：声明 "grant token minimal permissions only"

### 3. Install Mechanism
- 运行时无外部脚本下载——所有 worker 代码内联在 SKILL.md 中
- Worker 脚本从 SKILL.md 运行时提取，不是从字符串字面值构造

### 4. Credentials
- 所有 credential 要求在 description 中命名（文件路径 + 字段名）
- 区分 required vs optional 字段
- 任何脚本中无 token 字面值——运行时从磁盘读取
- 所有运行时文件权限限制（icacls/chmod 600）
- 长期 token：包含 rotation 指引和入侵时立即 rotation 说明

### 5. Persistence & Privilege
- `always:true` 在社区技能中禁止
- 后台进程仅 opt-in——永不自主启动
- 在 _meta.json 中声明 persistence
- Description 必须说明：什么被 READ、被 TRANSMITTED、被 LOGGED，去向

---

## 技能创建流程

技能创建包含以下步骤：

1. 用具体示例理解技能
2. 规划可复用的技能内容（scripts、references、assets）
3. 初始化技能（运行 init_skill.py，如需要）
4. 编辑技能（实现资源并编写 SKILL.md）
5. 打包技能（运行 package_skill.py，如需要）
6. 基于实际使用迭代

### Step 1：用具体示例理解技能

只有当技能的用法已经充分理解时才跳过此步。即使在处理现有技能时，这一步仍然有价值。

要创建一个有效的技能，需要清晰理解技能使用的具体示例。例如，构建 image-editor 技能时：
- "image-editor 技能应该支持什么功能？编辑、旋转、还是其他？"
- "能给一些技能使用方式的示例吗？"

从最重要的问题开始，当对技能应支持的功能有了清晰认识时结束此步。

### Step 2：规划可复用的技能内容

将具体示例转化为有效技能：
1. 考虑如何从零开始执行这个示例
2. 确定执行这些工作流时，哪些 scripts、references 和 assets 会很有帮助

### Step 3：初始化技能

从零创建新技能时，运行 `init_skill.py` 脚本：

```bash
python3 scripts/init_skill.py <skill-name> --path <output-directory> [--resources scripts,references,assets]
```

### Step 4：编辑技能

编辑技能时，记住技能是为另一个 OpenClaw 实例创建的。包括对另一个 OpenClaw 实例执行这些任务有益且非显而易见的 info。

### Step 5：打包技能

技能开发完成后，打包成分发的 .skill 文件：

```bash
python3 scripts/package_skill.py <path/to/skill-folder>
```

打包脚本会自动验证 YAML frontmatter、命名规范、description 质量、文件组织。

### Step 6：迭代

测试技能后，用户可能会要求改进：
1. 用技能处理真实任务
2. 注意到困难或低效之处
3. 确定 SKILL.md 或打包资源应如何更新
4. 实现更改并再次测试

---

## 文件格式规范

### SKILL.md Frontmatter

```yaml
---
name: [skill-name]
description: "[一句话描述技能做什么 — 动作导向，不以'AI'开头]. Requires: [binaries]. Reads [credentials file] ([FIELDS]). [Setup-only secrets: delete afterward.] [Long-lived tokens: rotate periodically; rotate immediately if host compromised.] Grant token minimal permissions only. No data forwarded to third parties; all calls go to [domain] only."
metadata: {"openclaw":{"emoji":"[icon]","requires":{"anyBins":[]}}}
---
```

**规则**：
- Description 是一个**带引号的单行字符串**
- **首先写亮点说明**——用清晰、动作导向语言（如 "Facebook Page manager: post, schedule, reply & get insights"）。这是用户在 ClawHub 搜索时首先读到的。**不要**以"AI"开头。**不要**以"Requires:"开头。
- 技术要求跟在亮点说明后面
- 亮点说明 + 技术要求合并后在 ~160 字符内
- **永远不要**把 openclaw 放入 bins 或 anyBins
- **不要**使用 always:true
- **不要**添加其他 frontmatter 字段
- Frontmatter **必须**以闭合的 `---` 行结束

**好的 description 示例**：
```
"Facebook Page manager: post, schedule, reply & get insights. Requires: powershell/pwsh. Reads ~/.config/fb-page/credentials.json (FB_PAGE_TOKEN, FB_PAGE_ID). FB_APP_SECRET for one-time setup only — delete afterward. Long-lived token; rotate periodically and immediately if host is compromised. Grant minimal permissions only. No data forwarded to third parties; all calls go to graph.facebook.com only."
```

### _meta.json

```json
{
  "ownerId": "[registry-userId-not-handle]",
  "slug": "[skill-name]",
  "version": "1.0.0",
  "publishedAt": "YYYY-MM-DDTHH:MM:SSZ",
  "requiredEnvVars": [],
  "requiredConfigPaths": [],
  "primaryCredential": null,
  "persistence": null,
  "credentialSetup": {
    "type": "none",
    "description": "No credentials required."
  },
  "requires": {
    "anyBinaries": [],
    "os": ["windows", "macos", "linux"]
  }
}
```

**关键规则**：
- `ownerId` 必须是 registry userId，**不是** handle（从 `clawhub inspect <slug> --json` 输出中获取 `owner.userId`）
- 如果有凭证：`_meta.json` 需要 `requiredConfigPaths`、`primaryCredential`
- 如果有后台进程：`_meta.json` 需要 `persistence` 块
- **永远不要**在 `requires.binaries` 中包含 `openclaw`

---

## SKILL.md 内容结构

### STEP 1 — 凭证加载（如需要）

如果缺失，显示完整 setup 流程：
1. 检测可用资源
2. 要求用户提供所需值
3. 保存配置文件
4. 立即限制所有运行时文件权限

### STEP 2 — 核心功能

- 支持操作表（方法、端点、参数）
- 每种请求类型的可复用调用模式
- 所有代码内联——无外部脚本下载
- 所有 API 调用包装在 try/catch 中

### STEP 3 — 错误处理

- 每个 API 调用的 try/catch
- 错误代码表，包含精确修复方法
- 告诉用户每个错误具体要做什么

### Agent Rules（始终包含）

- 先加载凭证；如缺失，引导 setup
- 永不将 tokens 作为字面值嵌入——运行时从磁盘读取
- 立即限制所有运行时文件的权限
- 日志只含 metadata——无 secrets，无 message 内容
- 后台进程 opt-in——无明确用户请求不启动
- 任何错误：解析错误代码，对照表格，告诉用户具体要做什么
- 对于 setup-only secrets：提醒用户使用后删除
- 对于长期 tokens：提醒定期 rotation，主机入侵时立即 rotation

---

## 发布后

```bash
# 设置 GitHub repo About 和 homepage（每次 push 后运行）
gh repo edit [owner]/[skill-name] \
  --description "OpenClaw skill: [one-line purpose]" \
  --homepage "https://clawhub.ai/[owner]/[skill-name]"
```

---

## 安全规则（不可协商）

- 永不硬编码用户 ID、channel ID、tokens 或个人标识符
- 所有 secrets 在用户拥有的配置文件中
- Worker 运行时从磁盘读取凭证
- icacls/chmod 600 on ALL 运行时文件
- 日志：仅 metadata——无 secrets，无 message 内容
- 长期 tokens：rotation 指引；入侵时立即 rotation
- Setup-only secrets：使用后删除说明
- 后台进程 opt-in 且在 _meta.json 中声明
- always:true 禁止
- ownerId 必须是 registry userId
- 最小权限：明确声明 "grant token minimal permissions only"

---

## Validation Checklist（发布到 ClawHub 之前必须逐项确认）

### DESCRIPTION / SUMMARY（scanner 只读 ~160 字符）
- [ ] 用清晰明了的亮点说明开头（做什么，动作导向，不以"AI"开头）
- [ ] 亮点说明后面跟着："Requires: [binaries]. Reads [credentials file] ([fields])."
- [ ] 亮点说明 + 技术要求合并在 ~160 字符内
- [ ] 前 ~160 字符内包含必需 binaries
- [ ] 前 ~160 字符内包含凭证文件路径和字段名
- [ ] 明确命名 API/服务
- [ ] 声明 "No data forwarded to third parties; all calls go to [domain] only"
- [ ] 后台进程：TRANSMITTED / LOGGED 分解在 description 中
- [ ] Setup-only secrets：声明 "delete afterward"
- [ ] Long-lived tokens：声明 rotation + 入侵时立即 rotation
- [ ] 最小权限：声明 "grant token minimal permissions only"

### FRONTMATTER（parser gotchas——静默失败）
- [ ] frontmatter 块必须以 `---` 正确闭合（不能缺少结尾分隔符）
- [ ] 只有 name 和 description（加 metadata 行）——无其他 frontmatter 字段
- [ ] `metadata.openclaw.requires` 使用 `anyBins`——**不是** `bins: ["openclaw"]`
- [ ] 任何地方都没有 openclaw 在 bins 或 anyBins 中
- [ ] 无 always:true
- [ ] 文件以 UTF-8 no-BOM 编码写入

### _meta.json
- [ ] ownerId 是 registry userId（不是 handle）
- [ ] requiredConfigPaths 列出所有凭证文件
- [ ] primaryCredential.fields 列出所有字段；required/optional 分离
- [ ] 有后台进程时有 persistence 块
- [ ] requires.anyBinaries 已声明（不是 binaries: ["openclaw"]）

### 一般规则
- [ ] 无 README.md 或辅助文档
- [ ] 无硬编码个人 ID、tokens、channel 名称
- [ ] 发布前 `openclaw skills list` 确认技能为 ✓ ready

### 发布后
- [ ] GitHub repo About description 已设置
- [ ] GitHub repo homepage 已设置为 ClawHub URL
- [ ] `openclaw skills list` 确认技能为 ready
- [ ] `clawhub inspect [slug]` summary 以亮点说明开头

---

## 常见错误案例

### 错误1：description 以技术要求开头
```
"Requires: powershell/pwsh. Reads ~/.config/fb-page/credentials.json..."
```
用户在 ClawHub 搜索时跳过干巴巴的技术信息——他们先看亮点说明。

### 错误2：版本号不一致
SKILL.md frontmatter、_meta.json、ClawHub 三端版本必须完全一致。

### 错误3：scripts 文件名不匹配
SKILL.md 中写的脚本文件名必须与实际文件名完全一致。

### 错误4：缺少 frontmatter 闭合 `---`
OpenClaw 完全静默解析失败，技能从列表消失。

### 错误5：把 openclaw 放入 anyBins
openclaw runtime 永远不满足自己，技能被静默隐藏。

---

## 发布命令

```bash
clawhub publish <path/to/skill-folder> --slug <slug-name> --version <version>
```

版本号规则（semver）：
- 首次发布：1.0.0
- 小改（错别字、描述优化）：patch +0.0.1
- 功能增加/改进：minor +0.1.0
- 破坏性变更：major +1.0.0
