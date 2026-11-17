# Production Deployment Patterns for Self-Improving Agents

## Overview

Deploying a self-improving agent in production introduces challenges beyond those of static AI systems. The agent not only serves users but also modifies itself, creating a moving target for monitoring, testing, and operations. This document covers production patterns for monitoring, logging, alerting, gradual rollout, health checks, recovery, cost management, and the unique challenges of operating a system that changes its own behavior.

## Monitoring Architecture

### What to Monitor

#### 1. Agent Health Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| Uptime | Agent availability | < 99% over 24h |
| Response latency | Time from input to output | > 30s average |
| Error rate | Failed tasks / total tasks | > 15% over 1h |
| Token consumption | Tokens used per hour | > budget allocation |
| Memory usage | Context window utilization | > 80% of limit |
| Skill invocation rate | Skills used per task | < 0.5 (skills not being used) |

#### 2. Self-Improvement Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| Improvement success rate | Successful changes / total changes | < 50% |
| Rollback frequency | Rollbacks per week | > 3 per week |
| Fitness trend | 7-day moving average of fitness | Declining for 3+ days |
| Change velocity | Changes applied per day | > 10 per day (too aggressive) |
| Reflection completion | Did 2 AM reflection run? | Missed 2+ consecutive days |

#### 3. Business Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| Task success rate | Successful tasks / total | < 80% |
| User satisfaction | Proxy from feedback signals | Declining for 3+ days |
| Cost per task | Total cost / successful tasks | > 2x baseline |
| Proactive value | Useful proactive actions / total | < 50% |

### Monitoring Implementation

#### Health Check Endpoint
```
Every 5 minutes:
1. Check agent process is running
2. Check memory system is accessible
3. Check cron scheduler is operational
4. Check file system has space
5. Check recent task completion (last 30 min)
6. Report status: healthy | degraded | unhealthy
```

#### Metrics Collection
```
Per task:
- Task ID, type, start time, end time
- Tokens consumed (input + output)
- Skills invoked
- Errors encountered
- Success/failure outcome
- User feedback (if any)

Per day:
- Aggregate all task metrics
- Record self-improvement actions taken
- Record fitness scores
- Record reflection outputs
- Store in daily metrics file
```

## Logging Strategy

### Log Levels
| Level | What to Log | Retention |
|-------|-------------|-----------|
| ERROR | Task failures, system errors, safety violations | 90 days |
| WARN | Unusual patterns, near-misses, degraded performance | 30 days |
| INFO | Task completions, skill invocations, user interactions | 14 days |
| DEBUG | Detailed reasoning, intermediate states, tool outputs | 7 days |

### Log Structure
```json
{
  "timestamp": "2026-08-10T02:00:00+07:00",
  "level": "INFO",
  "component": "self-improvement",
  "action": "reflection-complete",
  "details": {
    "duration_seconds": 300,
    "improvements_identified": 3,
    "improvements_applied": 2,
    "fitness_score": 0.82,
    "files_modified": ["skills/debugging/SKILL.md", "lessons/2026-08-10.md"]
  }
}
```

### Self-Improvement Audit Log
Every self-modification must be logged with full context:
```markdown
## Audit Entry: [change-id]
- **Timestamp:** 2026-08-10 02:15:00
- **Type:** skill-update
- **Zone:** Green (autonomous)
- **File:** skills/debugging/SKILL.md
- **Previous version:** v2.1
- **New version:** v2.2
- **Mutation type:** precision (added specific error patterns)
- **Reason:** 3 debugging tasks failed this week due to missing error pattern
- **Evidence:** tasks #1234, #1237, #1241 all hit same gap
- **Expected improvement:** 15% increase in debugging success rate
- **Rollback plan:** Restore v2.1 from versions/v2.1.md
- **Risk assessment:** Low (additive change, no existing behavior removed)
```

### Log Management
- Logs are stored in `logs/` directory with daily rotation
- Compress logs older than 7 days
- Delete logs older than retention period
- Index logs for search (grep-friendly format)
- Sensitive data (credentials, personal info) NEVER logged

## Alerting

### Alert Categories

#### Critical Alerts (Immediate Response)
- Agent process crashed or unresponsive
- Safety boundary violation detected
- Credential exposure detected
- Data loss or corruption detected
- Self-improvement loop detected (agent modifying itself in a positive feedback loop)

