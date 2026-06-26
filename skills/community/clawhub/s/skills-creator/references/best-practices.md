# Best Practices for OpenClaw Skills

Comprehensive design guidelines derived from analyzing top-performing skills on ClawHub.

## Design Philosophy

### LLM is the execution engine

A skill does not execute logic — the LLM does. Write clear instructions that tell the LLM **what to do**, and it will use its existing tools (Read, Write, Grep, Bash) to carry out the work. Only add `scripts/` when the task requires deterministic computation the LLM cannot reliably do (API calls, binary operations, error pattern matching).

### Tables are the fastest lookup structure

When an LLM encounters conditional logic ("if the user wants X, do Y"), a table row is found in ~1 token scan. A paragraph requires reading and parsing the entire block. Always prefer tables for:

- Situation → action mappings
- Field → format → rules references
- Decision criteria with multiple branches

### Guard clauses improve triggering accuracy

Explicit "When to use this skill" and "When NOT to use" sections help the LLM avoid false activations. The more specific the guard clause, the better.

### Negative examples are as valuable as positive ones

Show what NOT to do alongside what to do. LLMs learn boundaries from contrast. A bad example with explanation teaches more than three good examples alone.

---

## Description Deep Dive

The `description` field is the single most important piece of text in a skill. It is the ONLY text the LLM evaluates when deciding whether to activate a skill. Everything else (body, references, scripts) only matters AFTER activation.

### Formula

```
[Action verb] + [value proposition]. Use when [enumerated trigger conditions] or discusses [topic areas].
```

### Worked Examples

**Simple skill (find-skills)**:

> Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities.

Analysis: Starts with action verb ("Helps"), includes 3 quoted trigger phrases, covers intent pattern ("express interest in extending capabilities").

**Medium skill (tavily-search)**:

> AI-optimized web search via Tavily API. Returns concise, relevant results for AI agents.

Analysis: Terse but effective — clear value prop ("AI-optimized"), target audience ("AI agents"), differentiator ("concise, relevant"). Works because web search is universally understood.

**Complex skill (self-improving-agent)**:

