# Installing this skill in different AI tools

The skill core is plain Markdown (`SKILL.md` + `references/` + `examples/`), so
any LLM-based tool can use it. Pick your platform:

## Claude Code / Claude Desktop (native)

The skill lives in the `sendpulse-skills` monorepo. Clone it once, then copy (or
symlink) this skill's folder into your skills directory:

```bash
git clone https://github.com/sendpulse/sendpulse-skills

# User-level (all your projects):
cp -r sendpulse-skills/sendpulse-smtp-skill ~/.claude/skills/
# Or project-level (shared with the team via git):
cp -r sendpulse-skills/sendpulse-smtp-skill .claude/skills/
```

(On macOS/Linux a symlink instead of `cp -r` means a plain `git pull` in the clone
updates the skill in place.) Claude discovers `SKILL.md` automatically and
activates it when the conversation matches its description.

## Cursor

Copy [`cursor/sendpulse-smtp.mdc`](cursor/sendpulse-smtp.mdc) into your project's
`.cursor/rules/` directory, and clone the whole skill somewhere the rule can
reference (the rule assumes `docs/sendpulse-smtp-skill/`; adjust the path inside
the file if you put it elsewhere).

## ChatGPT (Custom GPT or Projects)

1. Create a Custom GPT (or a Project).
2. Paste the contents of [`chatgpt/instructions.md`](chatgpt/instructions.md)
   into *Instructions*.
3. Upload all files from `references/` and `examples/` as *Knowledge*.

## Gemini (gems / gemini-cli)

- **gemini-cli**: copy [`gemini/GEMINI.md`](gemini/GEMINI.md) into your project
  root (or merge into an existing `GEMINI.md`), and keep the skill folder in the
  repo so the file references resolve.
- **Gemini gems**: paste `SKILL.md` as the gem instructions and attach the
  reference files.

## GitHub Copilot

Add the key rules to `.github/copilot-instructions.md`, or keep the skill folder
in the repo and reference it: copy the "Critical rules" section of `SKILL.md`
into your instructions file.

## Any other AI tool

Two universal options:

1. **Paste**: `SKILL.md` alone is self-sufficient for the common cases — paste it
   into the system prompt / custom instructions. Add reference files as needed.
2. **Link**: if the tool can browse, give it
   `https://raw.githubusercontent.com/sendpulse/sendpulse-skills/main/sendpulse-smtp-skill/SKILL.md`
   and let it follow the relative links to `references/`.

## Updating

Every copy is a snapshot. To update: `git pull` in the monorepo clone and re-copy
the skill folder (not needed for symlinked installs), or re-download and re-upload
(ChatGPT/gems). The skill itself checks the published `VERSION` file when it has
web access and will remind the user when a newer release exists.