#### Warning Alerts (Response Within 1 Hour)
- Error rate exceeds threshold
- Token consumption exceeds budget
- Self-improvement rollback triggered
- Reflection cycle missed
- Performance regression detected

#### Informational Alerts (Review During Next Reflection)
- New skill created
- Significant prompt mutation applied
- Memory compaction completed
- Fitness score milestone reached

### Alert Routing
```
Critical → Immediate notification to user (if configured)
         → Halt self-improvement
         → Enter safe mode (continue tasks, stop modifying)

Warning  → Log for next reflection
         → If 3+ warnings in 24h → escalate to critical

Info     → Record in daily log
         → Review during 2 AM reflection
```

### Alert Fatigue Prevention
- Only alert on actionable conditions
- Require sustained threshold breach (not single spike)
- Include context in alert (what happened, what to do)
- Allow alert suppression for known conditions
- Weekly review: are alerts still relevant?

## Gradual Rollout

### Why Gradual Rollout?
Self-improvement changes agent behavior. Rolling out changes gradually prevents catastrophic failure from a bad improvement.

### Rollout Strategy

#### Phase 1: Shadow Mode
```
1. Apply change in shadow mode (evaluate but don't use)
2. Run change against recent tasks (replay)
3. Compare shadow results against actual results
4. If shadow performs well → proceed to Phase 2
5. If shadow performs poorly → discard change
```

#### Phase 2: Canary Deployment
```
1. Apply change to 10% of tasks (random selection)
2. Monitor canary tasks closely
3. Compare canary performance against control group
4. If canary > control by > 5% → proceed to Phase 3
5. If canary ≤ control → rollback, analyze
```

#### Phase 3: Full Rollout
```
1. Apply change to all tasks
2. Monitor for 48 hours
3. If stable → confirm change, update baseline
4. If issues → rollback to previous version
```

### Feature Flags for Self-Improvement
```
Feature flags control which improvements are active:

improvement.debugging-v2.2.enabled = true
improvement.debugging-v2.2.rollout_percentage = 100
improvement.communication-v1.5.enabled = true
improvement.communication-v1.5.rollout_percentage = 50
improvement.research-v3.0.enabled = false  # Still in shadow mode
```

Benefits:
- Enable/disable improvements without code changes
- Control rollout percentage per improvement
- Quick rollback by flipping a flag
- A/B testing different improvements simultaneously

## Health Checks

### Pre-Flight Checks (Before Each Self-Improvement Cycle)
```
1. File system health:
   - Disk space > 10% free
   - Memory files accessible and readable
   - No file corruption detected

2. Memory system health:
   - MEMORY.md exists and is valid
   - QMD index is accessible
   - memory_search returns results
   - No orphaned references

3. Skill system health:
   - All registered skills have valid SKILL.md
   - No circular skill references
   - Skill versions are consistent

4. Safety system health:
   - SOUL.md is unmodified (checksum match)
   - AGENTS.md critical rules intact
   - Safety boundaries not expanded
   - Change log is complete and unbroken

5. Resource health:
   - Token budget has headroom
   - No runaway processes
   - Cron scheduler operational
```

### Continuous Health Monitoring
```
During normal operation:
- Heartbeat check every 5 minutes
- Task success rate monitored continuously
- Token consumption tracked per hour
- Error patterns detected in real-time
- Safety boundary compliance verified per task
```

### Health Check Response Matrix
| Check Result | Action |
|-------------|--------|
| All checks pass | Proceed with self-improvement |
| Minor issues (disk > 80%) | Log warning, proceed with caution |
| Major issues (memory corruption) | Halt self-improvement, alert user |
| Critical issues (safety boundary breach) | Emergency stop, rollback recent changes |

## Recovery Procedures

### Scenario 1: Bad Improvement Caused Regression
```
1. DETECT: Regression identified (metrics dropped)
2. IDENTIFY: Find the specific change that caused regression
3. ROLLBACK: Restore previous version of affected file
4. VERIFY: Confirm metrics recover
5. ANALYZE: Understand why the change failed
6. LEARN: Record lesson to prevent similar failures
7. RESUME: Continue self-improvement with adjusted approach
```

