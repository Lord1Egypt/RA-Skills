# Visual Explainer for OpenClaw

OpenClaw skill adaptation of [nicobailon/visual-explainer](https://github.com/nicobailon/visual-explainer).

Generate beautiful, self-contained HTML pages that visually explain systems, code changes, plans, and data tables instead of ASCII art. Includes interactive Mermaid diagrams, responsive CSS layouts, and magazine-quality slide deck generation.

## Credit

This is an OpenClaw adaptation of the excellent [visual-explainer](https://github.com/nicobailon/visual-explainer) tool by [@nicobailon](https://github.com/nicobailon). The original tool supports Claude Code, Pi, and OpenAI Codex. This version adapts it for OpenClaw's tool system and workspace conventions.

**Original repository:** https://github.com/nicobailon/visual-explainer  
**Original author:** nicobailon  
**Adaptation by:** Tommy (tommy-openclaw)

All core functionality (HTML generation, Mermaid diagrams, CSS patterns, slide deck engine) comes from the original work. This adaptation adds OpenClaw-specific integration (skill.json, workspace paths, exec tool patterns).

## What's Different in This Adaptation

- **OpenClaw skill structure** (`skill.json`, compatible with ClawHub)
- **Workspace integration** (outputs to `~/.openclaw/workspace/diagrams/`)
- **Prompt templates** (converted slash commands to `./prompts/*.md`)  
- **macOS browser opening** (`exec open` instead of external dependencies)
- **Updated file paths** (OpenClaw workspace conventions)

The visual generation capabilities, templates, and references are preserved from the original.

## Installation

### Via ClawHub (recommended)
```bash
clawhub install visual-explainer-openclaw
```

### Manual Installation
```bash
git clone https://github.com/keylimesoda/visual-explainer-openclaw.git ~/.openclaw/skills/visual-explainer
```

## Usage

See `SKILL.md` for full documentation. Key prompt templates:

- `./prompts/generate-web-diagram.md` — Any visual diagram
- `./prompts/diff-review.md` — Code review with visual comparison  
- `./prompts/generate-slides.md` — Magazine-quality slide decks
- `./prompts/project-recap.md` — Context-switching summaries

## Example Output

Generates self-contained HTML files with:
- Interactive Mermaid diagrams (zoom, pan, dark/light themes)
- Responsive CSS Grid layouts  
- Typography optimized for technical content
- No build dependencies (works offline)

## License

MIT (same as original)

## Acknowledgments

Huge thanks to [@nicobailon](https://github.com/nicobailon) for creating the original visual-explainer tool. This adaptation wouldn't exist without their excellent work on the HTML generation engine, CSS patterns, and slide deck system.

If you're using Claude Code, Pi, or OpenAI Codex, use the [original tool](https://github.com/nicobailon/visual-explainer) instead — it's designed specifically for those platforms.