# Salience Research Artifacts

Research into linguistic and cognitive salience frameworks for improving Memory Crystal's recall architecture.

**Started:** 2026-02-20
**Origin:** Parker found the EuroSLA salience paper while exploring visual salience to language salience. Led to mapping how salience research applies to the gap between memory capture (works) and spontaneous recall (doesn't).

## Files

| File | What |
|------|------|
| `README.md` | This index |
| `eurosla-salience-review.md` | Summary of the Knell et al. EuroSLA paper (three-level salience taxonomy) |
| `salience-levels-diagram.png` | Screenshot of the perceptual/psycholinguistic/experiential diagram |
| `full-research-summary.md` | Complete research synthesis: 7 papers, 7 architecture principles, all sources |

## Key Insight

The problem isn't storage. It's not even retrieval. It's **associative recall**. Salience determines what gets noticed, encoded deeply, and spontaneously surfaced. Our current system treats all 150K chunks equally. It needs a salience layer.

## Seven Principles (from the research)

1. Salience is multi-dimensional (structural, contextual, experiential)
2. Prediction error drives encoding priority (surprise > confirmation)
3. Retrieval needs spreading activation (graph, not flat vector store)
4. Blocking is the enemy (summaries prevent deeper encoding)
5. Temporal decay with reactivation (use it or lose it)
6. Salience contagion (important events boost nearby memories)
7. Consolidation needs a "sleep" phase (salience-aware compaction)
