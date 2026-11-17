# 阶段 1：需求分析

## 目标

- 识别工作流中的所有阶段/步骤
- 映射阶段间的数据流
- 识别智能体、工具和条件逻辑
- 检测输入源类型并相应提取内容
- 为后续阶段产出 `workflowConfig` 对象

## 步骤 1.1：识别输入源

```javascript
// Determine what the user provided
const inputType = detectInputType(userInput);
// Returns: 'command_set' | 'text_description' | 'requirements_doc' | 'existing_skill'
```

### 源类型检测

| 指示 | 类型 | 操作 |
|-----------|------|--------|
| 指向 `.claude/commands/**/*.md` 的路径 | `command_set` | 读取编排器 + 发现子命令 |
| 描述工作流的自由文本 | `text_description` | 交互式需求收集 |
| 指向 `.md` 或 `.json` 需求的路径 | `requirements_doc` | 解析结构化需求 |
| 指向 `.claude/skills/**/*.md` 的路径 | `existing_skill` | 分析并重构 |

### 异常输入处理

| 异常 | 触发条件 | 处理 |
|------|----------|------|
| **空输入** | `userInput` 为空或仅含空白 | 引导补充："请提供工作流描述、命令文件路径、需求文档路径或现有技能路径" |
| **源文件不存在** | 路径指向的文件/目录不存在 | 列出候选路径让用户选择（从项目根开始扫描常见位置），或让用户修正路径 |
| **frontmatter 解析失败** | 文件有 YAML frontmatter 但格式不合法 | 展示 frontmatter 原文，提示用户修正 YAML 格式（常见错误：缩进、冒号后缺空格） |
| **需求文档无 phase 结构** | `requirements_doc` 模式下未找到 phase 定义 | 引导用户补充 phase 章节，或退回到 `text_description` 模式用交互式收集 |
| **子命令发现为空** | `command_set` 模式下编排器无 Skill() 调用 | 提示"编排器中未发现子命令调用，这可能是单命令工作流——是否改为单 SKILL.md 模式？" |

若 `detectInputType` 无法确定类型，默认进入 `text_description` 模式并说明原因。

## 步骤 1.2：源特定分析

### 模式 A：命令集分析

当输入源是现有的编排器命令 + 子命令时：

```javascript
// Step A.1: Read orchestrator command
const orchestratorPath = userInput; // e.g., ".claude/commands/workflow/plan.md"
const orchestratorContent = Read(orchestratorPath);

// Step A.2: Extract frontmatter
const frontmatter = extractYAMLFrontmatter(orchestratorContent);
// Fields: name, description, argument-hint, examples, allowed-tools, group

// Step A.3: Discover sub-commands by scanning Skill() calls
const skillCalls = orchestratorContent.match(/Skill\(skill="([^"]+)"/g);
// e.g., ["workflow:session:start", "workflow:tools:context-gather", ...]

// Step A.4: Map Skill() calls to file paths
// Pattern: "workflow:session:start" → ".claude/commands/workflow/session/start.md"
//          "workflow:tools:context-gather" → ".claude/commands/workflow/tools/context-gather.md"
const subCommandPaths = skillCalls.map(call => {
  const parts = call.replace('Skill(skill="', '').replace('"', '').split(':');
  return `.claude/commands/${parts.join('/')}.md`;
});

// Step A.5: Read all sub-commands
const subCommands = [];
for (const path of subCommandPaths) {
  const content = Read(path);
  const fm = extractYAMLFrontmatter(content);
  subCommands.push({
    path: path,
    content: content,
    frontmatter: fm,
    skillCallName: extractSkillCallName(path),
    bodyContent: removeYAMLFrontmatter(content)
  });
}

// Step A.6: Identify phase ordering from orchestrator execution flow
// Look for patterns like:
//   "Phase 1: ..." → first Skill() call
//   "Phase 2: ..." → second Skill() call
//   Conditional logic (if/else) → conditional phases
const phaseOrder = extractPhaseOrder(orchestratorContent, skillCalls);
```

**编排器中的关键提取点**:

| 章节 | 提取内容 | 映射至 |
|---------|-----------------|---------|
| Coordinator Role / Overview | 工作流描述、执行模型 | SKILL.md description + Architecture |
| Core Rules | 编排约束 | SKILL.md Core Rules |
| Execution Process | 阶段顺序 + 条件 | SKILL.md Execution Flow |
| Data Flow | 阶段间变量 | SKILL.md Data Flow |
| TodoWrite Pattern | 附加/折叠示例 | SKILL.md TodoWrite Pattern |
| Input Processing | 结构化格式规则 | SKILL.md Input Processing |
| Error Handling | 恢复策略 | SKILL.md Error Handling |
| Coordinator Checklist | 前/后动作 | SKILL.md Coordinator Checklist |
| Related Commands | 前置/后续 | SKILL.md Related Commands |
| Phase N sections | 阶段特定编排器指令 | SKILL.md inline (brief), Phase files (detail) |

