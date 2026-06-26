# vue-to-umijs

Cursor **Agent Skill** for migrating **Vue 2/3** codebases to **Umi 4 (`@umijs/max`) + React 18 + antd**: routing and data-flow conventions, constraints, stack mapping, and Vue→React syntax examples.

The authoritative instructions for the agent live in [`SKILL.md`](SKILL.md). This file is for humans installing or publishing the skill.

## Contents

- Scope, principles, API mapping (Vue Router / Pinia → Umi + hooks)
- Constraints (single router tree, request layer, i18n, env, forms/tables)
- Pre-release checklist
- Syntax examples (state, lists, controlled inputs, emits, computed/watch, cleanup, route params, dependency patterns)

## Requirements

- Cursor with **Agent Skills** support (see [Cursor docs — Agent Skills](https://cursor.com/docs/skills))
- Target stack as described in `SKILL.md`: Umi 4, `@umijs/max`, React 18, antd, Less + CSS Modules

## Install

**Folder name must stay `vue-to-umijs`** (matches the `name` field in `SKILL.md` frontmatter).

### Option A — Git clone (local skills directory)

Clone this repository, then symlink or copy the skill folder:

| Scope   | Typical path                         |
| ------- | ------------------------------------ |
| User    | `~/.cursor/skills/vue-to-umijs`      |
| Project | `<repo>/.cursor/skills/vue-to-umijs` |

Restart Cursor or reload the window so skills are discovered.

### Option B — Remote rule from GitHub (team share)

1. Open **Cursor Settings → Rules**
2. **Add Rule → Remote Rule (GitHub)**
3. Paste the **repository URL** that contains this folder at the repo root (or the path your team uses)

Details may vary by Cursor version; if the UI only accepts a repo root, keep this skill at the **root of the repository** as `vue-to-umijs/SKILL.md`, or publish a repo that only contains this skill.

### Use in chat

- The agent may apply the skill when the task matches the `description` in frontmatter.
- Or invoke explicitly: **`/vue-to-umijs`**

## Repository layout

```text
vue-to-umijs/
├── SKILL.md      # Skill body (required)
├── README.md     # This file
└── LICENSE       # MIT
```

Optional extras supported by the [Agent Skills](https://cursor.com/docs/skills) convention: `scripts/`, `references/`, `assets/` — add if you split content out of `SKILL.md` later.

## License

MIT — see [LICENSE](LICENSE).

## See also

- [UmiJS documentation](https://umijs.org/)
- [Agent Skills standard](https://agentskills.io/)
