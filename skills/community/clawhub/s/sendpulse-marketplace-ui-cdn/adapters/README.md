# Installing this skill in different AI tools

The skill core is plain Markdown and plain files — `SKILL.md`, `references/`, `examples/` —
so any LLM-based tool can use it. What differs between tools is how much of it survives:

| Tool | Steps 0–5 (wiring, tokens, components, layout, theming) | Step 6 (gaps) | Step 7 (checkers) |
|---|---|---|---|
| Claude Code / Desktop, Cursor, any agent with a shell | full | full | full — the scripts run |
| ChatGPT, Gemini gems, any chat window | full, via the condensed instructions here | full, if `gaps.md` is uploaded | the manual checklist only |

Pick your platform:

## Claude Code / Claude Desktop (native)

The skill lives in the `sendpulse-skills` monorepo. Clone it once, then copy (or
symlink) this skill's folder into your skills directory:

```bash
git clone https://github.com/sendpulse/sendpulse-skills

# User-level (all your projects):
cp -R sendpulse-skills/sendpulse-marketplace-ui-cdn ~/.claude/skills/
# Or project-level (shared with the team via git):
cp -R sendpulse-skills/sendpulse-marketplace-ui-cdn .claude/skills/
```

(On macOS/Linux a symlink instead of `cp -R` means a plain `git pull` in the clone
updates the skill in place.) The folder name must stay `sendpulse-marketplace-ui-cdn`.
Claude discovers `SKILL.md` automatically and activates it when the conversation matches
its description. Nothing in this `adapters/` folder is read on that path.

**Claude.ai upload:** zip the folder, then *Settings → Capabilities → Skills → Upload skill*.

## ChatGPT (Custom GPT or Projects)

1. Create a Custom GPT (or a Project).
2. Paste the part of [`chatgpt/instructions.md`](chatgpt/instructions.md) below its rule
   into *Instructions*. It is 7.9k characters — inside the field's 8000-character limit,
   with little headroom, so trim something if you add anything.
3. Upload as *Knowledge*, in this order of value:
   [`chatgpt/pocket-guide.md`](chatgpt/pocket-guide.md) (icon rules, the palette, the known
   gaps and the pre-delivery checklist — the detail the instruction field could not hold,
   and the file the paste block tells the model to read), `references/classes.txt`,
   `references/icons.txt`, `references/components.md`, `references/gaps.md`,
   `references/tokens.md`, `references/tokens.css`, `references/bundle-fixes.css`,
   `references/starter.html`, `references/kitchen-sink.html`,
   `examples/settings-screen.html`, `examples/amazon-connections-screen.html`.

`classes.txt` and `icons.txt` are the two that matter most and the two people skip. The
grep workflow the skill is built on — *does the bundle define this name, or am I inventing
it?* — becomes a file-search question against those two files, and it is the single check
that most reliably keeps a screen looking like SendPulse.

## Gemini (gems / gemini-cli)

- **gemini-cli**: copy [`gemini/GEMINI.md`](gemini/GEMINI.md) into your project root
  (or merge into an existing `GEMINI.md`), and keep the skill folder in the repo so the
  reference paths resolve.
- **Gemini gems**: paste [`chatgpt/instructions.md`](chatgpt/instructions.md) as the gem
  instructions (not `SKILL.md` — the condensed version assumes no file access) and attach
  the same files listed above, `pocket-guide.md` included.

## Cursor

Copy [`cursor/sendpulse-marketplace-ui.mdc`](cursor/sendpulse-marketplace-ui.mdc) into
your project's `.cursor/rules/`, and keep the whole skill folder somewhere the rule can
reference (the rule assumes `docs/sendpulse-marketplace-ui-cdn/`; adjust the path inside
the file if you put it elsewhere). Cursor has a shell, so the Step 7 checkers work there.

## GitHub Copilot

Copy [`copilot/copilot-instructions.md`](copilot/copilot-instructions.md) into
`.github/copilot-instructions.md` in your repo, and keep the skill folder in the repo so the
reference paths resolve (it assumes `docs/sendpulse-marketplace-ui-cdn/`; adjust the path inside
the file if you put it elsewhere). Copilot has a shell, so the Step 7 checkers work there.

## Any other AI tool

This covers **DeepSeek chat**, a plain API system prompt, or any tool with no file/Knowledge
support at all — the same instructions apply there as to any file-free chat window.

1. **Paste**: [`chatgpt/instructions.md`](chatgpt/instructions.md) is the version to paste
   into a system prompt or custom-instructions field — it needs no filesystem. With nothing to
   upload, paste the **whole file**, including the two sections after the `---`: the fallback
   class list and the fallback palette/gaps table cover what the main block otherwise delegates
   to `pocket-guide.md`/`classes.txt` in Knowledge. `SKILL.md` is the version for a tool that can
   open files, and is always the fuller one.
2. **Link**: if the tool can browse, give it
   `https://raw.githubusercontent.com/sendpulse/sendpulse-skills/main/sendpulse-marketplace-ui-cdn/SKILL.md`
   and let it follow the relative links.

## A note on drift

`chatgpt/instructions.md`, `chatgpt/pocket-guide.md`, `gemini/GEMINI.md` and the Cursor rule
are **derived** from `SKILL.md`. They deliberately carry only the slow-moving facts — the non-negotiables, the
metrics, the control widths, the frame and theme rules — and never the generated lists, so
`references/refresh.sh` can update `classes.txt` and `icons.txt` without touching them.
When one of those slow-moving numbers does change in `SKILL.md`, change it here in the same
commit.

## Updating

`git pull` in the monorepo clone, then re-copy the skill folder (not needed for symlinked
installs); re-upload the Knowledge files for ChatGPT/gems. Class and icon lists go stale
independently of the skill — `references/refresh.sh` re-derives them from the live CDN.
