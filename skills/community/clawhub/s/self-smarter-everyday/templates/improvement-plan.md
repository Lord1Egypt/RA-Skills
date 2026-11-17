# Improvement Plan

> **Plan ID:** {{PLAN_ID}}
> **Created:** {{CREATION_DATE}}
> **Status:** {{STATUS}} (draft / active / completed / abandoned)
> **Owner:** self-smarter-everyday automated system
> **Review Date:** {{REVIEW_DATE}}

---

## 1. Current State Assessment

### System Overview

The self-improvement system has been operational for 4 weeks. The nightly routine runs 6 phases (reflection, audit, memory compaction, prompt evolution, skill gap analysis, improvement planning) and has completed 26 out of 28 scheduled runs. The system demonstrates measurable improvement in error rate reduction (12% → 4.8%) and cache efficiency (82% → 94%), but falls short on token efficiency (63% vs 70% target) and daily budget ($8.20 vs $7 target).

### Performance Baseline (Current)

| Dimension | Current Score | Target | Gap | Severity |
|-----------|--------------|--------|-----|----------|
| Error rate | 4.8% | <5% | 0.2% | 🟢 Minimal |
| Token efficiency | 63% | >70% | -7% | 🟡 Moderate |
| Daily budget | $8.20 | <$7.00 | +$1.20 | 🔴 High |
| Response time | 35s avg | <30s | +5s | 🟡 Moderate |
| Cache hit rate | 94% | >80% | +14% | 🟢 Exceeding |
| Sub-agent count | 4.2/day | <3.0/day | +1.2 | 🔴 High |
| Lesson capture | 2.0/day | >1.5/day | +0.5 | 🟢 Exceeding |

### Strengths to Preserve
- Nightly routine execution is reliable (93% uptime)
- Memory compaction effectively prevents state bloat
- Cache-first email strategy saves significant API costs
- Lesson capture rate exceeds target — knowledge accumulation is healthy
- Prompt evolution shows measurable fitness improvement over generations

### Weaknesses to Address
- Sub-agent over-spawning drives both cost and token inefficiency
- Browser automation has intermittent failures (20% failure rate this week)
- No catch-up mechanism for missed nightly routine executions
- Prompt evolution doesn't yet consider task-category-specific optimization
- Memory access tracking is too coarse (day-level) for accurate tier management

---

## 2. Identified Gaps

### Gap 1: Sub-Agent Cost Overrun
- **Description:** Averaging 4.2 sub-agents per day, each adding ~15k tokens of context overhead. This accounts for approximately $1.20/day in excess spending.
- **Root cause:** Complex tasks are decomposed too aggressively. Some sub-agents handle tasks that could be done by the parent in fewer tokens.
- **Impact:** Budget target missed by 17%. Token efficiency degraded by ~7% due to sub-agent context overhead.
- **Evidence:** Session logs from past 2 weeks show 30 sub-agent spawns, of which approximately 8 could have been handled by parent directly.

### Gap 2: Browser Automation Reliability
- **Description:** 3 out of 15 browser automation attempts failed this week (20% failure rate). Failures cause task delays and sometimes require manual intervention.
- **Root cause:** No pre-flight health check before browser automation. Browser sessions become stale after extended idle time. No automatic recovery mechanism.
- **Impact:** 3 tasks delayed by 10-20 minutes each. 1 task required Akmal's manual intervention (violates personal assistant mode rules).
- **Evidence:** Error logs show `BrowserContext closed` and `TimeoutError` as primary failure modes.

### Gap 3: Missing Catch-Up Mechanism
- **Description:** When the nightly routine is missed (VPS restart, maintenance window), there's no automatic catch-up. The system simply skips that day's cycle.
- **Root cause:** Cron job fires at a fixed time. If the system is down at 2 AM, the routine doesn't run. No startup hook or delayed execution.
- **Impact:** 2 missed routines in 4 weeks. Each miss means a day without reflection, audit, or memory compaction — creating gaps in the improvement cycle.
- **Evidence:** `routine_state.json` shows `last_run` gaps of 2 days on two occasions.

### Gap 4: Coarse Memory Access Tracking
- **Description:** Memory entries track `last_accessed` at day granularity. Entries accessed multiple times in a day are indistinguishable from entries accessed once.
- **Root cause:** Initial implementation used date-only timestamps for simplicity. The compaction algorithm's promotion rules assume finer granularity.
- **Impact:** Some entries are incorrectly demoted because the system can't distinguish "accessed 5 times today" from "accessed once today." This leads to suboptimal tier placement.
- **Evidence:** Memory compaction logs show 3 entries demoted from HOT to WARM despite being accessed multiple times on the demotion day.

