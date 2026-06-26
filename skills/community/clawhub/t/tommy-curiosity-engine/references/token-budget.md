# Curiosity Engine — Token Budget Tracking

## Why Track This
The curiosity engine adds files to every heartbeat's context window. For users with strict token budgets, this overhead matters. This doc tracks actual measured costs so we can optimize and provide guidance.

## Estimated Per-Heartbeat Token Cost

| File | Est. Tokens | Loaded When | Phase |
|------|------------|-------------|-------|
| `questions.md` | ~800-2000 | Every heartbeat | 1 |
| `CURIOSITY.md` | ~400-1500 | Every heartbeat | 2 |
| `hits.md` | ~400-1500 | Curiosity-mode heartbeats | 2 |
| `competence.md` | ~400-1000 | Curiosity-mode heartbeats | 3 |
| **Heartbeat prompt addition** | ~250 | Every heartbeat | 1 |

### Phase 1 Overhead (current)
- **Minimum per heartbeat:** ~1050 tokens (prompt + small questions.md)
- **Typical per heartbeat:** ~1500-2500 tokens (prompt + populated questions.md)
- **With CURIOSITY.md (Phase 2):** add ~400-1500 tokens

### Context: What Does This Mean?
- Claude Sonnet context: 200K tokens → curiosity overhead is ~1.25% of context
- If heartbeat runs every 20 minutes, 72 heartbeats/day
- At ~2000 tokens/heartbeat overhead: ~144K extra input tokens/day
- At $3/M input tokens (Sonnet): **~$0.43/day** additional cost
- At $15/M input tokens (Opus): **~$2.16/day** additional cost

## Actual Measurements

*Updated as we collect real data. Measure by comparing heartbeat token usage before/after curiosity engine activation.*

| Date | Heartbeat Model | Curiosity Files Loaded | Input Tokens | Baseline (no curiosity) | Delta |
|------|----------------|----------------------|--------------|------------------------|-------|
| *(measuring starts next heartbeat cycle)* | | | | | |

## Optimization Levers

1. **Cap file sizes** — questions.md max 30 items, CURIOSITY.md max 3 mulling items
2. **Lazy loading** — only load hits.md and competence.md during dedicated curiosity heartbeats
3. **Summarization** — periodically compress questions.md (archive resolved, compress descriptions)
4. **Heartbeat frequency** — fewer heartbeats = less overhead (but less curiosity)
5. **Model selection** — use cheaper model for curiosity-heavy heartbeats

## Budget Guidance for Users

| Budget Level | Recommendation |
|-------------|---------------|
| **Unlimited** (e.g. GitHub Copilot) | Load everything. No restrictions needed. |
| **Generous** (>$10/day) | Full Phase 1-3. Monitor but don't restrict. |
| **Moderate** ($2-10/day) | Phase 1 only. Cap questions at 15. Skip hits/competence. |
| **Tight** (<$2/day) | Consider reducing heartbeat frequency. Phase 1 only, minimal questions. |
| **Strict** (<$0.50/day) | Curiosity engine may not be cost-effective. Consider disabling. |
