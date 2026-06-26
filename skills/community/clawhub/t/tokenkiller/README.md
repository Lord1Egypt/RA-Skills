# tokenkiller

Reduce token usage for agent workflows (budgets, gating, progressive disclosure, dedupe).

## What it is

TokenKiller is a lightweight skill/policy to systematically reduce LLM token usage **without noticeably lowering success rate**. It is designed for multi-step agent workflows such as:

- search / exploration
- coding / refactoring
- debugging / troubleshooting
- testing / verification
- docs / summarization

## How it works

Core mechanisms:

- **Dynamic budgets**: Assess task complexity first, then apply appropriate budget (simple/medium/complex)
- **Progressive disclosure**: pull only the minimum necessary context (avoid big-file/log dumps)
- **L0-L3 information layers**: Start with goal (L0), constraints (L1), evidence (L2); only pull full content (L3) when necessary
- **Diff-first outputs**: prefer patches and deltas over full-file reposts
- **Deduped evidence**: never paste the same content twice; reference it briefly instead
- **Token self-check**: periodic review of token consumption patterns
- **Multi-skill collaboration**: works alongside other skills as a constraint layer

## Key Features

### Dynamic Budget Mechanism

| Complexity | Criteria | Tool Budget | Output Budget |
|------------|----------|-------------|---------------|
| Simple | Single file, clear requirement | ≤3 calls | ≤50 lines |
| Medium | 2-3 files, some exploration | ≤6 calls | ≤120 lines |
| Complex | Cross-module, multi-step, unclear | ≤10 calls | ≤200 lines |

When budget runs low but task incomplete, a warning is issued and strategy shifts to more conservative mode.

### L3 Pull Triggers

Only pull full content (L3) in these scenarios:
- Code modification requiring exact indentation/format
- Config debugging with interdependent settings
- Error analysis needing complete stack trace
- User explicitly requests full content

### Multi-Skill Priority

- Functional skills (pdf, xlsx, etc.) take precedence
- TokenKiller applies as a constraint layer during output
- User requests override throttling rules

### Token Self-Check

High-consumption behaviors to avoid:
- Reading >500 line files in full
- Outputting complete file contents instead of diffs
- Repeatedly pasting the same code/log
- Listing entire directory trees
- Outputting lengthy explanatory text

Self-check timing: After every 3 tool calls, verify you're at L0-L2 level with no duplicate information.

## Files

- `SKILL.md` — the full policy definition (YAML header + detailed rules)
- `examples.md` — examples and anti-patterns (6 examples covering various scenarios)

## License

MIT-0 (see `LICENSE`).