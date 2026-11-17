**English** | [简体中文](README.zh.md)

# unppt-skill

An AI assistant skill for [unppt](https://github.com/spitmaster/unppt) — teach AI coding assistants (WorkBuddy, Claude Code, Cursor, etc.) to **convert PowerPoint decks (.pptx) into web pages**: via CLI or code, batch conversion, font checking, iframe embedding, and JS-controlled playback.

With this skill installed, just tell the AI:

- "Convert this PPT into a web page"
- "Turn demo.pptx into a single self-contained HTML file I can send as an attachment"
- "Batch-convert these courseware files for our website"
- "Check whether this PPT has font problems"
- "Embed this deck in my page with prev/next buttons"

The AI follows the workflow in `SKILL.md` to pick the right output form, run the conversion, surface font issues, and automatically loads the detailed references under `references/` when advanced tasks (embedding/control, cloud-function deployment) come up.

> **Input format**: direct input is `.pptx` (OOXML). Legacy binary `.ppt` files are not supported by the converter itself — save them as `.pptx` in PowerPoint first (File → Save As); the skill teaches the AI to guide users through this, including batch conversion via PowerPoint COM automation on Windows.

## Repository layout

```
unppt-skill/
├── SKILL.md                    # Skill entry: environment, output-form decision, common tasks, key rules
├── references/
│   ├── cli.md                  # Every CLI option, unppt check, how fonts work
│   ├── api.md                  # convert()/checkFonts() JS API, write callback, big files, 4 runnable examples
│   └── embedding.md            # iframe, postMessage protocol, UnpptFrame, native apps, live-class sync
└── scripts/
    └── batch-convert.mjs       # Batch-conversion script, ready to run
```

Skill content is based on **unppt 0.3.2** and maintained alongside upstream releases.

## Install

Prerequisite: [Node.js](https://nodejs.org/) ≥ 20.12 on the machine that converts (the AI will run `npm install -g @unppt/unppt` as part of the skill workflow).

### WorkBuddy

User-level (available in all projects):

```bash
git clone https://github.com/spitmaster/unppt-skill.git "%USERPROFILE%\.workbuddy\skills\unppt"
```

Or project-level (shared with your team via the repo):

```bash
git clone https://github.com/spitmaster/unppt-skill.git .workbuddy/skills/unppt
```

### Claude Code

```bash
# user-level
git clone https://github.com/spitmaster/unppt-skill.git ~/.claude/skills/unppt
# or project-level
git clone https://github.com/spitmaster/unppt-skill.git .claude/skills/unppt
```

### Cursor

```bash
git clone https://github.com/spitmaster/unppt-skill.git .cursor/skills/unppt
```

### Other AI tools that follow the SKILL.md convention

Clone this repo into that tool's skills directory (the folder name `unppt` is the skill name). The skill is plain text plus one script — no build step needed.

> Manual install (no git): download the [ZIP](../../archive/refs/heads/main.zip), extract, rename the extracted folder to `unppt`, and drop it into your tool's skills directory.

## Verify

After installing, ask the AI to "convert a PPT to a web page" (or mention unppt) and check that it triggers the unppt skill and follows the workflow. You can also run the batch script directly:

```bash
npm install @unppt/unppt
node scripts/batch-convert.mjs <pptx-dir> <output-dir>
```

## Links

- unppt main repo: <https://github.com/spitmaster/unppt>
- npm: <https://www.npmjs.com/package/@unppt/unppt>
- unppt documentation (the source this skill distills): [docs/en](https://github.com/spitmaster/unppt/tree/main/docs/en)

## License

[Apache-2.0](LICENSE). Skill content is distilled from the unppt project's documentation (Apache-2.0).