### Scenario 2: Memory Corruption
```
1. DETECT: Memory file unreadable or contains garbage
2. ISOLATE: Identify affected files
3. RESTORE: From backup or archive
   - Check archive/ for previous versions
   - Check git history if files were committed
   - Check QMD index for cached content
4. REBUILD: If no backup available, reconstruct from context
5. VERIFY: Confirm restored content is valid
6. PREVENT: Add validation to prevent future corruption
```

### Scenario 3: Self-Improvement Loop (Positive Feedback)
```
1. DETECT: Agent modifying same area repeatedly without improvement
2. HALT: Stop all self-improvement immediately
3. ASSESS: What is the agent trying to improve? Why is it stuck?
4. DIAGNOSE: Is the fitness function wrong? Is the mutation strategy broken?
5. FIX: Address root cause (may require user input)
6. RESET: Clear the stuck improvement queue
7. RESUME: Restart self-improvement with safeguards (lower mutation rate)
```

### Scenario 4: Budget Exhaustion
```
1. DETECT: Token budget approaching or exceeded
2. PRIORITIZE: Only essential operations (task execution, no improvement)
3. REDUCE: Lower reflection depth, skip optional analyses
4. COMMUNICATE: Inform user if budget is structurally insufficient
5. RECOVER: When budget resets, resume normal operations
```

## Cost Management

### Token Budget Optimization

#### Budget Allocation
```
Daily budget: $7.00 (target)

Allocation:
├── Task execution: 60% ($4.20)
│   ├── Parent agent: 40% ($2.80)
│   └── Sub-agents: 20% ($1.40)
├── Self-improvement: 25% ($1.75)
│   ├── Daily reflection: 15% ($1.05)
│   └── Research/learning: 10% ($0.70)
└── Overhead: 15% ($1.05)
    ├── Cron jobs: 10% ($0.70)
    └── Memory operations: 5% ($0.35)
```

#### Cost Reduction Strategies
1. **Cache aggressively**: Use memory_search before external searches
2. **Batch operations**: Combine multiple small operations into one
3. **Use cheap models for routine work**: Flash models for simple tasks
4. **Limit sub-agent depth**: Max 2 levels of sub-agent spawning
5. **Compact before storing**: Summarize before writing to memory
6. **Skip unnecessary reflection**: If day was uneventful, keep reflection minimal
7. **Reuse successful patterns**: Don't re-derive solutions that exist in memory

#### Cost Monitoring
```
Track daily:
- Total tokens consumed
- Cost per task type
- Self-improvement cost vs. task execution cost
- Trend: is cost per task decreasing over time?

Alert if:
- Daily cost > $7 (target exceeded)
- Self-improvement cost > 30% of total (too much overhead)
- Cost per task increasing for 3+ days (efficiency regression)
```

## Operational Runbook

### Daily Operations
```
Morning (automated):
1. Check overnight health metrics
2. Review 2 AM reflection output
3. Verify no alerts fired overnight
4. Check budget status

During day (continuous):
1. Monitor task success rate
2. Track token consumption
3. Respond to alerts if any
4. Log notable events

Evening (automated):
1. Daily metrics aggregation
2. Prepare for 2 AM reflection
3. Archive today's logs
4. Verify backup status
```

### Weekly Operations
```
1. Review weekly metrics trend
2. Assess self-improvement effectiveness
3. Prune old logs and temporary files
4. Update monitoring thresholds if needed
5. Review and update alerting rules
6. Check disk space and clean up
7. Verify backup integrity
```

### Monthly Operations
```
1. Comprehensive performance review
2. Cost analysis and budget adjustment
3. Monitoring system health check
4. Update runbook based on learnings
5. Review alert fatigue (are alerts still useful?)
6. Capacity planning (growing storage, increasing tasks)
7. Security audit (credential isolation, access controls)
```

## Conclusion

Production deployment of a self-improving agent requires robust monitoring, careful rollout procedures, comprehensive health checks, and clear recovery procedures. The unique challenge is that the system changes itself — every improvement is a potential source of regression, and the monitoring system must detect not just external failures but self-inflicted ones. The patterns described here — gradual rollout, feature flags, health checks, audit logging, budget management — provide the operational infrastructure needed to run a self-improving agent safely and efficiently in production. The key principle is: move fast but don't break things, and if you do break things, detect it immediately and rollback automatically.
