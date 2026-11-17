# Harness Demos

Each harness should prove the same thing: a local JSON spec becomes a checked artifact plus a receipt. Keep the demo small enough to paste into an agent task.

## OpenClaw

```bash
openclaw skills install visual-architecture
python3 ~/.openclaw/workspace/skills/visual-architecture/scripts/render_architecture.py deliver \
  ~/.openclaw/workspace/skills/visual-architecture/examples/showcase-visual-architecture-case-study.json \
  /tmp/visual-architecture-case-study.html --json
```

## Codex

```text
Use the visual-architecture skill. Validate examples/showcase-visual-architecture-case-study.json, deliver HTML, then report the receipt quality score and evidence count.
```

## Claude Code

```text
Read SKILL.md, run the validate command against examples/showcase-pr-delta.json, then deliver examples/showcase-pr-delta.html with a receipt.
```

## OpenCode

```text
Install or copy this repo as a local skill, then run make examples and make validate before citing any generated artifact.
```

A harness demo is not accepted unless it reports the generated receipt path, input/output SHA-256 hashes, quality rating, and evidence count.
