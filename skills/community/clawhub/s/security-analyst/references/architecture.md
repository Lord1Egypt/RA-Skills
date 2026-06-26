# Security Analyst — Architecture Reference

**See `references/constants.md` for the authoritative registry** of all directory paths, output filenames (including reports under `reports/`), template files, agent registry, stages, recon step files, and placeholder variables. **See `references/platform-tools.md` for environment-specific tool mapping (Cursor, Claude Code, Codex) — required to prevent hangs on Cursor.**

## Directory Structure

Per the skill layout guide, the skill uses `references/` for documentation and `assets/` for templates:

```
security-analyst/
├── SKILL.md                              # Skill entry point (required)
├── references/
│   ├── architecture.md                  # This file
│   ├── constants.md                     # Paths, agent registry, templates
│   ├── skills-complete-guide.md        # Compliance reference (maintainers)
│   ├── plan-lod.md                      # Internal planning
│   ├── commands/                        # Entry points and orchestrator
│   │   ├── security-analyst.md          # Main orchestrator (interactive)
│   │   ├── full.md                      # Full analysis entry point
│   │   ├── focused.md                   # Focused analysis entry point
│   │   ├── recon.md                     # Recon-only entry point
│   │   ├── threat-model.md              # Threat model entry point
│   │   ├── variant-hunt.md              # Variant hunt entry point
│   │   ├── fix-plan.md                  # Fix plan entry point
│   │   ├── sbom.md                      # SBOM entry point
│   │   ├── diff.md                      # Delta report entry point
│   │   ├── compliance.md                # Compliance mapping entry point
│   │   ├── privacy.md                   # Privacy assessment entry point
│   │   └── security-analysis.md         # Plan-level security analysis
│   ├── prompts/                         # Agent prompt templates (25 files)
│   │   ├── recon-agent.md               # Phase 0: reconnaissance
│   │   ├── attack-surface-http.md        # Phase 1: HTTP entry points
│   │   ├── attack-surface-authz.md      # Phase 1: database/authz rules
│   │   └── ... (see constants.md)       # All agent prompts
│   └── plugins/                         # Framework-specific security checks
│       ├── README.md                    # Plugin format spec and instructions
│       └── *.md                         # 16 plugins (Firebase, React, etc.)
└── assets/
    └── templates/                       # Output format templates (10 files)
        ├── recon-report.md              # Recon LOD format definitions
        ├── finding.md                   # Individual finding format
        ├── agent-common.md              # Shared LOD output + incidental findings
        ├── group-report.md              # Per-stage report
        ├── final-report.md              # Final report structure
        ├── fix-plan.md                  # Fix plan structure
        ├── sbom-report.md               # Software Bill of Materials
        ├── compliance-report.md         # Compliance framework mapping
        ├── delta-report.md              # Delta report between runs
        └── privacy-report.md            # Privacy & data protection assessment
```

## Agent Design

All agents are `generalPurpose` subagents (need Bash, Read, Grep, Glob for code analysis and git history mining). Each agent:

1. Reads the recon index for LOD-0+1 overview, selectively reads LOD-2 step files for relevant sections
2. Reads prior stage findings (if applicable)
3. Performs its specialized analysis
4. Reports findings using the standard finding template
5. Reports incidental findings (IX-prefixed) for issues outside its focus area

### Key Principles

- **Offensive framing**: Every analysis starts with "If I were attacking this system..."
- **Concrete exploits**: Every Medium+ finding includes reproducible attack steps and PoC
- **Chain analysis**: Low findings that enable Medium findings that enable Critical exploits = Critical chain
- **Git history mining**: Past fixes often have incomplete variants
- **OWASP LLM Top 10**: Dedicated agent covers all 10 categories plus a mitigation verification pass
- **Framework plugins**: After recon, framework-specific plugins are auto-detected and injected into relevant agent prompts. 16 plugins available
- **Dynamic scoping**: Recon determines which agents to skip (no frontend agent for backend-only projects, no LLM agent for projects without AI)
- **Stage discipline**: Later stages depend on earlier findings; never start a stage early
- **Critic validation**: Adversarial review catches false positives before the final report

