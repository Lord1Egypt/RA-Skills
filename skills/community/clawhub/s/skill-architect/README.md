# skill-architect

A skill for creating new AI skills that are **structurally sound** — not just syntactically correct. Works with any AI coding tool — Claude Code, Google Antigravity, Cursor, Windsurf, Cline, GitHub Copilot, and more.

Most skill-creation guides focus on format: how to write `SKILL.md`, what goes in frontmatter, how to organize directories. This skill focuses on **design**: before writing anything, it helps you figure out what shape the skill's internal logic should take.

It does this by applying [Google's 5 Agent Skill Design Patterns](https://x.com/GoogleCloudTech/status/2033953579824758855?s=20) as a structural framework — and by interviewing you before making any decisions.

---

## Quick Start

Once installed, trigger the skill by saying things like:

- "Create a skill for writing business proposals"
- "Build a skill that reviews React components"
- "Help me write a skill for client onboarding workflows"
- "I want a skill that generates weekly status reports"
- "Design a skill for API documentation audits"
- "Make a skill that plans database migrations"

The skill will interview you with 2–3 targeted questions, recommend a design pattern, and scaffold a complete skill directory.

---

## The 5 Patterns

| Pattern | Use when... |
|---|---|
| **Tool Wrapper** | Encapsulating correct usage of a specific API, SDK, or framework |
| **Generator** | Output must follow the same structure every time |
| **Reviewer** | Evaluating or auditing content against a defined standard |
| **Inversion** | You must collect information before you can act |
| **Pipeline** | Work has ordered steps that can't be skipped |

Patterns can be combined. `Inversion → Generator` and `Pipeline + Reviewer` are especially common.

---

## How It Works

This skill itself is built on the **Inversion** pattern — it interviews you before making any pattern recommendation.

```
You describe what you want the skill to do
          ↓
AI asks 2–3 targeted questions
          ↓
AI proposes a pattern (or combination) with reasoning
          ↓
You confirm or adjust
          ↓
AI scaffolds the SKILL.md from the matching template
          ↓
Test → iterate
```

The pattern recommendation always comes with an explanation. You're never just told "use Pipeline" — you're shown *why*, based on what you described.

---

## Installation

### Quick Install (any supported agent)

The easiest way to install — works with Claude Code, Cursor, Windsurf, Cline, and [40+ other agents](https://github.com/vercel-labs/skills):

```bash
npx skills add vincent-hq/skill-architect
```

The CLI auto-detects your agent and places the skill in the right directory.

---

### Manual Installation

If you prefer to install manually, follow the instructions for your tool below.

### Claude Code

Supports multi-file skill directories — all pattern templates and references are loaded automatically.

**Option A: Global install (available in all projects)**
```bash
git clone https://github.com/vincent-hq/skill-architect.git
mkdir -p ~/.claude/skills
cp -r skill-architect ~/.claude/skills/skill-architect
```

**Option B: Project install (available in one project)**
```bash
git clone https://github.com/vincent-hq/skill-architect.git
mkdir -p .claude/skills
cp -r skill-architect .claude/skills/skill-architect
```

After copying, the skill auto-triggers when you ask to create a skill.

### Google Antigravity

Supports multi-file skill directories — same `SKILL.md` format, different directory path.

**Option A: Global install (available in all projects)**
```bash
git clone https://github.com/vincent-hq/skill-architect.git
mkdir -p ~/.gemini/antigravity/skills
cp -r skill-architect ~/.gemini/antigravity/skills/skill-architect
```

**Option B: Project install (available in one project)**
```bash
git clone https://github.com/vincent-hq/skill-architect.git
mkdir -p .agent/skills
cp -r skill-architect .agent/skills/skill-architect
```

After copying, the skill auto-triggers when you ask to create a skill.

### Cursor

1. Copy the skill files into your project:
   ```bash
   git clone https://github.com/vincent-hq/skill-architect.git
   mkdir -p .cursor/rules
   cp skill-architect/SKILL.md .cursor/rules/skill-architect.md
   ```
2. Alternatively, go to **Settings → Rules → Project Rules** and paste the content of `SKILL.md`.

> **Note:** Cursor rules don't support multi-file references, so the templates in `references/` won't auto-load. You can paste specific template content into your rule file or reference them manually.

### Windsurf

1. Open **Cascade Settings → Custom Rules**
2. Paste the content of `SKILL.md`
3. For full pattern template support, also include content from `references/patterns.md`

### Cline

1. Open Cline settings and navigate to **Custom Instructions**
2. Paste the content of `SKILL.md` as a system prompt
3. Reference template files manually when scaffolding

### Other AI Coding Tools

The skill is plain markdown — it works anywhere you can provide custom instructions:

1. Copy the content of `SKILL.md`
2. Add it as a system prompt, custom instruction, or project rule in your tool
3. For best results, also include `references/patterns.md` for the full pattern definitions

---

## File Structure

```
skill-architect/
├── SKILL.md                          — Main skill instructions
├── references/
│   ├── patterns.md                   — Full definitions, decision criteria, combinations
│   └── templates/
│       ├── tool-wrapper.md           — Template for Tool Wrapper skills
│       ├── generator.md              — Template for Generator skills
│       ├── reviewer.md               — Template for Reviewer skills
│       ├── inversion.md              — Template for Inversion skills
│       ├── pipeline.md               — Template for Pipeline skills
│       └── combined.md               — Template for multi-pattern skills
├── README.md
├── CLAUDE.md
├── LICENSE
└── .gitignore
```

---

## Environment Support

The core workflow (interview → pattern classification → scaffolding) works in **all environments**. The only difference is how companion files (templates, pattern definitions) are loaded.

| Environment | Multi-file auto-loading | Notes |
|---|---|---|
| **Claude Code** | Yes | Reads `references/` automatically |
| **Claude.ai / Cowork** | Yes | All features work |
| **Google Antigravity** | Yes | Reads multi-file skill directories |
| **Cursor** | No | Paste `SKILL.md` as project rule; reference templates manually |
| **Windsurf** | No | Paste `SKILL.md` as custom rule; reference templates manually |
| **Cline** | No | Paste `SKILL.md` as custom instructions; reference templates manually |
| **GitHub Copilot** | No | Use as custom instructions |

For tools without multi-file auto-loading, the AI will still guide you through the full interview and pattern classification. When it needs a template, you can paste the relevant file content from `references/templates/` into the conversation.

---

## Contributing

Contributions welcome! Some ideas:

- Add new pattern templates or improve existing ones
- Share skills you've built with skill-architect (open an issue!)
- Improve installation instructions for specific environments

---

## Credits

This project stands on the shoulders of two key contributions:

**Google ADK Team** — The 5 Agent Skill Design Patterns (Tool Wrapper, Generator, Reviewer, Inversion, Pipeline) that form the structural foundation of this skill were introduced by the Google ADK team. Their framework for thinking about *how* skills should work internally — not just what they produce — is what makes pattern-aware skill design possible.
- [5 Agent Skill design patterns every ADK developer should know](https://developers.google.com/adk)

**Anthropic** — The skill-creation workflow (interview → scaffold → test → iterate) and the SKILL.md format are based on Anthropic's [skill-creator](https://github.com/anthropics/claude-skills) from the Claude Skills project. skill-architect extends this workflow by adding a pattern classification step before scaffolding.

> **Disclaimer:** This is an independent community project inspired by publicly available resources from Google and Anthropic. It is not affiliated with, endorsed by, or maintained by Google or Anthropic. Any errors or issues in this project are solely the responsibility of the maintainers, not of Google, Anthropic, or their respective teams.

---

## License

[MIT](LICENSE) — use freely, attribution appreciated.
