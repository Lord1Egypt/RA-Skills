# Long-Narrative Window Management (P1 upgrade, v2.0)

Chapter 20 betraying chapter 1 is the classic failure of long-form generation. This
module defines a windowed consistency regime that scales with story length.

## Window architecture

```
[ch01-05] [ch06-10] ... sliding summary window (per 5 chapters)
     \        \__ canonical facts extracted → worldview canon
      \______ chapter summaries → rolling story memory (bounded, FIFO)
```

- **Canonical facts** (per character + per world rule) live in the worldview
  record (`WorldviewVersioning.md`) — never summarized away.
- **Rolling memory** keeps the last N chapters' summaries for scene continuity.
- **Full audit** re-checks the entire canon against the whole text when a new
  arc starts (major checkpoints), not every chapter.

## Checkpoints

| Checkpoint | When | Scope |
|---|---|---|
| Chapter gate | every chapter | immutable facts + worldview contradiction + continuity checklist |
| Arc gate | every 5 chapters | rolling summary rebuild + foreshadowing ledger check |
| Volume gate | every ~20 chapters | full canon audit + character arc diff |

## Foreshadowing ledger

Promises made must be kept (or explicitly broken with narrative cost):

| Promise | Made in | Payoff in | Status |
|---|---|---|---|
| the key unlocks the lighthouse door | c03 | c18 | pending |
| the queen knows the sea-folk secret | c07 | c22 | pending |

A promise left unresolved for >10 chapters triggers a warning at the arc gate.

## Rules

1. Never mutate an immutable fact to fix a plot hole — fix the plot.
2. Synonym drift in character voice is drift: reuse the voice guard.
3. The worldview file is the single source of truth; chapter text is a projection.