**子命令中的关键提取点**:

| 章节 | 提取内容 | 映射至 |
|---------|-----------------|---------|
| Full body content | 完整执行细节 | Phase file (preserved verbatim) |
| Agent prompts (Task calls) | 智能体委派逻辑 | Phase file agent sections |
| Bash command blocks | Shell 执行步骤 | Phase file step sections |
| Validation/Output sections | 阶段输出 | Phase file Output section |
| Frontmatter | 工具、描述 | Phase file header context |

### 模式 B：文本描述分析

当输入源是自然语言工作流描述时：

```javascript
// Interactive requirements gathering
const basicInfo = AskUserQuestion({
  questions: [
    {
      question: "What is this workflow skill's name? (kebab-case)",
      header: "Name",
      multiSelect: false,
      options: [
        { label: "Custom name", description: "Enter a custom skill name" },
        { label: "Auto-generate", description: "Generate from workflow description" }
      ]
    },
    {
      question: "How many main phases does this workflow have?",
      header: "Phases",
      multiSelect: false,
      options: [
        { label: "3 phases", description: "Simple linear workflow" },
        { label: "4 phases", description: "Standard workflow with validation" },
        { label: "5+ phases", description: "Complex workflow with conditions" }
      ]
    }
  ]
});

// For each phase, gather details
const phases = [];
for (let i = 0; i < phaseCount; i++) {
  const phaseInfo = AskUserQuestion({
    questions: [
      {
        question: `Phase ${i+1}: What does this phase do?`,
        header: `Phase ${i+1}`,
        multiSelect: false,
        options: [
          { label: "Session/Init", description: "Initialize session or state" },
          { label: "Context/Gather", description: "Collect information or analyze" },
          { label: "Process/Transform", description: "Process data or generate artifacts" },
          { label: "Validate/Review", description: "Quality check or user review" }
        ]
      },
      {
        question: `Phase ${i+1}: Does it use agents?`,
        header: "Agents",
        multiSelect: false,
        options: [
          { label: "No agents", description: "Direct execution only" },
          { label: "Single agent", description: "Delegates to one agent" },
          { label: "Multiple agents", description: "Parallel or sequential agents" }
        ]
      }
    ]
  });
  phases.push(phaseInfo);
}

// Gather conditional logic
const conditions = AskUserQuestion({
  questions: [{
    question: "Are any phases conditional (skipped based on previous results)?",
    header: "Conditions",
    multiSelect: false,
    options: [
      { label: "No conditions", description: "All phases always execute" },
      { label: "Has conditions", description: "Some phases execute conditionally" }
    ]
  }]
});
```

### 模式 C：需求文档

当输入源是结构化需求文档时：

```javascript
// Read and parse requirements
const reqContent = Read(requirementsPath);

// Extract structured fields
// Expected format: Markdown with ## sections for each phase
// Or JSON with phases array
const requirements = parseRequirements(reqContent);
```

### 模式 D：现有技能重构

当输入源是待重构的现有技能时：