## Level of Detail (LOD) Architecture

Agent reports use a three-tier Level of Detail system to minimize context consumption across independent agent context windows:

| Level | Content | ~Tokens | Where it lives |
|---|---|---|---|
| LOD-0 | `ID \| Severity \| One sentence` | 30/finding | Agent return message, orchestrator context, `{PRIOR_FINDINGS_SUMMARY}` |
| LOD-1 | ID + title + severity + CVSS + CWE + file:line + paragraph | 100/finding | `{FINDINGS_DIR}/index.md`, terminal agent prompts |
| LOD-2 | Full finding with PoC, remediation, regression test | 800/finding | `{FINDINGS_DIR}/{FINDING-ID}.md`, read on demand |

**How it flows:**
1. Analysis agents write atomic LOD-2 files to `{FINDINGS_DIR}/` and return LOD-0 summaries
2. The orchestrator builds `{FINDINGS_DIR}/index.md` with LOD-0 + LOD-1 views
3. Next-stage agents receive LOD-0 in their prompt; selectively `Read` LOD-2 files for relevant findings
4. Terminal agents (exploit dev, critic, report writer) receive LOD-1 index; `Read` all LOD-2 files

This saves 80-96% of prompt tokens for downstream agents while preserving full detail on disk.

### Recon LOD Architecture

The recon report uses the same LOD architecture as findings:

| Level | Content | Where it lives |
|---|---|---|
| LOD-0 | `Step # \| Section Name \| Key facts` | `{RECON_DIR}/index.md` (top table) |
| LOD-1 | Key metric + key files + notable observations + details link | `{RECON_DIR}/index.md` (section briefs) |
| LOD-2 | Full tables with every file:line reference | `{RECON_DIR}/step-{NN}-{name}.md` |

**How it flows:**
1. 14 parallel recon agents each write one LOD-2 step file and return LOD-0+1 summaries
2. The orchestrator assembles `recon/index.md` with LOD-0 table + LOD-1 briefs
3. Downstream agents read the index, then selectively read relevant step files
4. Each downstream agent's prompt specifies which step files are most relevant

### Task-Driven Progress Tracking

All platforms use agents-only orchestration (no Teams). Agents are spawned via the Task tool with self-contained prompts and return results via the Task return value. On **Claude Code / Codex**, TaskCreate/TaskUpdate provide user-visible progress tracking — the orchestrator creates tasks before spawning and marks them completed after each agent returns. On **Cursor**, task tracking is not available (no TaskCreate/TaskList). See `references/platform-tools.md`.

## Context Budget Considerations

The LOD architecture mitigates most context pressure, but be aware:
- The LLM agent prompt (`attack-surface-llm.md`) is ~340 lines before plugin injection — the largest single prompt
- Terminal agents (exploit dev, critic, report writer) still read all LOD-2 files via tool calls; for runs with 40+ findings, consider batching reads
- Plugin sections add to every injected agent's context — keep plugins concise

## Adding New Agents

1. Create a prompt file in `references/prompts/` following the pattern of existing prompts
2. Use placeholders: `{RECON_INDEX_PATH}`, `{RECON_DIR}`, `{FINDING_TEMPLATE_PATH}`, `{PRIOR_FINDINGS_SUMMARY}`
3. Define a finding ID prefix (e.g., `NEW-XXX`)
4. Add the agent to the appropriate stage in `references/commands/security-analyst.md`

## Adding New Plugins

1. Create a `.md` file in `references/plugins/` (e.g., `spring-boot.md`)
2. Add YAML frontmatter with `name` and `detect` criteria (files, dependencies, keywords)
3. Add `## {agent-name}` sections with framework-specific security checks
4. The orchestrator auto-detects plugins after recon and injects matching sections into agent prompts
5. See `references/plugins/README.md` for the full format spec
