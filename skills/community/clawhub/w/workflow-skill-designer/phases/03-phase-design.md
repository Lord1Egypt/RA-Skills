# 阶段 3：阶段文件设计

在 `phases/` 目录中生成阶段文件，保留源内容中的完整执行细节。每个阶段文件都是一份完整的执行指令。

## 目标

- 为 workflowConfig 中的每个阶段创建 `phases/0N-{slug}.md`
- 保留完整源内容（智能体提示词、bash 命令、代码、校验）
- 添加标准阶段结构（标题、目标、输出、下一阶段）
- 处理不同源类型（命令提取 vs 全新生成）

## 关键规则

**内容保真度**: 阶段文件必须对其源**内容保真**。不得总结、缩写或简化执行细节。阶段文件就是执行指令本身。

| 内容类型 | 规则 |
|-------------|------|
| Agent prompts (Task calls) | 逐字保留，包含所有提示词文本、变量、约束 |
| Bash command blocks | 逐字保留，包含所有标志、路径、错误处理 |
| Code implementations | 逐字保留，包含所有函数、校验逻辑 |
| Validation checklists | 逐字保留，包含所有检查项 |
| Error handling details | 逐字保留，包含恢复策略 |
| Tables and specifications | 逐字保留，包含所有行和列 |
| Comments and notes | 逐字保留，包含内联文档 |

**反模式**: 创建一个写着"见原命令了解细节"或"用适当参数执行智能体"的阶段文件——这破坏了技能结构的目的。阶段文件必须自包含。

## 阶段文件内容限制

阶段文件是内部执行文档。**不得**包含以下禁止内容：

| 禁止模式 | 检测 | 正确位置 |
|-------------------|-----------|-----------------|
| 标志解析 (`$ARGUMENTS.includes(...)`) | Grep: `\$ARGUMENTS\.includes` | SKILL.md via AskUserQuestion → `workflowPreferences` |
| 调用语法 (`/skill-name "..."`) | Grep: `\/\w+[\-:]\w+\s+"` | 完全移除（阶段文件非面向用户） |
| 转换来源 (`Source: Converted from...`) | Grep: `Source:.*Converted from` | 完全移除（实现细节） |
| 阶段间技能路由 (`Skill(skill="...")`) | Grep: `Skill\(skill=` | 直接 `Read("phases/0N-xxx.md")` |

### 偏好引用模式

阶段文件可以**引用**工作流偏好，但**不得**从参数中**解析**它们：

```javascript
// CORRECT: Reference workflowPreferences (set by SKILL.md)
const autoYes = workflowPreferences.autoYes
const forceExplore = workflowPreferences.forceExplore

// WRONG: Parse from $ARGUMENTS
const autoYes = $ARGUMENTS.includes('--yes') || $ARGUMENTS.includes('-y')
const forceExplore = $ARGUMENTS.includes('--explore') || $ARGUMENTS.includes('-e')
```

### 阶段间交接模式

当阶段 N 需要调用阶段 M 时，使用直接阶段读取：

```javascript
// CORRECT: Direct handoff (executionContext already set)
Read("phases/02-lite-execute.md")
// Execute with executionContext (Mode 1)

// WRONG: Skill routing (unnecessary round-trip)
Skill(skill="workflow-lite-plan", args="--in-memory")
```

### 内容限制强制

从命令提取时（步骤 3.2），在逐字提取后应用内容清理：

