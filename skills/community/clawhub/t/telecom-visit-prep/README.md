# Telecom Visit Prep

One-stop enterprise visit preparation for China Telecom account managers: input a company name, automatically search enterprise information, intelligently recommend business opportunities, generate visit scripts, and output a complete visit preparation report.

## Quick Start

### OpenClaw

```bash
# Install from ClawHub
openclaw skills install telecom-visit-prep
```

After installation, input an enterprise name to trigger the workflow.

### Claude Code

Copy the skill directory to `.claude/skills/`:

```bash
cp -r telecom-visit-prep/ .claude/skills/
```

Or use `/add-skill` command pointing to the SKILL.md file path.

### Other Platforms

This skill is written in pure Markdown with LLM-driven workflows, making it highly portable across different agent platforms. See [Cross-Platform Adaptation Guide](#cross-platform-adaptation-guide) for details.

---

## Skill Structure

```
telecom-visit-prep/
├── SKILL.md                        # Skill main file (workflow definition)
├── README.md                       # This file
└── references/                     # Knowledge base and templates
    ├── telecom-products.md         # China Telecom full product line knowledge base
    ├── speech-scripts.md           # Visit script templates (dual style)
    └── report-template.md          # Visit report output template
```

---

## Cross-Platform Adaptation Guide

### Dependency Analysis

| Dependency | Level | OpenClaw | Claude Code | Codex CLI |
|--------|---------|--------------|-------------|-----------|
| **Web Search** | Core | MCP search plugin | MCP search plugin | Shell + API |
| **File Read** | Core | Built-in | Built-in | Built-in |
| **Word Document Generation** | Non-core | python-docx / MCP | python-docx / MCP | python-docx |
| **Current Time** | Non-core | Built-in | Built-in | Built-in |

> **Core dependency**: Missing means the workflow cannot run normally
> **Non-core dependency**: Missing only affects some features; main workflow can operate in degraded mode

---

### OpenClaw / Claude Code Adaptation

#### 1. Web Search Setup

Install an MCP search tool (recommended):

| MCP Server | Installation | Notes |
|-----------|---------|------|
| @anthropic/mcp-web-search | `claude mcp add web-search -- npx @anthropic/mcp-web-search` | Official, requires API Key |
| @anthropic/mcp-brave-search | `claude mcp add brave-search -- npx @anthropic/mcp-brave-search` | Brave Search, requires API Key |

After installation, the `baidu_search` references in Step 1 should be replaced with the corresponding MCP search tool calls.

**Alternative**: Use WebFetch (built-in) to directly fetch web content, though this may trigger anti-crawling mechanisms on search engines.

#### 2. Word Document Generation

**Option A: python-docx script** (recommended)

```bash
pip install python-docx
```

In the SKILL.md Step 6, replace docx skill calls with: generate a Python script that uses python-docx to create Word documents.

**Option B: MCP document server**

Search for and install an MCP server that supports docx generation (e.g., `mcp-docx`).

#### 3. Key Adaptation Points

| Content in SKILL.md | Replacement |
|------------------|-------------------|
| `baidu_search` tool calls | MCP search tool or WebFetch |
| `docx` skill dependency | python-docx script or MCP doc server |
| Skill dependency check paths | Check python-docx: `pip show python-docx` |

---

### Codex CLI Adaptation

Codex CLI has no Skill system; inject instructions as first message or into AGENTS.md:

```bash
# Option 1: As first message
codex "$(cat telecom-visit-prep/SKILL.md)

Please generate a visit preparation report for: [Enterprise Name]"

# Option 2: Write to project instructions
cat telecom-visit-prep/SKILL.md >> AGENTS.md
```

**Important**: Codex CLI cannot auto-read the `references/` directory. You must inline the content of `telecom-products.md`, `speech-scripts.md`, and `report-template.md` directly into the AGENTS.md or SKILL.md.

---

## FAQ

### Q: Can I use this without a search tool?

Yes, in degraded mode. Change Step 1 in SKILL.md to "user provides enterprise information", and the skill can still complete profile building, opportunity recommendation, script generation, and report output.

### Q: Does not generating Word files affect report quality?

No. The core value of the report is in its content, not format. Markdown output in conversation is complete; Word export is just for archiving and printing convenience.

### Q: Data security considerations?

This skill runs locally. Enterprise information search uses public channels. Word document generation is done locally with no data exfiltration.

---

## Skill Maintenance

- **Author**: KeyangWang0726 (China Telecom Changshu Branch, AI & Software Development Center)
- **Version**: 1.0.1
- **Last Updated**: 2026-05-12
- **License**: MIT