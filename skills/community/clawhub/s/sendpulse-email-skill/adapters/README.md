# Installing this skill in different AI tools

The skill core is plain Markdown (`SKILL.md` + `references/` + `examples/`), so any
LLM-based tool can use it. Pick your platform:

## Claude Code / Claude Desktop (native)

The skill lives in the `sendpulse-skills` monorepo. Clone it once, then copy (or
symlink) this skill's folder into your skills directory:

```bash
git clone https://github.com/sendpulse/sendpulse-skills

# User-level (all your projects):
cp -r sendpulse-skills/sendpulse-email-skill ~/.claude/skills/
# Or project-level (shared with the team via git):
cp -r sendpulse-skills/sendpulse-email-skill .claude/skills/
```

(On macOS/Linux a symlink instead of `cp -r` means a plain `git pull` in the clone
updates the skill in place.) Claude discovers `SKILL.md` automatically and
activates it when the conversation matches its description.

**Recommended companions** (install alongside for full email coverage):
`sendpulse-template-skill` (builds the email HTML) and `sendpulse-smtp-skill`
(transactional email). This skill hands off to them instead of duplicating.

## Cursor

Copy [`cursor/sendpulse-email.mdc`](cursor/sendpulse-email.mdc) into your project's
`.cursor/rules/` directory, and clone the whole skill somewhere the rule can
reference (the rule assumes `docs/sendpulse-email-skill/`; adjust the path inside
the file if you put it elsewhere).

## ChatGPT (Custom GPT or Projects)

1. Create a Custom GPT (or a Project).
2. Paste the contents of [`chatgpt/instructions.md`](chatgpt/instructions.md) into
   *Instructions*.
3. Upload all files from `references/` and `examples/` as *Knowledge*.

## Gemini (gems / gemini-cli)

- **gemini-cli**: copy [`gemini/GEMINI.md`](gemini/GEMINI.md) into your project root
  (or merge into an existing `GEMINI.md`), keep the skill folder in the repo so the
  references resolve.
- **Gemini gems**: paste `SKILL.md` as the gem instructions, attach the reference
  files.

## GitHub Copilot

Copy the "Critical rules" section of `SKILL.md` into
`.github/copilot-instructions.md`, or keep the skill folder in the repo and
reference it from there.

## Any other AI tool

1. **Paste**: `SKILL.md` alone covers the common cases — paste it into the system
   prompt / custom instructions; add reference files as needed.
2. **Link**: if the tool can browse, give it
   `https://raw.githubusercontent.com/sendpulse/sendpulse-skills/main/sendpulse-email-skill/SKILL.md`
   and let it follow the relative links.

## Updating

`git pull` in the monorepo clone, then re-copy the skill folder (not needed for
symlinked installs); re-upload for ChatGPT/gems. The skill also self-checks the
published `VERSION` when it has web access and reminds the user when a newer
release exists.
