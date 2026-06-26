# Reference

## Project idea

Skill Graph for Analogical Reasoning builds a graph over `SKILL.md`-based skills and tries to retrieve skills the way a careful human would:

- one primary skill
- a few complementary supporting skills
- no naive pile of near-duplicate instructions

## Build algorithm

`build` extracts from each skill:

- description
- trigger phrases
- keywords
- tool/code references
- runtime constraints

Then it computes weakly supervised relations between skill pairs.

Stored views include:

- `similarity` — static closeness between skills
- `complementarity` — a proxy for "useful together without being redundant"

## Query algorithm

### Step 1: choose one primary skill

Primary-skill ranking uses signals such as:

- intent match
- trigger match
- object match
- readiness
- specificity
- lexical match

### Step 2: choose complementary support

Supporting-skill ranking uses:

- `task_relevance`
- `complementarity`
- `execution_support`
- `redundancy_with_primary` penalty

The goal is **not** to attach several highly similar skills.
The goal is to attach only the skills that actually add missing coverage.

## Look view

`look` renders the graph and lets the user switch between:

- `Similarity`
- `Complementarity`

Edges are colored from blue (`0`) to red (`1`) in the active view.