### Gap 5: No Task-Category Prompt Optimization
- **Description:** All tasks use the same evolved prompt variant regardless of task category (coding, research, communication, maintenance).
- **Root cause:** Prompt evolution currently optimizes a single universal prompt. No mechanism to select or evolve category-specific prompts.
- **Impact:** A prompt optimized for coding tasks may not be optimal for research tasks, and vice versa. Leaving potential fitness gains on the table.
- **Evidence:** Success rate varies significantly by category: coding 88%, research 79%, communication 91%, maintenance 73%.

---

## 3. Proposed Improvements

### Improvement 1: Sub-Agent Consolidation Policy
- **What:** Implement a decision tree that determines whether a task should be handled by parent or delegated to a sub-agent.
- **Rules:**
  - Single-file read/write → parent handles directly
  - Simple web search (1-2 queries) → parent handles directly
  - Multi-step browser automation → sub-agent (justified)
  - Complex research (20+ queries) → sub-agent (justified)
  - SSH operations with verification → sub-agent (justified)
- **Expected impact:** Reduce sub-agent count from 4.2 to ~3.0 per day. Save ~$1.20/day.
- **Risk:** Low. Parent can handle simple tasks without quality loss.

### Improvement 2: Browser Pre-Flight Health Check
- **What:** Before any browser automation task, run a health check: verify browser process is running, test a simple page load, confirm cookies are valid.
- **Implementation:** Add `browser_health_check()` function to the automation workflow. If check fails, auto-restart browser and retry once before reporting failure.
- **Expected impact:** Reduce browser failures from 20% to <5%.
- **Risk:** Low. Health check adds ~2 seconds per automation task.

### Improvement 3: Nightly Routine Catch-Up
- **What:** On system startup or first interaction of the day, check if nightly routine ran in the past 24 hours. If not, trigger it immediately.
- **Implementation:** Add a check in the heartbeat/proactivity system: compare `last_run` timestamp against current time. If gap > 24h, run routine with `--catch-up` flag.
- **Expected impact:** Eliminate missed routine executions. Maintain continuous improvement cycle.
- **Risk:** Low. Catch-up run may delay first response by ~30 seconds.

### Improvement 4: Fine-Grained Memory Access Tracking
- **What:** Upgrade `last_accessed` from date-only to full ISO timestamp with hour precision.
- **Implementation:** Update `memory_compact.py` to write and read full timestamps. Adjust promotion/demotion thresholds to use hours instead of days.
- **Expected impact:** More accurate tier placement. Prevent incorrect demotion of frequently-accessed entries.
- **Risk:** Low. Backward compatible — existing date-only entries are treated as midnight.

### Improvement 5: Task-Category Prompt Variants
- **What:** Evolve separate prompt variants for each major task category: coding, research, communication, maintenance.
- **Implementation:** Extend `prompt_evolve.py` to maintain separate variant pools per category. Fitness evaluation uses category-specific success rates.
- **Expected impact:** Improve success rate for weaker categories (maintenance 73% → 85%, research 79% → 88%).
- **Risk:** Medium. More variants = more state to manage. Evolution cycles take longer.

---

## 4. Priority Ranking

| Priority | Improvement | Impact | Effort | Risk | Score |
|----------|------------|--------|--------|------|-------|
| **P1** | Sub-Agent Consolidation | High | Low | Low | 🟢 9/10 |
| **P1** | Browser Pre-Flight Check | High | Low | Low | 🟢 9/10 |
| **P2** | Nightly Routine Catch-Up | Medium | Low | Low | 🟢 7/10 |
| **P2** | Fine-Grained Access Tracking | Medium | Medium | Low | 🟡 6/10 |
| **P3** | Task-Category Prompts | Medium | High | Medium | 🟡 5/10 |

**Rationale:** P1 items have the highest impact-to-effort ratio and directly address the two biggest gaps (budget and reliability). P2 items are important for system resilience but less urgent. P3 is valuable but requires significant refactoring of the prompt evolution system.

---

## 5. Resource Requirements

### Time Investment
| Improvement | Development Time | Testing Time | Total |
|------------|-----------------|-------------|-------|
| Sub-Agent Consolidation | 30 min | 15 min | 45 min |
| Browser Pre-Flight | 20 min | 10 min | 30 min |
| Nightly Catch-Up | 15 min | 10 min | 25 min |
| Access Tracking | 30 min | 20 min | 50 min |
| Category Prompts | 60 min | 30 min | 90 min |
| **Total** | **155 min** | **85 min** | **240 min (4 hours)** |

### Infrastructure
- No additional infrastructure required. All improvements run on existing VPS.
- Storage impact: negligible (<1 MB additional state data for category prompts).
- Cron impact: one additional check for catch-up mechanism (~1 second per heartbeat).

