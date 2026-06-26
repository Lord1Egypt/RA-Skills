# Anthropic Skills Guide (Compact, LLM-Friendly)

## 1) Core Purpose
A skill should be treated as a **stable execution specification** that teaches Claude when and how to run a workflow automatically, not a one-off prompt.

## 2) Three-Tier Loading Model
- Layer 1: `SKILL.md` frontmatter (always considered for routing)
  - Decides whether the skill should be loaded.
- Layer 2: `SKILL.md` body (loaded when needed)
  - Instructions, steps, examples, errors.
- Layer 3: Linked files (`references/`, `assets/`, `scripts/`)
  - Loaded only when necessary.

## 3) Mandatory Structure and Naming
- Required file: `SKILL.md` (exact case)
- Skill folder name must be `kebab-case`
  - valid: `notion-project-setup`
  - invalid: `Notion Project Setup`, `notion_project_setup`, `NotionProjectSetup`
- Do **not** put `README.md` inside skill directory
- Allowed optional folders:
  - `scripts/` (executable helpers)
  - `references/` (docs for deeper context)
  - `assets/` (templates, prompts, brand files)

## 4) Minimum Frontmatter (Required)
```yaml
---
name: your-skill-name
description: What it does and when to use it. Include specific trigger phrases.
---
```

Requirements:
- `name`: kebab-case, no spaces/caps, ideally matches folder name
- `description`: must contain both
  - what the skill does
  - when it should be used
- length under 1024 chars
- avoid XML-like `<` `>` in frontmatter
- avoid names containing `claude` or `anthropic` prefix/special terms

## 5) Optional Frontmatter Fields
```yaml
license: MIT
compatibility: "Claude.ai only"
allowed-tools: "Bash(python:*) Bash(npm:*) WebFetch"
metadata:
  author: your-team
  version: 1.0.0
  mcp-server: your-mcp
  tags: [automation, onboarding]
  documentation: https://...
  support: support@example.com
```

## 6) How to Write an Effective `description`
Use this shape:
- `[Capability] + [Trigger scenarios] + [Boundaries] + [File types if relevant]`

Good pattern:
- include exact user phrasings and synonyms
- include the context where it should run
- include explicit exclusions when possible

Bad pattern:
- vague text like "helps with projects"
- only technical jargon with no trigger phrase
- high-level benefit without actionable user inputs

## 7) SKILL.md Body Template
Recommended order:
1. Skill name + one-line role
2. Use cases (what / when)
3. Step-by-step workflow
4. Inputs + outputs for each step
5. At least 2 examples (user input -> actions -> result)
6. Error handling table
7. Validation criteria
8. Reference links (`references/`)

## 8) Instruction Quality Principles
- Prefer concrete commands over abstract language.
- Specify tool names and parameters explicitly.
- Put constraints and safety checks early.
- Error handling must be actionable: detect -> fix -> continue/retry.
- Keep `SKILL.md` concise; move long docs to `references/`.

## 9) Core Design Patterns
### 9.1 Sequential orchestration
- Define strict order and dependency boundaries.
- Validate output before moving forward; rollback or stop on failure.

### 9.2 Multi-MCP coordination
- Define phase boundaries and handoffs between MCP calls.
- Validate each phase before the next phase.

### 9.3 Iterative refinement
- generate draft -> validate script -> fix issues -> validate again until threshold is met.

### 9.4 Context-aware tool selection
- choose tool by input type/size/context;
- include decision tree and fallback path.

### 9.5 Domain intelligence
- apply compliance / rules / domain constraints before action;
- log decisions for traceability.

## 10) Testing and Iteration
Three layers:
- Trigger tests
  - obvious relevant queries
  - paraphrased versions
  - non-relevant negatives
- Functional tests
  - expected output correctness
  - tool/API success
  - edge and failure handling
- Comparative tests
  - with and without skill
  - compare number of tool calls, tokens, consistency

Suggested trigger target:
- about **90%** success on relevant queries (adaptive by product context)

Common feedback loops:
- Undertrigger (not activated): expand descriptions, add trigger phrases
- Overtrigger (unintended activation): tighten constraints and add negative examples
- Execution issues: rewrite for clarity, add explicit error recovery steps

## 11) Distribution
### Claude.ai / Claude Code
- build skill folder
- zip if needed
- upload in Settings > Capabilities > Skills
- enable + verify MCP connectivity

### API / Programmatic usage
- list/manage via `/v1/skills`
- attach through `container.skills`
- integrate with Console and Agent SDK for production-scale flows

### How to ship publicly
- keep a repo-level `README.md` (not inside skill folder)
- include install steps, screenshots, quick start, and outcome-focused value statement

## 12) Troubleshooting Checklist
1. Skill not detected
   - check frontmatter and `description`
2. Frontmatter parse error
   - validate YAML, closing `---`, indentation
3. Name format invalid
   - enforce kebab-case
4. No triggers
   - description too abstract / lacks user phrases
5. Wrong triggers
   - add boundary conditions and exclusions
6. MCP failures
   - verify connection, API key, permissions, tool names
7. Wrong execution behavior
   - simplify instructions, reduce ambiguity
8. Context overload
   - keep `SKILL.md` concise; move details to references

## 13) Launch Checklist
Before writing:
- define 2–3 concrete use cases
- identify dependencies (built-in vs MCP tools)
- draft workflow first

During development:
- valid folder + file naming
- valid frontmatter with clear description
- concrete steps and examples
- explicit error handling

Before release:
- pass trigger/functional tests
- verify integrations and tooling
- package and upload

After release:
- test in real chats
- monitor under/over triggering
- collect user feedback and version metadata accordingly

## 14) LLM Runtime Instructions
- map user request to the closest use case before acting
- validate preconditions each step
- require explicit expected outputs for external calls
- when conflicts occur, prioritize in order:
  1. safety + authorization
  2. task integrity
  3. reproducibility
  4. user experience

## 15) Reference sources (high-level)
- Anthropic Skills docs (Claude, API, MCP)
- Skill-creator guidance
- public skill examples and partner directories