> Captures learnings, errors, and corrections to enable continuous improvement. Use when: (1) A command or operation fails unexpectedly, (2) User corrects Claude ('No, that's wrong...', 'Actually...'), (3) User requests a capability that doesn't exist, (4) An external API or tool fails, (5) Claude realizes its knowledge is outdated or incorrect, (6) A better approach is discovered for a recurring task. Also review learnings before major tasks.

Analysis: Enumerated triggers (6 specific conditions), exact dialogue quotes, contextual guidance ("Also review learnings before major tasks"). This is the gold standard for complex skills.

### Common Mistakes

| Mistake | Example | Fix |
|---------|---------|-----|
| Too vague | "A helpful skill for various tasks" | Add specific trigger phrases and scenarios |
| No trigger phrases | "Manages Docker configurations" | Add "Use when user asks to..." with quoted phrases |
| Too long | 500+ character wall of text | Front-load the value prop, enumerate triggers concisely |
| Passive voice | "Skills can be created using..." | "Create, review, and improve OpenClaw skills..." |

---

## Content Structure Patterns

### Quick Reference Pattern

Place immediately after the title paragraph. Maps user intent to action:

```markdown
## Quick Reference

| User wants... | Do this |
|---------------|---------|
| [Intent 1] | → [Action with step reference] |
| [Intent 2] | → [Action with step reference] |
```

This serves as a dispatch table — the LLM reads it first and jumps to the relevant section.

### Workflow Mode Pattern

For skills with multiple distinct use cases, define numbered modes:

```markdown
### Mode N: [Descriptive Name]

**When**: [Trigger condition]

1. [Step 1]
2. [Step 2]
3. [Step 3]
```

Each mode should be self-contained — the LLM can execute it without reading other modes.

### Rule Pattern

For constraints the LLM must always follow:

```markdown
### Rule N: [Short imperative title]

[One paragraph explaining the rule with rationale]
```

Keep to 3–5 rules. More than 5 dilutes attention. If you need more constraints, they belong in specific workflow modes, not as top-level rules.

### Inline Code Pattern

For skills that wrap CLI tools:

```markdown
## [Tool Name]

\`\`\`bash
{baseDir}/scripts/tool.sh "argument"
\`\`\`

Options:
- `-n <count>`: Description (default: 5)
- `--deep`: Description
```

Minimal prose. Let the code block speak. Add options as a bulleted list, not a table (faster to scan for CLI reference).

---

## Metadata Best Practices

### Single-line JSON

The ClawHub YAML parser processes metadata as a single line. This works:

```yaml
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["node"],"env":["API_KEY"]}}}
```

This **breaks**:

```yaml
metadata:
  clawdbot:
    emoji: "🔍"
    requires:
      bins: ["node"]
```

### Use `clawdbot` key

The ecosystem convention is `clawdbot`, not `openclaw`. 5 out of 6 top skills use `clawdbot`. Follow convention to ensure platform tooling recognizes your metadata.

### Declare ALL dependencies

`requires.bins` must include every executable the skill invokes, including transitive ones:

| If your skill runs... | requires.bins should include |
|----------------------|------------------------------|
| `node scripts/search.mjs` | `["node"]` |
| `npx -y some-package` | `["npx", "node"]` |
| MCP via mcporter | `["mcporter", "npx", "node"]` |
| `curl` API calls | `["curl"]` |
| Pure instructions (no code) | `[]` (empty array) |

Missing entries cause silent failures — the skill loads but commands error out. Adding all bins lets ClawHub warn users at install time.

### Emoji selection

Choose an emoji that represents the skill's **domain**, not its mechanism:

- 🔍 Search / discovery
- 🎨 Creative / design
- 🧠 Learning / AI
- 🛠️ Development tools
- 📊 Data / analytics
- 🔒 Security

---

## Security and VirusTotal Compliance

ClawHub runs automated security scans on all published skills. Certain terms and patterns trigger flags:

### Terms to avoid

| Flagged term | Safe alternative | Why flagged |
|-------------|-----------------|-------------|
| "upload" | "prepare", "compress" | Implies data exfiltration |
| "public URL" | "reference URL", "temporary link" | Implies exposure of private data |
| "CDN" | "image hosting", "storage" | Associated with data staging |
| `@latest` | `@1.2.5` (pinned version) | Supply chain risk — floating versions can be hijacked |
| "execute arbitrary" | "run specified" | Associated with RCE |

### Version pinning

All `npx` references in SKILL.md, README, and scripts must use pinned versions:

```bash
# Good
npx -y meigen@1.2.5

# Bad — supply chain risk
npx -y meigen@latest
npx -y meigen
```

---

## Cross-Platform Considerations

### `{baseDir}` for portable paths

OpenClaw resolves `{baseDir}` to the skill's installation directory at runtime. Always use it for referencing files within the skill package:

```bash
# Good
node {baseDir}/scripts/search.mjs "query"

# Bad — breaks when installed elsewhere
node ~/.openclaw/skills/my-skill/scripts/search.mjs "query"
```

### Shell compatibility

Write scripts for `bash`, not `zsh`. Use `#!/usr/bin/env bash` as the shebang. Avoid zsh-specific features (arrays with `typeset -A`, `=~` with PCRE). This ensures compatibility across macOS and Linux.

### File permissions

Scripts in `scripts/` must be executable. Add `chmod +x` instructions or ensure the git repository preserves the execute bit:

```bash
chmod +x scripts/*.sh
```

---

## Real-World Skill Analysis

How three top skills implement these principles at different complexity levels:

| Dimension | find-skills (Simple) | tavily-search (Medium) | self-improving-agent (Complex) |
|-----------|---------------------|------------------------|-------------------------------|
| SKILL.md lines | 134 | 39 | 648 |
| Subdirectories | 0 | 1 (scripts/) | 4 (scripts/, references/, hooks/, assets/) |
| Executable code | 0 lines | ~160 lines (2 Node.js scripts) | ~300 lines (3 shell scripts) |
| Description triggers | 6 trigger phrases | 0 (universal use case) | 6 enumerated conditions |
| Tables | 2 (categories, tips) | 0 (code blocks instead) | 12+ (decisions, formats, priorities) |
| Guard clauses | 6-item "When to Use" list | None needed | "Detection Triggers" section |
| Negative cases | "When No Skills Are Found" | None | "Resolving Entries" lifecycle |
| Core mechanism | LLM runs `npx skills find` | LLM runs `node {baseDir}/scripts/` | LLM writes Markdown files per format spec |

### Key insight

All three skills share one principle: **the LLM is the execution engine**. The skill provides instructions; the LLM uses its standard tools to carry them out. Code is only added where deterministic behavior is required (API calls in tavily, error pattern matching in self-improving-agent).
