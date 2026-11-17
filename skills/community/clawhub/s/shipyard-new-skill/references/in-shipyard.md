# Adding a skill to Shipyard

Work on a branch, never on `main`.

1. `skills/<name>/SKILL.md` with `name: <name>` and a description ending in its trigger phrases and the skill's own slash command (look at the other skills). Detail in `skills/<name>/references/`. Follow the other skills: "Rules (always)", numbered steps, plain English, no em dashes.
2. Add `<name>` to `SKILLS` in `scripts/agents/core.mjs` and in `tests/agents-install.test.mjs`. That puts it in the Codex and Cursor copy (`~/.agents/skills/shipyard-<name>`).
3. The copy may not hold Claude Code only wording (`LINT_RULES` in `core.mjs` lists it: agent and model names, slash commands of one agent, and so on). The plugin root variable and the skills' slash commands are rewritten for you. Anything else gets a row in `scripts/agents/rewrites.mjs` that replaces that exact text.
4. A new script goes in `scripts/`, with `--help` and `--json`, and a test in `tests/`. Every Shipyard script command in a skill must be one the key guard trusts; the pack tests check it.
5. Bump `version` in the manifest in `.claude-plugin/`, add the skill to the README (what is in this release, the table of what to type) and a "What changed in" section.
6. Run `node --test tests/*.test.mjs` and `node --test template/tests/*.test.mjs`. Both must pass before the pull request.
