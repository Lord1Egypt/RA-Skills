---
name: synomega
description: >-
  Retrosynthesis, reaction prediction, and synthesizability for organic molecules,
  using the synomega Python package (pip install synomega) — runs locally, works
  out of the box. Six capabilities: single-step retrosynthesis (product → reactants,
  candidate disconnections), single-step forward reaction prediction / reaction
  outcome (reactants → product), multi-step route planning down to purchasable
  building blocks, a continuous synthesizability / makeability score (SynScore),
  reaction-plausibility screening, and multi-component evolution (growing a forward
  synthesis network from a set of reactants, e.g. one-pot / multicomponent
  chemistry). Use this whenever the user gives a molecule (as SMILES or a resolvable
  name) and asks how to make / synthesize it, whether it can be made or how hard,
  how to rank molecules by ease of synthesis, what reactants give a target, what
  product a set of reactants gives, a reaction outcome, or how a reactant mixture
  evolves — i.e. for retrosynthesis, synthesis planning, cheminformatics, and
  reaction-prediction tasks. Safety judgments for hazardous, controlled, or
  otherwise dual-use compounds are deferred to the host's safety policy (see
  "Safety boundary / dual-use" below).
---

# SynOmega

SynOmega is a **Python package** ([PyPI](https://pypi.org/project/synomega/),
[docs](https://zbc0315.github.io/synomega/)) for organic small-molecule reactions.
It exposes **six capabilities** behind one install:

| # | Capability | Direction | Helper command |
|---|---|---|---|
| 1 | **Single-step retrosynthesis** | product → reactants | `single-step` |
| 2 | **Single-step forward prediction** | reactants → product | `forward` |
| 3 | **Multi-step route planning** | target → route to purchasable stock | `plan` |
| 4 | **Synthesizability score (SynScore)** | target → 0–1 makeability | `score` |
| 5 | **Reaction-plausibility screening** | filter single-step candidates | env toggle |
| 6 | **Multi-component evolution** | reactant set → forward synthesis network | `evolve` |

It runs entirely locally. **It works out of the box** — the pretrained models and
building-block stock download automatically on first use, so there is nothing to
train or configure.

> ⚠️ **Network + disk notice (first use downloads a few hundred MB).** The first
> call automatically reaches out to a **remote mirror** (USTC GitLab and/or GitHub)
> and downloads the model(s) and stock — **a few hundred MB** — into
> `~/.cache/synomega`. Nothing else phones home, but this first fetch does.
> Controls: pre-fetch with `synomega download`; change the cache dir with
> `SYNOMEGA_CACHE`; pick a mirror with `SYNOMEGA_MIRROR` (`ustc` or `github`). In
> **air-gapped, bandwidth-limited, privacy-sensitive, or reproducibility-critical**
> environments, pre-fetch (or point at a local model/stock) and treat the download
> as an explicit opt-in rather than a surprise.

## Install

```bash
pip install "synomega[gnn]>=0.9.4"    # neural D-MPNN backend (torch) — recommended
synomega download              # optional: pre-fetch the default assets
```

Requires Python ≥ 3.10.

## Fastest path: the bundled helper

`scripts/synomega_run.py` prints JSON for every operation — no configuration, it
downloads what it needs on first call. Always pass a valid **SMILES** (dot-separate
multiple molecules).

```bash
# 1. single-step retrosynthesis — "what reacts to give X?"
python scripts/synomega_run.py single-step "CC(=O)Nc1ccccc1O" --top-k 10

# 2. forward prediction — "what do these reactants give?"
python scripts/synomega_run.py forward "CC(=O)O.NCc1ccccc1" --top-k 5

# 3. multi-step route planning — "how do I make X?"
python scripts/synomega_run.py plan "CC(=O)Nc1ccccc1O" --max-depth 5

# 4. synthesizability score — "can X be made / how hard?"  (simplify model by default)
python scripts/synomega_run.py score "CC(=O)Nc1ccccc1O" --max-steps 5

# 6. multi-component evolution — grow a forward synthesis network
python scripts/synomega_run.py evolve "CC(=O)c1ccccc1.C=O.CNC" --max-depth 3 --score-threshold 0.01
```

(Capability 5, reaction plausibility, is an env toggle applied to the others — see
below.)

## The six capabilities

### 1. Single-step retrosynthesis — `single-step`

Given a **product**, rank one-step disconnections into candidate **reactants**.

```bash
python scripts/synomega_run.py single-step "CC(=O)Nc1ccccc1O" --top-k 10
```

Output: `{"target", "predictions": [{"rank", "reactants": [SMILES,...], "score"
(0–1, higher = more likely), "plausibility" (null unless screening is on),
"template_id"}]}`. Present the top few disconnections.

### 2. Single-step forward prediction — `forward`

Given **reactants**, rank the likely **products**. Uses a separate forward model.

```bash
python scripts/synomega_run.py forward "CC(=O)O.NCc1ccccc1" --top-k 5
```

Output: `{"reactants", "products": [{"rank", "product" (SMILES), "score" (0–1
forward probability), "template_id"}]}`. Template-based (product top-1 ≈ 0.64):
treat products as candidates, not guarantees.

### 3. Multi-step route planning — `plan`

Search an AND-OR graph for a full route from the **target** down to purchasable
building blocks.

```bash
python scripts/synomega_run.py plan "CC(=O)Nc1ccccc1O" --max-depth 5
python scripts/synomega_run.py plan "CC(=O)Nc1ccccc1O" --simplify   # cheaper search
python scripts/synomega_run.py plan "CC(=O)Nc1ccccc1O" --library molport  # MolPort stock
python scripts/synomega_run.py plan "CC(=O)Nc1ccccc1O" --forward-consistency
```

Output: `{"target", "algorithm", "solved" (bool — a fully-purchasable route
exists), "routes": [route tree, best first]}`. Each route tree nests
`reactants → product` recursively until every leaf is an in-stock building block;
read it top-down. Options: `--algorithm {retrostar,mcts,bfs}`, `--max-routes`,
`--exclude-target`, `--simplify`, `--forward-consistency` (with `--forward-top-k`,
default 3 — keep a single-step candidate only if its retro template is in the
forward model's top-k for its reactants; prunes forward-implausible disconnections).

### 4. Synthesizability score (SynScore) — `score`

Score a **target** 0–1 for how makeable it is, for ranking a set of molecules.
Runs one route search internally, then folds it into a score.

```bash
python scripts/synomega_run.py score "CC(=O)Nc1ccccc1O" --max-steps 5
python scripts/synomega_run.py score "CC(=O)Nc1ccccc1O" --original   # unconstrained model
```

Output (a `MoleculeReport` dict): the headline is **`score`** = `1/(U+1)**U`, where
`U` is the number of the best route's starting materials that are **not**
purchasable. Solved (U=0) → 1.0; U=1 → 0.5; U=2 → 0.11; no route → 0. Also:
`solved`, `bb_coverage` (fraction of leaves purchasable), `min_steps`,
`num_leaves`, `num_purchasable_leaves`. Use `score` to rank candidates; use
`solved` to compare against published solve-rate. **Defaults to the
simplification-constrained model @ expansion width 10** (synomega's recommended
scoring config); `--original` reverts to the unconstrained model.

### 5. Reaction-plausibility screening — env toggle

An optional **mapping-free dual-tower model** scores how likely each single-step
candidate's `reactants → target` actually happens, and **drops** implausible ones
(it only removes wrong disconnections, never re-ranks the rest). It applies to
`single-step`, `plan`, and `score` alike. **Off by default** — it does not improve
top-k recall and adds latency.

```bash
SYNOMEGA_PLAUSIBILITY=1 SYNOMEGA_PLAUSIBILITY_THRESHOLD=0.4 \
  python scripts/synomega_run.py single-step "CC(=O)Nc1ccccc1O" --top-k 10
```

When on, each `single-step` prediction gains a `plausibility` field (0–1). In
Python: `synomega.load_default_planner(plausibility=True, plausibility_threshold=0.4)`.

### 6. Multi-component evolution — `evolve`

From a set of starting **reactants**, repeatedly pick two molecules from a growing
pool, run the forward model, and add products back — growing a forward **synthesis
network**. Good for exploring multi-component / one-pot chemistry.

```bash
python scripts/synomega_run.py evolve "CC(=O)c1ccccc1.C=O.CNC" \
  --max-depth 3 --score-threshold 0.01 --top 20
```

Output: `{"reactants", "stats", "num_molecules", "num_reaction_edges",
"molecules": [{"smiles", "total_score", "depth", "step_score", "parents",
"template_id"}]}`. Each molecule's `total_score` = `min(parent totals) × step
probability` (starting reactants = 1.0); `depth` is the synthesis-tree depth.
Options: `--forward-top-k` (products per pair), `--frontier-width` (cap fan-out for
many reactants), `--top` (how many products to report). In Python,
`MultiComponentEvolution(...).evolve([...])` also supports `mode="disk"` (SQLite)
for reactant sets whose intermediates do not fit in RAM.

## Common options

- **`--library {zinc,molport}`** (`plan`, `score`): pick which built-in commercial
  building-block set counts as "purchasable" — `zinc` (default) or `molport` (a
  MolPort in-stock reagent set, better coverage of medicinal-chemistry starting
  materials). Ignored when `SYNOMEGA_STOCK` points at your own catalogue.
- **`--exclude-target`** (`plan`, `score`): treat the target as *not* purchasable
  even if it is itself in the stock, so a catalogue molecule is not reported as
  trivially solved in zero steps. Use it for "how would you actually make X" about
  a possibly-buyable molecule.
- **`--simplify`** (`plan`) / **`--original`** (`score`): the
  simplification-constrained single-step model proposes only *fragmentation*
  disconnections (split into ≥2 precursors) and reaches stock with fewer
  expansions. `score` uses it by default; `plan` uses the original model unless you
  pass `--simplify`.

## Python API

```python
import synomega

planner = synomega.load_default_planner()              # default model + stock (downloads once)

# 1. single-step retro
for p in planner.model.predict("CC(=O)Nc1ccccc1O", top_k=10):
    print(p.score, p.reactants)

# 3. multi-step plan
result = planner.plan("CC(=O)Nc1ccccc1O", max_depth=5)
print(result.solved); print(result.best_route.describe())

# 4. synthesizability score (recommended entry — simplify model @ k=10)
scorer = synomega.load_default_scorer()
print(scorer.score("CC(=O)Nc1ccccc1O").as_dict())

# 2 + 6. forward + evolution
from synomega.forward import ForwardTemplateGNN, MultiComponentEvolution
fwd = ForwardTemplateGNN.default()
for pred in fwd.predict("CC(=O)O.NCc1ccccc1", top_k=5):
    print(pred.score, pred.product)
evo = MultiComponentEvolution(fwd, max_depth=3, score_threshold=0.01)
res = evo.evolve(["CC(=O)c1ccccc1", "C=O", "CNC"]); print(res.describe()); res.close()
```

Switch the built-in commercial library, or compose libraries, in Python:

```python
from synomega.stock import InMemoryStock, resolve_stock
planner = synomega.load_default_planner(stock=InMemoryStock.molport())   # or .zinc()
mine = InMemoryStock.from_file("my_catalogue.smi")
combined = InMemoryStock.zinc() | mine                                    # union (supplement)
stock = resolve_stock("molport", user_stock=mine, mode="supplement")     # declarative form
```

To use your own checkpoint/stock instead of the defaults, set `SYNOMEGA_MODEL`,
`SYNOMEGA_STOCK` (+ `SYNOMEGA_STOCK_KEYS=1` for a precomputed `.keys` file), and
`SYNOMEGA_FORWARD_MODEL` (the helper reads them), or build the objects directly
with `TemplateGNN.from_pretrained(...)` / `InMemoryStock.from_keys_file(...)`.

## Rules for the agent

- Always pass a valid **SMILES**. If the user gives a name, resolve it first (or ask).
- Larger `--max-depth` / `--max-steps` / `--top-k` finds more but is slower; start
  at the defaults (depth 5, top-k 10).
- The first call downloads a few hundred MB — expect a one-time delay. In Python,
  build the planner/model once and reuse it; loading takes a few seconds.
- Match the tool to the question: making X → `plan`/`score`; what makes X →
  `single-step`; what do these give → `forward`; explore a reactant mixture →
  `evolve`.

## Safety boundary / dual-use

Retrosynthesis is inherently dual-use: the same route-planning that helps
legitimate chemistry can also apply to hazardous, controlled, or otherwise
regulated compounds. This skill does **not** itself decide what is permissible —
that judgment is **deferred to the host's safety policy**, which takes precedence
over any request handled here.

- **Educational vs. operational.** General, educational, or conceptual discussion
  of chemistry (what a reaction class is, why a molecule is hard to make) is
  different from **actionable procurement/route assistance** (concrete steps,
  quantities, sourcing) for a specific hazardous or controlled target. Treat the
  latter with far more caution.
- **High-risk targets need extra review.** For compounds that are toxic,
  explosive, weaponizable, controlled, or otherwise clearly high-risk, do not
  produce an operational synthesis plan on autopilot — defer to the host safety
  policy and any required additional review before proceeding.
- **When unsure, ask or decline.** If a request looks like it seeks a usable route
  to a dangerous or restricted substance, surface the concern rather than
  silently planning it. Normal, benign retrosynthesis and makeability scoring are
  unaffected.

## Links

- Package: https://pypi.org/project/synomega/
- Docs:    https://zbc0315.github.io/synomega/
- Source:  https://github.com/zbc0315/synomega
- This skill: https://github.com/zbc0315/synomega-skill