```javascript
function sanitizePhaseContent(content) {
  let sanitized = content;

  // Remove flag parsing blocks
  sanitized = sanitized.replace(
    /\/\/.*flag.*parsing[\s\S]*?\n(?=\n)/gi, ''
  );

  // Remove invocation syntax examples
  sanitized = sanitized.replace(
    /^.*\/\w+[\-:]\w+\s+"[^"]*".*$/gm, ''
  );

  // Remove conversion provenance notes
  sanitized = sanitized.replace(
    /^\*\*Source\*\*:.*Converted from.*$/gm, ''
  );

  // Replace all $ARGUMENTS.includes patterns with workflowPreferences reference
  // Handles any flag name, not just --yes/-y
  sanitized = sanitized.replace(
    /\$ARGUMENTS\.includes\(['"]--?([^"']+)['"]\)/g,
    (match, flagName) => {
      // Map common flag names to workflowPreferences keys
      const flagMap = {
        'yes': 'workflowPreferences.autoYes',
        'y': 'workflowPreferences.autoYes',
        'explore': 'workflowPreferences.forceExplore',
        'e': 'workflowPreferences.forceExplore'
      };
      return flagMap[flagName] || `workflowPreferences.${flagName}`;
    }
  );
  // Also clean up residual || chains from multi-flag expressions
  sanitized = sanitized.replace(
    /workflowPreferences\.(\w+)\s*\|\|\s*workflowPreferences\.\1/g,
    'workflowPreferences.$1'
  );

  // Replace Skill() inter-phase routing with direct Read (with or without args)
  sanitized = sanitized.replace(
    /Skill\(skill=["']([^"']+)["'](?:,\s*args=["']([^"']+)["'])?\)/g,
    (match, skillName) => `Read("phases/0N-xxx.md")\n// Execute with context`
  );

  return sanitized;
}
```

## 步骤 3.1：阶段文件生成策略

```javascript
function selectGenerationStrategy(phase, config) {
  if (config.source.type === 'command_set' && phase.sourcePath) {
    return 'extract';    // Extract from existing command file
  } else if (config.source.type === 'text_description') {
    return 'generate';   // Generate from requirements
  } else if (config.source.type === 'existing_skill') {
    return 'restructure'; // Restructure existing content
  }
  return 'generate';
}
```

## 步骤 3.2：模式 A — 从命令提取

When source is an existing command file, transform its content into phase file format:

> **Reference pseudocode**: `extractYAMLFrontmatter()` / `removeYAMLFrontmatter()` below sketch the parsing intent only — replace them with the host environment's real frontmatter utilities in generated output.

```javascript
function extractPhaseFromCommand(phase, config) {
  const sourceContent = Read(phase.sourcePath);
  const sourceFrontmatter = extractYAMLFrontmatter(sourceContent);
  const sourceBody = removeYAMLFrontmatter(sourceContent);

  // Phase file structure:
  // 1. Phase header (new)
  // 2. Source body content (preserved verbatim)
  // 3. Output section (extracted or added)
  // 4. Next Phase link (new)

  let phaseContent = '';

  // 1. Phase header
  phaseContent += `# Phase ${phase.number}: ${phase.name}\n\n`;
  phaseContent += `${phase.description}.\n\n`;

  // 2. Source body content - PRESERVED VERBATIM
  // Only modifications:
  //   a. Remove original H1 title (replaced by phase header)
  //   b. Remove command-specific frontmatter references
  //   c. Preserve everything else as-is

  // Remove original H1 title line(s)
  let bodyContent = sourceBody;
  bodyContent = bodyContent.replace(/^# .+\n+/, '');

  // Remove command-specific overview if it just restates what the phase header says
  // But KEEP any overview content that adds execution detail

  phaseContent += bodyContent;

  // 2.5. Ensure Objective section exists
  if (!bodyContent.includes('## Objective')) {
    // Insert Objective after phase header, before main content
    const objectiveSection = `## Objective\n\n- ${phase.description}\n`;
    phaseContent = phaseContent.replace(
      `${phase.description}.\n\n${bodyContent}`,
      `${phase.description}.\n\n${objectiveSection}\n${bodyContent}`
    );
  }

  // 3. Ensure Output section exists
  if (!bodyContent.includes('## Output')) {
    phaseContent += '\n## Output\n\n';
    if (phase.outputVariables.length > 0) {
      phaseContent += phase.outputVariables.map(v => `- **Variable**: \`${v}\``).join('\n') + '\n';
    }
    if (phase.outputFiles.length > 0) {
      phaseContent += phase.outputFiles.map(f => `- **File**: \`${f}\``).join('\n') + '\n';
    }
    phaseContent += `- **TodoWrite**: Mark Phase ${phase.number} completed, Phase ${phase.number + 1} in_progress\n`;
  }

  // 4. Ensure Next Phase link exists
  if (!bodyContent.includes('## Next Phase')) {
    const nextPhase = config.phases.find(p => p.number === phase.number + 1);
    if (nextPhase) {
      const nextFilename = `${String(nextPhase.number).padStart(2, '0')}-${nextPhase.slug}.md`;
      phaseContent += `\n## Next Phase\n\n`;
      phaseContent += `Return to orchestrator, then auto-continue to [Phase ${nextPhase.number}: ${nextPhase.name}](${nextFilename}).\n`;
    }
  }

  return phaseContent;
}
```

### 内容保留检查清单

When extracting from commands, verify these content types are preserved:

```javascript
function verifyContentPreservation(sourceContent, phaseContent) {
  const checks = {
    // Count code blocks
    sourceCodeBlocks: (sourceContent.match(/```/g) || []).length / 2,
    phaseCodeBlocks: (phaseContent.match(/```/g) || []).length / 2,

    // Count Task/Agent calls
    sourceAgentCalls: (sourceContent.match(/Task\(/g) || []).length,
    phaseAgentCalls: (phaseContent.match(/Task\(/g) || []).length,

    // Count bash commands
    sourceBashBlocks: (sourceContent.match(/```bash/g) || []).length,
    phaseBashBlocks: (phaseContent.match(/```bash/g) || []).length,

    // Count tables
    sourceTables: (sourceContent.match(/\|.*\|.*\|/g) || []).length,
    phaseTables: (phaseContent.match(/\|.*\|.*\|/g) || []).length,

    // Count AskUserQuestion calls
    sourceAUQ: (sourceContent.match(/AskUserQuestion/g) || []).length,
    phaseAUQ: (phaseContent.match(/AskUserQuestion/g) || []).length,

    // Line count comparison (phase should be >= source minus frontmatter)
    sourceLines: sourceContent.split('\n').length,
    phaseLines: phaseContent.split('\n').length
  };

  const issues = [];
  if (checks.phaseCodeBlocks < checks.sourceCodeBlocks) {
    issues.push(`Missing code blocks: source=${checks.sourceCodeBlocks}, phase=${checks.phaseCodeBlocks}`);
  }
  if (checks.phaseAgentCalls < checks.sourceAgentCalls) {
    issues.push(`Missing agent calls: source=${checks.sourceAgentCalls}, phase=${checks.phaseAgentCalls}`);
  }
  if (checks.phaseBashBlocks < checks.sourceBashBlocks) {
    issues.push(`Missing bash blocks: source=${checks.sourceBashBlocks}, phase=${checks.phaseBashBlocks}`);
  }
  if (checks.phaseTables < checks.sourceTables * 0.8) {
    issues.push(`Missing tables: source=${checks.sourceTables}, phase=${checks.phaseTables}`);
  }
  if (checks.phaseAUQ < checks.sourceAUQ) {
    issues.push(`Missing AskUserQuestion: source=${checks.sourceAUQ}, phase=${checks.phaseAUQ}`);
  }

  return { checks, issues, passed: issues.length === 0 };
}
```

### 处理源命令中的编排器级内容

Some commands mix orchestrator-level instructions (coordination, TodoWrite) with execution detail. Separation rules:

| Content in Source Command | Goes To | Rule |
|---------------------------|---------|------|
| Phase execution steps, agent prompts, bash commands | **Phase file** | Preserve verbatim |
| TodoWrite update examples specific to this phase | **Phase file** (optional) | Keep if useful for context |
| Inter-phase data passing code | **SKILL.md** Post-Phase Updates | Extract to orchestrator |
| Coordinator instructions ("after this phase, auto-continue") | **SKILL.md** Core Rules | Extract to orchestrator |
| Conditional logic ("if conflict_risk >= medium") | **SKILL.md** Execution Flow | Extract to orchestrator |

When in doubt, **keep content in the phase file**. It's better to have slight overlap than to lose execution detail.

## 步骤 3.3：模式 B — 从需求生成

When source is a text description, generate phase files interactively:

```javascript
function generatePhaseFromRequirements(phase, config) {
  let phaseContent = '';

  // Phase header
  phaseContent += `# Phase ${phase.number}: ${phase.name}\n\n`;
  phaseContent += `${phase.description}.\n\n`;

  // Objective
  phaseContent += `## Objective\n\n`;
  phaseContent += `- ${phase.description}\n`;
  if (phase.outputVariables.length > 0) {
    phaseContent += `- Produce: ${phase.outputVariables.join(', ')}\n`;
  }
  if (phase.outputFiles.length > 0) {
    phaseContent += `- Generate: ${phase.outputFiles.join(', ')}\n`;
  }
  phaseContent += '\n';

  // Execution steps
  phaseContent += `## Execution\n\n`;

  if (phase.usesAgents) {
    // Generate agent delegation skeleton
    for (const agentType of phase.agentTypes) {
      phaseContent += `### Step: ${agentType} Delegation\n\n`;
      phaseContent += '```javascript\n';
      phaseContent += `const result = Task({\n`;
      phaseContent += `  subagent_type: "${mapAgentType(agentType)}",\n`;
      phaseContent += `  prompt: \`\n`;
      phaseContent += `    [ROLE] ${agentType}\n`;
      phaseContent += `    [TASK] ${phase.description}\n`;
      phaseContent += `    [INPUT] \${inputData}\n`;
      phaseContent += `    [OUTPUT] \${outputPath}\n`;
      phaseContent += `  \`,\n`;
      phaseContent += `  run_in_background: false\n`;
      phaseContent += `});\n`;
      phaseContent += '```\n\n';
    }
  } else {
    // Generate direct execution from phase.steps (required field — Phase 1 must populate)
    phaseContent += `### Step ${phase.number}.1: Execute\n\n`;
    if (phase.steps && phase.steps.length > 0) {
      phase.steps.forEach((step, idx) => {
        phaseContent += `**Step ${phase.number}.${idx + 1}**: ${step}\n\n`;
      });
    } else {
      // No steps defined — emit a concrete skeleton using phase description, never TODO
      phaseContent += `Execute: ${phase.description}\n\n`;
      phaseContent += `- Read input: ${phase.inputVariables?.join(', ') || 'workflow context'}\n`;
      phaseContent += `- Process according to phase definition\n`;
      phaseContent += `- Produce output: ${phase.outputVariables?.join(', ') || phase.outputFiles?.join(', ') || 'none'}\n\n`;
    }
  }

  // Output
  phaseContent += `## Output\n\n`;
  phase.outputVariables.forEach(v => {
    phaseContent += `- **Variable**: \`${v}\`\n`;
  });
  phase.outputFiles.forEach(f => {
    phaseContent += `- **File**: \`${f}\`\n`;
  });
  phaseContent += `- **TodoWrite**: Mark Phase ${phase.number} completed\n\n`;

  // Next Phase
  const nextPhase = config.phases.find(p => p.number === phase.number + 1);
  if (nextPhase) {
    const nextFilename = `${String(nextPhase.number).padStart(2, '0')}-${nextPhase.slug}.md`;
    phaseContent += `## Next Phase\n\n`;
    phaseContent += `Return to orchestrator, then auto-continue to [Phase ${nextPhase.number}: ${nextPhase.name}](${nextFilename}).\n`;
  }

  return phaseContent;
}

// Map custom agent type names to Task subagent_types
function mapAgentType(agentType) {
  const mapping = {
    'cli-explore-agent': 'cli-explore-agent',
    'context-search-agent': 'context-search-agent',
    'cli-execution-agent': 'cli-execution-agent',
    'action-planning-agent': 'action-planning-agent',
    'code-developer': 'code-developer',
    'test-fix-agent': 'test-fix-agent',
    'general-purpose': 'general-purpose',
    'Explore': 'Explore'
  };
  return mapping[agentType] || 'general-purpose';
}
```

## 步骤 3.4：写入阶段文件

```javascript
function writePhaseFiles(config) {
  const skillDir = `.claude/skills/${config.skillName}`;

  for (const phase of config.phases) {
    const filename = `${String(phase.number).padStart(2, '0')}-${phase.slug}.md`;
    const filepath = `${skillDir}/phases/${filename}`;

    const strategy = selectGenerationStrategy(phase, config);
    let content;

    switch (strategy) {
      case 'extract':
        content = extractPhaseFromCommand(phase, config);
        // Verify content preservation
        const sourceContent = Read(phase.sourcePath);
        const verification = verifyContentPreservation(sourceContent, content);
        if (!verification.passed) {
          console.warn(`⚠️ Content preservation issues for Phase ${phase.number}:`);
          verification.issues.forEach(issue => console.warn(`  - ${issue}`));
          // Re-extract with more aggressive preservation
          content = extractPhaseFromCommand(phase, config, { aggressive: true });
        }
        break;

      case 'generate':
        content = generatePhaseFromRequirements(phase, config);
        break;

      case 'restructure':
        content = restructureExistingPhase(phase, config);
        break;
    }

    Write(filepath, content);
    console.log(`✓ Generated: ${filepath} (${content.split('\n').length} lines)`);
  }
}
```

## 步骤 3.5：跨阶段一致性检查

After generating all phase files, verify cross-phase consistency:

```javascript
function checkCrossPhaseConsistency(config) {
  const skillDir = `.claude/skills/${config.skillName}`;
  const issues = [];

  for (const phase of config.phases) {
    const filename = `${String(phase.number).padStart(2, '0')}-${phase.slug}.md`;
    const content = Read(`${skillDir}/phases/${filename}`);

    // Check: Next Phase links point to correct file
    const nextPhaseMatch = content.match(/\[Phase (\d+): (.+?)\]\((.+?)\)/);
    if (nextPhaseMatch) {
      const nextNum = parseInt(nextPhaseMatch[1]);
      const nextPhase = config.phases.find(p => p.number === nextNum);
      if (!nextPhase) {
        issues.push(`Phase ${phase.number}: Next Phase link points to non-existent Phase ${nextNum}`);
      }
    }

    // Check: Output variables match config
    for (const varName of phase.outputVariables) {
      if (!content.includes(varName)) {
        issues.push(`Phase ${phase.number}: Output variable '${varName}' not mentioned in content`);
      }
    }
  }

  return issues;
}
```

## 大小对照参考

Expected phase file sizes relative to their source commands:

| Scenario | Phase File Size vs Source | Reason |
|----------|--------------------------|--------|
| Command extraction | ≥ 90% of source | Minor removals (H1 title, frontmatter) |
| New generation (with agents) | 50-200 lines | Agent prompt skeletons |
| New generation (direct) | 30-80 lines | Step skeletons |
| Restructure | ~100% of source | Content reorganization only |

**Red Flag**: If a phase file is significantly smaller than its source (< 70%), content was likely lost during extraction. Re-check with `verifyContentPreservation()`.

## 输出

- **文件**: 每个阶段一个 `.claude/skills/{skillName}/phases/0N-{slug}.md`
- **TodoWrite**: 标记阶段 3 已完成，阶段 4 进行中

## 下一阶段

返回编排器，然后自动继续 [阶段 4：校验与集成](04-validation.md)。
