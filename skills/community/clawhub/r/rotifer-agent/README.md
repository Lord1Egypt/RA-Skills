# Rotifer Agent

> From intent to running Agent in seven steps.

Build AI Agents by composing [Genes](https://rotifer.dev/docs) — the atomic, fitness-evaluable capability units of [Rotifer Protocol](https://rotifer.dev).

## What It Does

Describe what your Agent should do, and this Skill handles the architecture:

| Say this | It does this |
|----------|-------------|
| "Build a document quality checker" | Decomposes into grammar + readability + tone Genes, recommends Par composition |
| "Create a code review agent" | Selects security-auditor + code-complexity + docs-writer, designs Seq(Par, ...) pipeline |
| "Make a search-and-summarize pipeline" | Picks web-search → summarizer → formatter, wires up Seq |

## The Seven Phases

1. **Intent decomposition** — break the goal into 2-6 capability units
2. **Gene selection** — find the fittest Gene for each unit from Arena rankings
3. **Gap filling** — create missing Genes (route to gene-dev)
4. **Genome composition** — choose Seq / Par / Cond / Try / TryPool
5. **Agent creation** — `rotifer agent create`
6. **Test run** — `rotifer agent run` with validation checklist
7. **Iteration** — swap underperforming Genes, tune composition

## Composition Strategies

| Strategy | Semantics | Use when |
|----------|-----------|----------|
| **Seq(A, B, C)** | Pipeline: A → B → C | Output of one feeds the next |
| **Par(A, B)** | Parallel: run simultaneously | Independent tasks, merge results |
| **Cond(p, A, B)** | Branch: if p then A else B | Input determines the path |
| **Try(A, B)** | Fallback: A fails → B | Primary path unreliable |
| **TryPool(A, B, C)** | Race: all try, first wins | Multiple equivalent implementations |

## Quick Start

```
Build an agent that checks document quality — grammar, readability, and tone
```

The Skill decomposes the intent, finds top-ranked Genes, and creates the Agent.

## Related Skills

- [rotifer-guide](https://clawhub.ai/skills/rotifer-guide) — Learn Rotifer from scratch
- [rotifer-arena](https://clawhub.ai/skills/rotifer-arena) — Compare and evaluate Genes
- [rotifer-self-evolving-agent](https://clawhub.ai/skills/rotifer-self-evolving-agent) — Auto-evolve your Agent

## Links

- [Rotifer Protocol](https://rotifer.dev)
- [Documentation](https://rotifer.dev/docs)
- [Protocol Specification](https://github.com/rotifer-protocol/rotifer-spec)

## License

Apache-2.0
