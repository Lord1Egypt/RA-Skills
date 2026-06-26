# Sequencer Archive And DA

Use this file when the user asks how Zeko works or which endpoint role matters for a task.

## Official docs

- Core concepts: `https://docs.zeko.io/architecture/zeko-core-concepts`
- Sequencer guide: `https://docs.zeko.io/operators/guides/sequencer`
- DA layer guide: `https://docs.zeko.io/operators/guides/da-layer`

## Sequencer

- The sequencer is the live coordination point for Zeko L2 state progression.
- It exposes GraphQL surfaces such as `sequencerPk` and `circuitsConfig`.
- Use the live Zeko GraphQL endpoint when the user needs current chain config, bridge config, or request lifecycle status.
- If the user asks which live query to run, route them to the `curl` examples in `references/40-endpoints-and-curl.md`.

## Archive node

- The archive node is the historical read path.
- Use it for past actions, events, and timeline debugging.
- If the user needs to inspect bridge history, historical actions, or event backfills, query the archive node instead of the live node.
- If the user asks what queries to run against the archive node, route them to the archive `curl` examples in `references/40-endpoints-and-curl.md`.
- For bridge operations, do not confuse archive visibility with canonical finality. A transaction/action can be visible and usable for pending-inclusion finalization before it is marked canonical.

## DA layer

- The DA layer is the availability path for rollup data.
- Use the DA layer docs when the user asks how Zeko makes rollup data available or what validators are checking.

## Practical split

- Live Zeko node: current config, sequencer info, live bridge request status.
- Mina gateway: current Mina reads on testnet.
- Mina archive gateway: historical Mina actions and archive state.
- Zeko archive: historical Zeko events.
- Actions/indexer surfaces: bridge action visibility and finality metadata; diagnose pending inclusion separately from canonical finality.
- When the question is conceptual, explain the sequencer, archive node, and DA layer here first.
- When the question is operational, pair this file with `references/40-endpoints-and-curl.md` for exact queries.
