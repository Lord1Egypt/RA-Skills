# visual-dna

[![Validate](https://github.com/LeoStehlik/visual-dna/actions/workflows/validate.yml/badge.svg)](https://github.com/LeoStehlik/visual-dna/actions/workflows/validate.yml)

Extract a visual identity from screenshots, images, or URLs, turn it into structured Design DNA JSON, then reuse that DNA to generate matching UI.

The skill captures three layers:

| Layer | What it records |
| --- | --- |
| `design_system` | Colour, typography, spacing, layout, shape, elevation, motion, and component rules |
| `design_style` | Mood, composition, visual language, brand voice, and interaction personality |
| `visual_effects` | Canvas, WebGL, particles, shaders, scroll effects, SVG animation, and other rendering details |

Inspired by [zanwei/design-dna](https://github.com/zanwei/design-dna), adapted as an OpenClaw/Codex-friendly skill workflow.


## Activation Boundary

Use `visual-dna` for explicit visual identity extraction, reference-style analysis, brand/design-system capture, or generation from an existing Design DNA JSON. Do not route generic UI tasks through it unless the user supplied references or asked to match a reference.

When URLs or assets are supplied, the skill uses the references the user provided or assets already present in the project. It reports which references were used, but it does not try to judge ownership, sensitivity, or permission to analyze a reference; that remains a human decision.

## Install

### OpenClaw / ClawHub

```bash
openclaw skills install visual-dna
```

### Manual

```bash
git clone https://github.com/LeoStehlik/visual-dna.git ~/.openclaw/workspace/skills/visual-dna
```

For Claude Code, Codex, or other agent harnesses, copy this folder into the harness skill directory and load `SKILL.md`.

## Use

```text
Analyse this website and extract its Design DNA: https://example.com
```

```text
I have this Design DNA JSON. Build a dashboard for this content in the same style.
```

```text
Extract the design DNA from this screenshot and generate a matching landing page.
```

## Proof Artifact

The repo includes [`examples/sample-design-dna.json`](examples/sample-design-dna.json), a complete sample profile that follows the schema described in [`references/schema.md`](references/schema.md).

Validate it locally:

```bash
make validate
```

The GitHub Actions workflow runs the same checks on every push:

- `SKILL.md` declares `name: visual-dna`
- README includes the ClawHub install command
- the sample Design DNA JSON parses cleanly
- the sample includes the required top-level sections: `meta`, `design_system`, `design_style`, and `visual_effects`

## Why It Exists

"Make it look like this" is not a stable spec. Design DNA turns a reference into a reusable, reviewable JSON asset.

Once extracted, the DNA can be:

- committed to version control
- reused across prompts, agents, and projects
- refined as the brand evolves
- paired with [no-slop-ui](https://github.com/LeoStehlik/no-slop-ui) so the generated UI stays faithful without drifting into generic AI defaults

## Repository

```text
visual-dna/
├── SKILL.md
├── examples/
│   └── sample-design-dna.json
├── references/
│   ├── generation-guide.md
│   └── schema.md
├── .github/workflows/
│   └── validate.yml
├── Makefile
└── README.md
```

## Status

Usable public skill bundle, published on ClawHub as `visual-dna@0.2.2`.

## License

MIT. See [LICENSE](LICENSE).
