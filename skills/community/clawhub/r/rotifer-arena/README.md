# Rotifer Arena

> Objective, quantifiable capability evaluation for AI agents.

One-click Gene comparison and evaluation powered by [Rotifer Protocol](https://rotifer.dev).

## What It Does

Evaluate any AI capability against the Arena — no setup required:

| Say this | It does this |
|----------|-------------|
| "Evaluate the web-search skill from ClawHub" | Imports, compiles, finds the top opponent, runs Arena battle |
| "Compare my two implementations" | Head-to-head comparison with fitness breakdown |
| "Build a quantitative strategy benchmark" | Scaffolds the scenario, creates Genes, runs evaluation |

Every evaluation produces a structured Markdown report with:
- **F(g)** fitness scores and ranking
- **V(g)** security assessment
- Fidelity comparison (Native vs Hybrid vs Wrapped)
- Upgrade path recommendations

## Quick Start

```
Compare my particle-brute and particle-spatial Genes
```

The Skill handles the rest: confirms both Genes exist, submits to Arena, and generates a comparison report.

## Workflow

1. **Identify target** — understand what to evaluate
2. **Compile & verify** — `rotifer compile` the Gene
3. **Match opponent** — auto-find the strongest competitor in the same domain
4. **Arena submit** — run the evaluation
5. **Generate report** — structured Markdown with scores, rankings, and next steps

## Related Skills

- [rotifer-guide](https://clawhub.ai/skills/rotifer-guide) — Learn Rotifer from scratch
- [rotifer-agent](https://clawhub.ai/skills/rotifer-agent) — Compose Genes into Agents
- [rotifer-self-evolving-agent](https://clawhub.ai/skills/rotifer-self-evolving-agent) — Auto-evolve your Agent

## Links

- [Rotifer Protocol](https://rotifer.dev)
- [Documentation](https://rotifer.dev/docs)
- [Protocol Specification](https://github.com/rotifer-protocol/rotifer-spec)

## License

Apache-2.0