### Token Budget Impact
- Sub-agent consolidation: **saves** ~15k tokens/day (fewer sub-agents)
- Browser pre-flight: **costs** ~500 tokens/day (health check overhead)
- Nightly catch-up: **costs** ~5k tokens on catch-up days (1 day in 14)
- Net effect: **saves** ~14k tokens/day on average

---

## 6. Success Criteria

### Quantitative Targets

| Metric | Before | After (4 weeks) | After (8 weeks) |
|--------|--------|-----------------|-----------------|
| Daily budget | $8.20 | <$7.50 | <$7.00 |
| Sub-agents/day | 4.2 | <3.5 | <3.0 |
| Browser success rate | 80% | >90% | >95% |
| Nightly routine uptime | 93% | >98% | >99% |
| Token efficiency | 63% | >67% | >70% |
| Maintenance success rate | 73% | >80% | >85% |

### Qualitative Indicators
- No manual intervention required for browser automation failures
- Nightly routine runs every day without manual triggering
- Memory tier placement feels accurate (frequently-used entries stay HOT)
- Different task types receive appropriately-tuned prompts
- Akmal doesn't notice any degradation in response quality

### Acceptance Tests
1. **Budget test:** 7-day rolling average of daily cost stays below $7.00 for 2 consecutive weeks.
2. **Reliability test:** 30 consecutive browser automation attempts with <2 failures.
3. **Uptime test:** 30 consecutive days of nightly routine execution (including catch-ups).
4. **Quality test:** No task requires re-execution due to prompt-related errors.

---

## 7. Timeline

### Week 1 (Immediate)
- [ ] Implement sub-agent consolidation decision tree
- [ ] Add browser pre-flight health check
- [ ] Test both P1 improvements in dry-run mode
- [ ] Deploy P1 improvements to production

### Week 2
- [ ] Implement nightly routine catch-up mechanism
- [ ] Upgrade memory access tracking to hour precision
- [ ] Run memory compaction with new granularity
- [ ] Monitor P1 improvements for 7 days, verify metrics

### Week 3
- [ ] Design task-category prompt variant system
- [ ] Implement category detection logic
- [ ] Begin parallel evolution of category-specific prompts
- [ ] Review and adjust P2 improvements

### Week 4
- [ ] Complete category prompt evolution (minimum 3 generations each)
- [ ] Full system review: all metrics vs targets
- [ ] Document lessons learned from this improvement cycle
- [ ] Plan next improvement cycle based on remaining gaps

---

## 8. Rollback Plan

### Per-Improvement Rollback

| Improvement | Rollback Method | Data Loss Risk | Time to Rollback |
|------------|----------------|---------------|-----------------|
| Sub-Agent Consolidation | Remove decision tree, revert to always-delegate | None | 5 min |
| Browser Pre-Flight | Remove health check function | None | 5 min |
| Nightly Catch-Up | Remove catch-up trigger from heartbeat | None | 5 min |
| Access Tracking | Revert to date-only timestamps | Low (hour data lost) | 15 min |
| Category Prompts | Revert to single universal prompt | Medium (category variants lost) | 10 min |

### Global Rollback
If multiple improvements cause issues simultaneously:
1. Disable all new improvements (revert scripts to pre-plan versions)
2. Run `nightly_routine.py --dry-run` to verify system health
3. Review logs for error patterns
4. Re-enable improvements one at a time with 24h observation between each

### Backup Strategy
- All script changes are made in the skill directory (version-controlled)
- State directory (`~/self-smarter/state/`) is backed up by existing VPS backup
- Pre-improvement state snapshot saved to `~/self-smarter/backups/pre_plan_{{PLAN_ID}}/`

---

## 9. Notes and Dependencies

### Dependencies
- Sub-agent consolidation depends on accurate task complexity estimation — needs calibration period.
- Category prompt evolution depends on accurate task categorization — initial classification may be imperfect.
- Nightly catch-up requires the heartbeat/proactivity system to be running — verify cron is active.

### Risks Not Yet Mitigated
- VPS disk space: state directory growth is managed by compaction, but archive tier has no size limit.
- Prompt evolution divergence: category-specific prompts may drift too far from each other, making universal fallback difficult.
- Catch-up timing: running nightly routine during active hours may impact response latency.

### Future Considerations (Post-This-Plan)
- Implement A/B testing framework for prompt variants (split tasks between variants, compare results)
- Add sentiment analysis to reflection logs (track confidence/frustration patterns)
- Explore cross-session learning (share lessons between different agent instances)
- Build dashboard for real-time metric visualization

---

*This improvement plan is a living document. Update status and metrics as work progresses. Review weekly during the weekly evaluation cycle.*
