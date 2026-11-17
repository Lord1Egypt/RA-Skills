# SynOmega Skill

An agent **Skill** for [SynOmega](https://github.com/zbc0315/synomega) — the
retrosynthesis and reaction-prediction toolkit on PyPI
([docs](https://zbc0315.github.io/synomega/)). It teaches Claude Code, OpenClaw and
other coding agents to use the `synomega` Python package across its **six
capabilities**: single-step retrosynthesis (product → reactants), single-step
forward prediction (reactants → product), multi-step route planning, a continuous
**synthesizability score** (SynScore), reaction-plausibility screening, and
multi-component evolution (growing a forward synthesis network from a set of
reactants).

The skill runs synomega **locally** — `pip install synomega` plus a trained model
and a building-block file. It does not depend on any hosted service.

## Install

**OpenClaw / ClawHub**

```bash
clawhub install synomega
```

**Claude Code (manual)**

```bash
mkdir -p ~/.claude/skills/synomega
curl -fsSL https://raw.githubusercontent.com/zbc0315/synomega-skill/main/SKILL.md \
  -o ~/.claude/skills/synomega/SKILL.md
curl -fsSL https://raw.githubusercontent.com/zbc0315/synomega-skill/main/scripts/synomega_run.py \
  -o ~/.claude/skills/synomega/synomega_run.py
```

## Prerequisites

```bash
pip install "synomega[gnn]"        # the package (neural backend)
```

That's it — **it works out of the box**. The default pretrained model and
building-block stock download automatically on first use (into
`~/.cache/synomega`); run `synomega download` to pre-fetch them. Downloads come
from the nearest mirror (USTC GitLab in China, or GitHub), auto-selected by
latency. To use your own checkpoint/stock instead, set `SYNOMEGA_MODEL` /
`SYNOMEGA_STOCK`.

## Use

Ask your agent things like:

- "Can *paracetamol* be synthesized? How hard?"
- "Propose a synthesis route for `CC(=O)Nc1ccccc1O`."
- "What reactants could give this molecule in one step?"
- "What product do acetic acid and benzylamine give?"
- "Evolve a forward network from acetophenone + formaldehyde + dimethylamine."

Or call the bundled helper directly (one JSON-printing command per capability):

```bash
python scripts/synomega_run.py single-step  "CC(=O)Nc1ccccc1O" --top-k 10     # product -> reactants
python scripts/synomega_run.py forward      "CC(=O)O.NCc1ccccc1" --top-k 5    # reactants -> product
python scripts/synomega_run.py plan         "CC(=O)Nc1ccccc1O" --max-depth 5  # multi-step route
python scripts/synomega_run.py score        "CC(=O)Nc1ccccc1O" --max-steps 5  # synthesizability (SynScore)
python scripts/synomega_run.py evolve       "CC(=O)c1ccccc1.C=O.CNC" --max-depth 3 --score-threshold 0.01
```

`plan` and `score` take `--exclude-target` (treat the target as not purchasable
even if it is a catalogue molecule, so it is not trivially "solved" in zero steps).
Reaction-plausibility screening is an env toggle: `SYNOMEGA_PLAUSIBILITY=1`. See
`SKILL.md` for the full option list and output shapes.

## Contents

| File | Purpose |
|---|---|
| `SKILL.md` | the skill definition (frontmatter + instructions) |
| `scripts/synomega_run.py` | loads model + stock from env vars, runs any capability (single-step / forward / plan / score / evolve), prints JSON |

## Related

- Toolkit: https://github.com/zbc0315/synomega · https://pypi.org/project/synomega/
- Online demo (browser instance): synomega-web

## License

MIT — see [LICENSE](LICENSE).