```javascript
// Read existing SKILL.md
const existingSkill = Read(skillPath);

// Scan for phase files
const existingPhases = Glob(`${skillDir}/phases/*.md`);

// Analyze current structure for improvement
const analysis = analyzeExistingStructure(existingSkill, existingPhases);
```

## 步骤 1.3：构建工作流配置

无论输入源类型，产出统一的 `workflowConfig`：

```javascript
const workflowConfig = {
  // Metadata
  skillName: "workflow-plan",           // kebab-case
  title: "Workflow Plan",               // Human-readable
  description: "5-phase planning...",   // One-line description
  triggers: ["workflow-plan"],          // Trigger phrases
  allowedTools: ["Task", "AskUserQuestion", "TodoWrite", "Read", "Write", "Edit", "Bash", "Glob", "Grep", "Skill"],

  // Source information
  source: {
    type: "command_set",                // input source type
    orchestratorPath: "...",            // original orchestrator file
    subCommandPaths: ["..."]            // original sub-command files
  },

  // Phase definitions
  phases: [
    {
      number: 1,
      name: "Session Discovery",
      slug: "session-discovery",        // for filename: 01-session-discovery.md
      description: "Create or discover workflow session",
      sourcePath: ".claude/commands/workflow/session/start.md",
      isConditional: false,
      condition: null,
      usesAgents: false,
      agentTypes: [],
      todoWriteSubTasks: [],            // no sub-tasks (atomic phase)
      outputVariables: ["sessionId"],
      outputFiles: ["planning-notes.md"]
    },
    {
      number: 2,
      name: "Context Gathering",
      slug: "context-gathering",
      description: "Gather project context via agents",
      sourcePath: ".claude/commands/workflow/tools/context-gather.md",
      isConditional: false,
      condition: null,
      usesAgents: true,
      agentTypes: ["cli-explore-agent", "context-search-agent"],
      todoWriteSubTasks: [
        "Analyze codebase structure",
        "Identify integration points",
        "Generate context package"
      ],
      outputVariables: ["contextPath", "conflictRisk"],
      outputFiles: ["context-package.json"]
    },
    {
      number: 3,
      name: "Conflict Resolution",
      slug: "conflict-resolution",
      description: "Detect and resolve conflicts",
      sourcePath: ".claude/commands/workflow/tools/conflict-resolution.md",
      isConditional: true,
      condition: "conflictRisk >= 'medium'",
      usesAgents: true,
      agentTypes: ["cli-execution-agent"],
      todoWriteSubTasks: [
        "Detect conflicts with CLI analysis",
        "Present conflicts to user",
        "Apply resolution strategies"
      ],
      outputVariables: [],
      outputFiles: ["conflict-resolution.json"]
    },
    {
      number: 4,
      name: "Task Generation",
      slug: "task-generation",
      description: "Generate implementation plan and task JSONs",
      sourcePath: ".claude/commands/workflow/tools/task-generate-agent.md",
      isConditional: false,
      condition: null,
      usesAgents: true,
      agentTypes: ["action-planning-agent"],
      todoWriteSubTasks: [],            // single agent task
      outputVariables: [],
      outputFiles: ["IMPL_PLAN.md", "IMPL-*.json", "TODO_LIST.md"]
    }
  ],

  // Data flow
  dataFlow: [
    { from: "input", to: "phase1", variables: ["structuredDescription"] },
    { from: "phase1", to: "phase2", variables: ["sessionId"] },
    { from: "phase2", to: "phase3", variables: ["contextPath", "conflictRisk"] },
    { from: "phase2", to: "phase4", variables: ["contextPath"] },
    { from: "phase3", to: "phase4", variables: ["resolvedArtifacts"] }
  ],

  // Features
  features: {
    hasAutoMode: true,                  // Interactive preference collection (AskUserQuestion)
    hasConditionalPhases: true,         // some phases may be skipped
    hasTodoWriteSubTasks: true,         // phases expand into sub-tasks
    hasPlanningNotes: true,             // accumulated state document
    hasPostPhaseUpdates: true,          // state updates between phases
    hasMemoryCompaction: true,          // compact after heavy phases
    hasUserDecisionGate: true           // user choice after final phase
  }
};
```

## 步骤 1.4：用户确认

将分析后的结构呈现给用户确认：

```javascript
// Display summary
console.log(`
Workflow Analysis Complete:
  Name: ${workflowConfig.skillName}
  Phases: ${workflowConfig.phases.length}
  ${workflowConfig.phases.map(p =>
    `  ${p.number}. ${p.name}${p.isConditional ? ' (conditional)' : ''}${p.usesAgents ? ` [${p.agentTypes.join(', ')}]` : ''}`
  ).join('\n')}
  Data Flow: ${workflowConfig.dataFlow.length} connections
  Features: ${Object.entries(workflowConfig.features).filter(([,v]) => v).map(([k]) => k).join(', ')}
`);

const confirm = AskUserQuestion({
  questions: [{
    question: "Proceed with this workflow structure?",
    header: "Confirm",
    multiSelect: false,
    options: [
      { label: "Yes, proceed", description: "Generate skill with this structure" },
      { label: "Modify phases", description: "Adjust phase count or ordering" },
      { label: "Add features", description: "Enable additional patterns (auto mode, conditions, etc.)" }
    ]
  }]
});
```

## 输出

- **变量**: `workflowConfig`（结构化配置对象）
- **TodoWrite**: 标记阶段 1 已完成，阶段 2 进行中

## 下一阶段

返回编排器，然后自动继续 [阶段 2：编排器设计](02-orchestrator-design.md)。
