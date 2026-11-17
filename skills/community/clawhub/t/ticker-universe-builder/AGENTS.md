# AGENTS.md

This repository is a single agent skill: **ticker-universe-builder**.

**Read [`SKILL.md`](SKILL.md) first.** It carries the routing — which reference to open for which
request, which commands to run in which order, and the boundaries that must not be crossed.
Everything below is only the part `SKILL.md` assumes you already know.

- **Entry point:** `python scripts/universe.py <subcommand>`. Python 3.10+, standard library
  only, no install step. Run it from the repository root.
- **Subcommands:** `taxonomy`, `import`, `fetch`, `measure`, `build`, `maintain`, `diff`, `evaluate`,
  `validate`, `audit-core`.
- **Contracts:** [`references/data-contracts.md`](references/data-contracts.md). Read it before
  writing any JSON. Every input is a documented shape; nothing is inferred from prose.
- **Worked inputs:** [`examples/`](examples/README.md). US Light/Medium/Heavy/Max and
  CN/Crypto/HK/JP/KR/UK Medium
  builds, with standard outputs and disclosed research limits. Open the
  matching example, or the closest available one, before writing a snapshot from scratch.
- **Tests:** `python -m pytest tests -q`.

Hard boundaries, repeated here because they are the ones that matter if you read nothing else:

- Never invent a ticker, venue, listing state, liquidity number, theme relationship or source.
- Never hand-write the final watchlist. The model proposes; the scripts select and render.
- Never bypass or weaken the validator to make an output pass.
- No return guarantees, allocations, order instructions or trade execution. This skill produces
  an observation instrument, not investment advice.
