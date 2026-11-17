# AI data evidence guide

Use this guide for stories about model capability, training cost, compute, adoption, labor impact, energy, or investment. AI datasets often mix estimates, vendor claims, and changing benchmarks; visual polish must not conceal weak comparability.

## Evidence levels

Label each field or claim:

1. **Primary observed** — official filings, audited reports, measured experiment results, or reproducible public datasets.
2. **Primary reported** — model cards, technical reports, or company statements without independent verification.
3. **Independent estimate** — transparent third-party calculation with assumptions and uncertainty.
4. **Aggregated observation** — leaderboards, user votes, or scraped catalogs with known selection effects.
5. **Inference** — a conclusion derived by the story team.

Do not silently merge levels. Use primary observed evidence for headline claims when available; show reported or estimated values as ranges and name the source class.

## Training input is not one metric

Keep these separate:

- training compute, usually FLOP;
- accelerator count;
- GPU/TPU hours;
- calendar training time;
- hardware acquisition cost;
- cloud rental cost;
- estimated total training cost;
- energy use and associated emissions.

Converting one to another requires hardware type, utilization, precision, time, price, and often power assumptions. Show the formula, range, and date of prices. Do not place mixed measures on one axis and call it “cost.”

## Capability is not one metric

Record for every score:

- benchmark and version;
- task and language;
- metric definition;
- evaluation date;
- model version or snapshot;
- prompting/scaffolding conditions;
- pass count or sampling;
- possible contamination;
- whether the score is vendor-reported or independently reproduced.

Do not combine Elo, pass@k, accuracy, and an author-built index without an explicit normalization method and sensitivity check. Prefer small-multiple capability tracks over one synthetic “intelligence” score.

## Time alignment

Compare only information that a reader could reasonably interpret together:

- use release/evaluation dates, not retrieval date;
- note benchmark revisions and deprecated test sets;
- avoid comparing a current model on a new benchmark with an older model never evaluated on it;
- distinguish a model family from a specific version;
- freeze dynamic leaderboard snapshots and record the retrieval time.

## Missingness and selection

Absence of a disclosed training cost is not zero. A public leaderboard is not the full model population. A benchmark table often overrepresents organizations that report favorable results.

Show:

- which models are excluded and why;
- whether missingness correlates with company, era, or model type;
- sensitivity to removing estimated values;
- uncertainty intervals when rankings can change.

## Causal language

Cost and capability rising together do not prove that added spending caused each gain. Use “associated with,” “coincides with,” or a descriptive comparison unless the design supports causality.

Separate:

- frontier cost increasing over time;
- cost of reaching a fixed capability decreasing over time;
- capability improvements at a fixed compute budget;
- deployment or inference cost.

These can move in different directions and often make the strongest visual tension.

## Recommended source hierarchy

Start with official technical reports and reproducible benchmark repositories, then triangulate with transparent independent datasets such as Epoch AI and broad syntheses such as the Stanford AI Index. Use company marketing pages only for clearly attributed claims. Archive dynamic tables and keep a source URL for every row.
