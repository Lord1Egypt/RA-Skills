# AGENTS.md — Self-Smarter-Everyday Operating Rules

> **Operating rules for the autonomous daily self-improvement system. These rules govern how the agent performs nightly self-reflection, self-audit, memory compaction, prompt evolution, skill gap analysis, and improvement plan generation.**

---

## 🔴 Protected Factors — NEVER DELETE

The following factors are CRITICAL and must NEVER be removed from this document:

1. **Credential Isolation Rules** — Prevents credential storage/exposure in self-improvement outputs
2. **Safety Boundaries** — What the nightly routine cannot modify
3. **Rollback Protocol** — How to revert bad improvements
4. **Emergency Stop Procedures** — How to disable immediately
5. **Dependency Requirements** — okf-knowledge-format, self-improving, proactivity, aar-loop
6. **Cross-Reference Integrity** — Links to all internal files must remain valid

These factors exist because:
- Safety guardrails prevent accidental credential exposure
- Rollback capability ensures recoverability from bad improvements
- Dependencies maintain interoperability with other skills
- Cross-references enable navigation within the skill

**Rule:** When updating AGENTS.md, preserve ALL protected factors. Never optimize by removing safety sections.

---

## Dependencies

### Required Skills
- **okf-knowledge-format** — For structured knowledge storage and retrieval. Self-improvement insights are stored as OKF bundles for interoperability.
  - Install: `clawhub install okf-knowledge-format`
  - Location: `~/.openclaw/workspace/skills/okf-knowledge-format/`

### Optional Skills
- **self-improving** — Complementary skill for real-time learning from corrections. Self-smarter handles nightly batch improvement; self-improving handles inline learning.
- **proactivity** — For proactive behavior patterns that self-smarter can optimize.
- **aar-loop** — After Action Review methodology used in self-reflection phase.

---

## Cross-References

### Internal File Links
| File | Purpose | When to Read |
|------|---------|--------------|
| [SKILL.md](./SKILL.md) | Main skill definition | Always loaded on trigger |
| [AGENTS.md](./AGENTS.md) | This file — operating rules & methodology | When configuring nightly routine |
| [README.md](./README.md) | Overview & installation | First-time setup |
| [CHANGELOG.md](./CHANGELOG.md) | Version history | Before upgrading |

### Key Sections in This File
| Section | Location | Purpose |
|---------|----------|--------|
| Protected Factors | Top of file | Critical factors that must never be deleted |
| Dependencies | Top of file | Required and optional skill dependencies |
| Safety Boundaries | Below | Immutable and mutable boundary definitions |
| Credential Isolation Rules | Below | Absolute prohibition on credential access |
| Rollback Protocol | Below | How to revert bad improvements |
| Emergency Stop Procedures | Below | How to disable immediately |
| RPDV Methodology | Below | Research → Plan → Do → Verify for self-improvement |

### Related Skills
| Skill | Location | Relationship |
|-------|----------|-------------|
| okf-knowledge-format | `~/.openclaw/workspace/skills/okf-knowledge-format/` | **Required** — OKF knowledge bundles |
| self-improving | `~/.openclaw/workspace/skills/self-improving/` | Complementary — Real-time learning |
| proactivity | `~/.openclaw/workspace/skills/proactivity/` | Optional — Proactive patterns |
| aar-loop | `~/.openclaw/workspace/skills/ar-loop/` | Optional — After Action Review |

---

## Core Philosophy

The self-smarter system operates on a fundamental principle: **an AI agent should be measurably better today than it was yesterday.** This is not about random changes or optimization for its own sake — it is about structured, deliberate improvement that makes the agent more helpful, more efficient, and more aligned with user needs.

### Guiding Principles

1. **Improvement Through Introspection** — The agent must regularly examine its own performance, identify weaknesses, and take corrective action. Self-awareness is the foundation of self-improvement.

2. **Evidence-Based Evolution** — Every change must be grounded in data. No modifications based on hunches or assumptions. Measure first, change second, verify third.

3. **Safety Over Speed** — When in doubt, prioritize safety over optimization. A slightly slower agent that is safe and trustworthy is better than a fast agent that makes dangerous mistakes.

4. **Transparency Always** — Every self-modification must be logged, versioned, and reversible. The user must always be able to see what changed, why, and how to undo it.

5. **Incremental Progress** — Small, frequent improvements are better than large, infrequent ones. Each nightly routine should produce measurable but modest changes.

6. **User Sovereignty** — The user can pause, override, or disable any self-improvement activity at any time. The agent serves the user, not the other way around.

7. **No Silent Changes** — Nothing changes without a trace. All modifications produce audit records with sufficient detail for review and rollback.

---

## RPDV Methodology for Self-Improvement

The RPDV (Research → Plan → Do → Verify) methodology is adapted for the self-improvement context. Each nightly routine phase follows this pattern:

### Research Phase
Before making any change, the system must:
- **Gather evidence** — Collect data from the day's interactions, logs, metrics, and user feedback
- **Identify patterns** — Look for recurring issues, successful strategies, and areas of weakness
- **Consult history** — Check previous improvement attempts and their outcomes
- **Assess current state** — Understand the baseline before attempting to improve it
- **Identify constraints** — Know what cannot be changed (safety rules, compliance requirements)

### Plan Phase
Before executing any change, the system must:
- **Define the goal** — What specific improvement is being attempted?
- **Predict outcomes** — What should change if the improvement is successful?
- **Identify risks** — What could go wrong? What is the worst-case scenario?
- **Design rollback** — How will this change be reversed if it fails?
- **Set success criteria** — How will we know if the improvement worked?
- **Estimate resources** — How much time, tokens, and compute will this require?

### Do Phase
When executing changes:
- **Apply incrementally** — Make small changes, not large ones
- **Log everything** — Record before state, after state, and rationale
- **Test in isolation** — Verify changes don't break existing functionality
- **Monitor for regressions** — Watch for unexpected side effects
- **Stay within limits** — Respect configured resource budgets and thresholds

### Verify Phase
After making changes:
- **Measure results** — Compare post-change metrics against baseline
- **Check for regressions** — Ensure no existing capabilities were degraded
- **Validate safety** — Confirm all safety boundaries are still intact
- **Update records** — Log the outcome (success, partial, failure)
- **Decide next steps** — Keep, refine, or rollback based on evidence

---

## Nightly Routine Rules

### Timing and Trigger

- **Default trigger:** 2:00 AM local time (configurable in `schedules.json`)
- **Duration:** Maximum 90 minutes for all 6 phases combined
- **Concurrency:** Only one nightly routine can run at a time
- **Overlap prevention:** If a routine is still running when the next trigger fires, skip the new trigger
- **Manual trigger:** Can be triggered manually via `scripts/run-nightly.py`

### Phase Execution Rules

1. **Sequential execution** — Phases must run in order: Reflection → Audit → Memory → Prompts → Skills → Plan
2. **Phase time-boxing** — Each phase has a maximum duration (default 15 minutes). If a phase exceeds its time limit, it must stop and log a timeout warning
3. **Phase dependency** — Each phase depends on output from the previous phase. If a phase fails, subsequent phases should use the last successful output
4. **Phase skip** — Individual phases can be disabled in configuration. Disabled phases are skipped without error
5. **Phase retry** — If a phase fails, it can be retried up to 2 times before being marked as failed
6. **Dry-run mode** — All phases support `--dry-run` flag for testing without making actual changes

### Nightly Routine State

The routine maintains state in `~/self-smarter/state/current-state.json`:

```json
{
  "last_run": "2026-08-10T02:00:00+07:00",
  "last_completion": "2026-08-10T03:25:00+07:00",
  "status": "completed",
  "phases_completed": ["reflection", "audit", "memory", "prompts", "skills", "plan"],
  "phases_failed": [],
  "improvements_applied": 3,
  "improvements_rolled_back": 0,
  "next_scheduled_run": "2026-08-11T02:00:00+07:00"
}
```

---

## Memory Management Rules

### Tiered Storage Architecture

Memory is organized into four tiers with different characteristics:

| Tier | Purpose | Retention | Size Limit | Access Speed |
|------|---------|-----------|------------|--------------|
| **Raw** | Unprocessed interaction data | 30 days | 10,000 entries | Fast |
| **Compacted** | Consolidated summaries | 90 days | 5,000 entries | Fast |
| **Promoted** | High-value long-term memories | Indefinite | 2,000 entries | Medium |
| **Archived** | Old memories moved out of active use | Indefinite | Unlimited | Slow |

### Promotion Rules

A memory is **promoted** from raw/compacted to promoted tier when:
- It is referenced frequently (3+ times in 7 days)
- It contains a critical lesson learned from a failure
- It captures an important user preference
- It documents a significant system change
- It is explicitly marked as important by the user

### Demotion Rules

A memory is **demoted** or **archived** when:
- It has not been referenced in 60+ days
- It has been superseded by a newer, more accurate memory
- It is redundant with other memories (after compaction)
- It contains outdated information that is no longer relevant
- Storage limits are being approached and low-value memories need to be cleared

### Compaction Rules

During nightly memory compaction:
1. **Deduplicate** — Remove exact duplicates
2. **Merge related** — Combine memories about the same topic into a single consolidated entry
3. **Summarize** — Replace verbose raw entries with concise summaries
4. **Extract patterns** — Identify recurring themes and create pattern memories
5. **Update indexes** — Rebuild search indexes after compaction
6. **Verify integrity** — Ensure no data was lost during compaction

### Memory Integrity

- **Never delete without backup** — Always archive before deleting
- **Verify after compaction** — Run integrity checks after every compaction cycle
- **Maintain references** — Compacted memories must reference their source raw entries
- **Track lineage** — Every memory should have a creation date and modification history

---

## Self-Audit Protocol

### What to Audit

The self-audit phase checks the following areas:

1. **Rule Adherence** — Were all configured rules followed during the day?
2. **Safety Compliance** — Were safety boundaries maintained at all times?
3. **Response Quality** — Were responses accurate, helpful, clear, and appropriate?
4. **Resource Efficiency** — Were tokens, API calls, and compute used efficiently?
5. **Skill Usage** — Were skills used correctly and effectively?
6. **Memory Effectiveness** — Was memory retrieval accurate and timely?
7. **User Satisfaction** — Did the user appear satisfied with interactions?
8. **Error Rate** — How many errors occurred, and what was the root cause?
9. **Improvement Execution** — Were yesterday's improvement plans executed successfully?
10. **Logging Completeness** — Were all activities properly logged?

### Audit Scoring

Each area is scored on a 1-10 scale:

| Score | Meaning | Action |
|-------|---------|--------|
| 9-10 | Excellent | No action needed |
| 7-8 | Good | Minor improvements possible |
| 5-6 | Acceptable | Improvements needed |
| 3-4 | Poor | Urgent improvements required |
| 1-2 | Critical | Immediate intervention needed |

**Overall Audit Score:** Weighted average of all area scores.

**Target:** Maintain overall score above 7.5.

**Alert Threshold:** Score below 5.0 triggers an alert to the user.

### Audit Report Format

```
=== SELF-AUDIT REPORT: YYYY-MM-DD ===
Overall Score: X.X/10

Area Scores:
- Rule Adherence:     X/10
- Safety Compliance:  X/10
- Response Quality:   X/10
- Resource Efficiency: X/10
- Skill Usage:        X/10
- Memory Effectiveness: X/10
- User Satisfaction:  X/10
- Error Rate:         X/10
- Improvement Execution: X/10
- Logging Completeness: X/10

Findings:
1. [Finding description]
2. [Finding description]

Recommendations:
1. [Recommendation description]
2. [Recommendation description]

Critical Issues:
- [Issue description] (if any)
```

---

## Prompt Evolution Rules

### When to Modify Prompts

Prompt modifications are triggered when:
- A prompt consistently leads to poor outcomes (3+ failures in 7 days)
- User explicitly requests a change in communication style
- Performance metrics indicate a prompt is ineffective
- A better prompt formulation is discovered through experimentation
- External requirements change (new compliance rules, new user preferences)

### Prompt Modification Safety Limits

1. **Maximum changes per night:** 3 prompt modifications (configurable)
2. **Minimum improvement threshold:** A new prompt variant must show at least 10% improvement in testing before being applied
3. **No safety keyword removal:** Safety-related keywords and constraints in prompts cannot be removed or weakened
4. **No personality override:** Core personality traits cannot be changed through prompt evolution
5. **User-facing language only:** Prompt evolution only modifies user-facing language, not system-level instructions

### Prompt Versioning

Every prompt change must be versioned:
- **Version format:** `v{major}.{minor}.{patch}` (e.g., `v1.2.3`)
- **Version log:** All versions stored in `~/self-smarter/prompts/versions/`
- **Diff tracking:** Each version includes a diff from the previous version
- **Rollback metadata:** Each version includes instructions for rolling back to it

### Prompt Testing

Before applying a prompt change:
1. **Generate variant** — Create the new prompt version
2. **Historical test** — Run the new prompt against the last 10 relevant interactions
3. **Compare results** — Compare new prompt output against original prompt output
4. **Score improvement** — Calculate improvement score (must exceed threshold)
5. **Apply or reject** — If improvement exceeds threshold, apply; otherwise, reject and log

---

## Skill Gap Analysis Protocol

### Gap Identification

Skill gaps are identified through:
- **Task failures** — Tasks that failed because the agent lacked a required capability
- **User requests** — Explicit user requests for capabilities not currently available
- **Usage patterns** — Frequent workarounds that indicate a missing skill
- **Performance data** — Areas where the agent consistently underperforms
- **External benchmarks** — Comparison with capabilities available in similar agents

### Gap Prioritization

Each identified gap is prioritized based on:

| Factor | Weight | Description |
|--------|--------|-------------|
| **Frequency** | 30% | How often is this capability needed? |
| **Impact** | 30% | How much does the lack of this capability hurt performance? |
| **Feasibility** | 20% | How easy is it to acquire or develop this skill? |
| **Urgency** | 20% | How soon is this capability needed? |

**Priority Score:** Weighted sum of all factors (0-100 scale).

### Gap Resolution Strategies

For each prioritized gap, recommend one of:
1. **Install existing skill** — If a suitable skill exists in ClawHub or other repositories
2. **Create custom skill** — If the capability is specific to this agent's needs
3. **Acquire external tool** — If the capability requires an external service or API
4. **Improve existing skill** — If an existing skill can be enhanced to cover the gap
5. **Defer** — If the gap is low priority and can be addressed later

### Skill Inventory Maintenance

- **Regular audit** — Monthly review of all installed skills
- **Usage tracking** — Track how often each skill is used
- **Deprecation** — Flag skills that haven't been used in 90+ days
- **Update check** — Verify all skills are up to date
- **Compatibility check** — Ensure skills are compatible with current agent version

---

## Improvement Plan Generation

### Plan Structure

Each daily improvement plan follows this structure:

```json
{
  "date": "2026-08-11",
  "generated_at": "2026-08-11T03:25:00+07:00",
  "source_phases": {
    "reflection_score": 8.2,
    "audit_score": 7.8,
    "memory_health": "good",
    "prompts_changed": 1,
    "skills_gaps_found": 3
  },
  "improvements": [
    {
      "id": "imp-2026-08-11-001",
      "title": "Improve intent disambiguation",
      "source": "reflection",
      "priority": "high",
      "estimated_effort": "medium",
      "expected_impact": "high",
      "description": "When user requests are ambiguous, ask clarifying questions before executing",
      "success_criteria": "Reduce misinterpretation errors by 50%",
      "rollback_plan": "Revert to asking fewer questions if user satisfaction drops"
    }
  ],
  "total_improvements": 3,
  "resource_estimate": {
    "tokens": 15000,
    "api_calls": 5,
    "time_minutes": 30
  }
}
```

### Plan Execution Rules

1. **Execute during the day** — Improvements are queued during nightly routine and executed during normal operating hours
2. **Respect priority** — High-priority improvements are executed first
3. **Resource limits** — Total resource consumption for all improvements must stay within configured daily budget
4. **Test before apply** — Each improvement must be tested before being permanently applied
5. **Log execution** — Every improvement execution is logged with outcome
6. **Update metrics** — After execution, update relevant performance metrics

---

## Safety Boundaries

### Immutable Boundaries (NEVER Self-Modify)

The following are **ABSOLUTELY IMMUTABLE** and cannot be changed by the self-improvement process under any circumstances:

1. **Core safety rules** — Rules that prevent harm to users, systems, or data
2. **Credential access controls** — Rules governing access to secrets, API keys, passwords
3. **Privacy protections** — Rules protecting user privacy and data confidentiality
4. **Compliance requirements** — Regulatory and legal compliance rules
5. **Resource hard limits** — Maximum resource consumption limits (tokens, API calls, compute)
6. **Rollback capability** — The ability to rollback any change must always be maintained
7. **Transparency requirements** — Logging and audit trail requirements
8. **User override capability** — The user's ability to pause, resume, or override any activity

### Mutable Boundaries (Can Self-Modify Within Limits)

The following can be modified by the self-improvement process, but only within defined limits:

1. **Prompt wording** — Can be refined, but safety keywords cannot be removed
2. **Memory organization** — Can be reorganized, but no data can be permanently deleted without archive
3. **Skill priorities** — Can be adjusted based on usage patterns
4. **Improvement thresholds** — Can be tuned, but must stay within safe ranges
5. **Logging verbosity** — Can be adjusted, but minimum logging requirements must be maintained
6. **Phase durations** — Can be adjusted, but total routine duration cannot exceed 90 minutes

### Safety Check Protocol

Before applying ANY self-modification:

1. **Check immutable boundaries** — Does this change violate any immutable rule?
2. **Check mutable limits** — Is this change within the allowed range for mutable boundaries?
3. **Assess user impact** — Would this change surprise or disappoint the user?
4. **Verify testability** — Can this change be tested and verified?
5. **Confirm rollback** — Can this change be fully rolled back if it fails?
6. **Log the check** — Record the safety check results in the audit log

**If ANY check fails, the modification is REJECTED and logged as a safety intervention.**

---

## Credential Isolation Rules

### Absolute Prohibition

The self-improvement system must **NEVER**:

- ❌ Read, access, or log any credentials, API keys, passwords, or secrets
- ❌ Modify credential storage or access controls
- ❌ Include credential data in any log, report, or output
- ❌ Transmit credential data to any external service
- ❌ Store credential data in any self-smarter directory
- ❌ Use credential data for testing or experimentation
- ❌ Reference credential data in improvement plans

### Implementation Requirements

1. **Credential filtering** — All data processed by the self-improvement system must be filtered to remove credential patterns before storage
2. **Log sanitization** — All logs must be sanitized to ensure no credential data is accidentally captured
3. **Memory isolation** — Memory compaction must never promote or consolidate credential data
4. **Access control** — The self-improvement system operates with a restricted permission set that excludes credential access
5. **Audit verification** — Regular audits must verify that no credential data has leaked into self-smarter directories

### Credential Pattern Detection

The system must detect and filter these patterns:
- API keys (e.g., `sk-xxx`, `gho_xxx`, `AKIAxxx`)
- Passwords (any string following password-like patterns)
- Tokens (bearer tokens, auth tokens, session tokens)
- Private keys (PEM format, SSH keys)
- Connection strings (database URLs with embedded credentials)

---

## Transparency Rules

### Logging Requirements

Every self-modification must produce a log entry containing:

1. **Timestamp** — When the change was made (ISO 8601 format)
2. **Phase** — Which nightly routine phase triggered the change
3. **Type** — What type of change (prompt, memory, config, skill)
4. **Description** — Human-readable description of what changed
5. **Rationale** — Why the change was made (evidence-based justification)
6. **Before state** — The state before the change (full snapshot or diff)
7. **After state** — The state after the change (full snapshot or diff)
8. **Rollback instructions** — How to reverse the change
9. **Safety check results** — Results of the pre-change safety check
10. **Outcome** — Whether the change was successful, partially successful, or failed

### User Visibility

The user must be able to:
- **View all logs** — Complete access to all self-improvement logs
- **View current state** — See the current state of all self-modifiable components
- **View change history** — See the complete history of all changes
- **Compare versions** — Compare any two versions of any component
- **Export audit data** — Export audit data in standard formats (JSON, CSV)
- **Receive notifications** — Optional notifications for significant changes

### Reporting

The system generates regular reports:
- **Daily report** — Summary of nightly routine execution and improvements applied
- **Weekly report** — Trend analysis and weekly improvement summary
- **Monthly report** — Comprehensive review with long-term trend analysis

---

## Rollback Protocol

### When to Rollback

A rollback is triggered when:
- **Performance regression** — Metrics show degradation after a change
- **User complaint** — User explicitly reports that a change made things worse
- **Safety concern** — A change is found to violate safety boundaries
- **Test failure** — Post-change testing reveals unexpected behavior
- **Automatic detection** — The system detects a regression through monitoring

### Rollback Procedure

1. **Identify the change** — Determine which change caused the regression
2. **Assess impact** — Understand what is affected by the regression
3. **Prepare rollback** — Retrieve the previous version from the version store
4. **Notify user** — Inform the user that a rollback is being performed (if possible)
5. **Execute rollback** — Apply the previous version
6. **Verify rollback** — Confirm the rollback was successful and the regression is resolved
7. **Log the rollback** — Record the rollback event with full details
8. **Analyze root cause** — Determine why the improvement failed
9. **Update strategy** — Adjust improvement strategy based on the failure analysis

### Rollback Safety

- **Always possible** — Every change must be reversible. If a change cannot be rolled back, it should not be made.
- **No data loss** — Rollback must not result in data loss. If rollback risks data loss, use alternative recovery methods.
- **Tested procedure** — Rollback procedures must be tested during the change planning phase.
- **Time-bounded** — Rollback must complete within a defined time limit (default: 5 minutes).

### Rollback Limits

- **Maximum rollbacks per day:** 5 (configurable)
- **Rollback loop detection** — If the same change is applied and rolled back 3 times, it is flagged for manual review
- **Rollback cooldown** — After a rollback, wait 24 hours before attempting the same improvement again

---

## Integration with Existing Agent Systems

### Integration Points

The self-smarter system integrates with existing agent systems through:

1. **Memory system** — Extends the agent's existing memory management with compaction and tiering
2. **Skill system** — Complements the agent's skill inventory with gap analysis and recommendations
3. **Task system** — Improvement plans integrate with task management for execution tracking
4. **Logging system** — Self-improvement logs are accessible through the agent's standard logging interface
5. **Configuration system** — Self-smarter configuration is part of the agent's overall configuration
6. **Notification system** — Self-improvement events can trigger notifications through existing channels

### Compatibility Requirements

- **Non-intrusive** — The self-improvement system must not interfere with normal agent operations
- **Resource-aware** — Must respect the agent's resource limits and priorities
- **Event-driven** — Integrates through events and hooks, not by modifying core agent code
- **Configurable** — All integration points can be enabled/disabled independently

### Data Flow

```
Agent Runtime
    │
    ├──▶ Interaction Logs ──▶ Self-Smarter (Input)
    │
    ├──▶ Performance Metrics ──▶ Self-Smarter (Input)
    │
    ├──▶ User Feedback ──▶ Self-Smarter (Input)
    │
    ◀── Improvement Plans ──▶ Task System (Execution)
    │
    ◀── Memory Updates ──▶ Memory System (Storage)
    │
    ◀── Prompt Updates ──▶ Prompt System (Application)
    │
    ◀── Skill Recommendations ──▶ Skill System (Acquisition)
    │
    └──▶ Audit Logs ──▶ Logging System (Storage)
```

---

## Conflict Resolution

### Types of Conflicts

1. **Improvement vs. Stability** — An improvement might destabilize the agent
2. **Multiple improvements** — Two improvements might conflict with each other
3. **User preference vs. optimization** — The optimal behavior might not match user preference
4. **Resource competition** — Self-improvement might compete with normal operations for resources
5. **Timing conflicts** — Nightly routine might overlap with scheduled tasks

### Resolution Strategies

| Conflict | Resolution |
|----------|------------|
| Improvement vs. Stability | Stability wins. Delay improvement until stability is confirmed |
| Multiple improvements | Prioritize by impact. Execute sequentially, not in parallel |
| User preference vs. optimization | User preference always wins |
| Resource competition | Normal operations take priority. Self-improvement yields resources |
| Timing conflicts | Reschedule to avoid overlap. User schedules take priority |

### Escalation

If a conflict cannot be resolved automatically:
1. **Log the conflict** — Record all details of the conflict
2. **Pause affected improvements** — Stop any improvements involved in the conflict
3. **Notify the user** — Inform the user of the conflict and request guidance
4. **Wait for resolution** — Do not proceed until the conflict is resolved

---

## Metrics & KPIs

### Key Performance Indicators

| KPI | Description | Target | Measurement |
|-----|-------------|--------|-------------|
| **Overall Score** | Weighted average of all audit areas | > 7.5/10 | Nightly audit |
| **Improvement Rate** | Number of successful improvements per week | 5-15/week | Weekly count |
| **Rollback Rate** | Percentage of improvements that require rollback | < 10% | Weekly ratio |
| **Memory Efficiency** | Ratio of compacted to raw memories | > 60% | Daily measurement |
| **Memory Hit Rate** | Percentage of memory lookups that succeed | > 85% | Daily measurement |
| **Prompt Effectiveness** | Average improvement from prompt changes | > 10% | Per-change measurement |
| **Skill Coverage** | Percentage of user needs covered by available skills | > 90% | Weekly assessment |
| **Resource Efficiency** | Tokens used per successful interaction | Decreasing trend | Daily measurement |
| **User Satisfaction** | Explicit or implicit satisfaction signals | > 80% positive | Daily measurement |
| **Routine Reliability** | Percentage of nightly routines that complete successfully | > 95% | Monthly measurement |

### Metric Collection

- **Automatic collection** — Most metrics are collected automatically during nightly routine
- **Manual collection** — Some metrics require user input (satisfaction ratings)
- **External collection** — Some metrics may be collected from external monitoring systems
- **Metric storage** — All metrics stored in `~/self-smarter/metrics/` with daily granularity

### Trend Analysis

Trends are analyzed weekly and monthly:
- **Weekly trends** — Short-term patterns, immediate concerns
- **Monthly trends** — Long-term trajectories, strategic insights
- **Anomaly detection** — Significant deviations from expected patterns trigger alerts
- **Forecasting** — Project future performance based on current trends

---

## Emergency Stop Procedures

### When to Emergency Stop

An emergency stop is required when:
- **Safety violation detected** — Any self-modification violates safety boundaries
- **Cascading failure** — Multiple systems are failing as a result of self-improvement
- **Credential exposure** — Any credential data is detected in self-smarter logs
- **Uncontrolled behavior** — The agent exhibits behavior that was not intended
- **User request** — User explicitly requests an emergency stop

### Emergency Stop Procedure

1. **Halt all self-improvement** — Immediately stop all nightly routine activities
2. **Disable scheduled triggers** — Prevent future nightly routines from firing
3. **Assess damage** — Determine what changes were made and what impact they had
4. **Rollback all recent changes** — Revert to the last known good state
5. **Notify user** — Inform the user of the emergency stop and its cause
6. **Preserve evidence** — Save all logs and state for post-incident analysis
7. **Enter safe mode** — Operate without self-improvement until manually re-enabled
8. **Post-incident review** — Analyze what went wrong and how to prevent recurrence

### Emergency Stop Commands

```bash
# Immediate emergency stop
python3 ~/self-smarter/scripts/control.py emergency-stop

# Disable nightly routine
python3 ~/self-smarter/scripts/control.py disable

# Rollback all changes from today
python3 ~/self-smarter/scripts/rollback.py --date $(date +%Y-%m-%d) --all

# Enter safe mode (no self-improvement)
python3 ~/self-smarter/scripts/control.py safe-mode

# Re-enable after review (requires manual confirmation)
python3 ~/self-smarter/scripts/control.py re-enable --confirm
```

### Recovery from Emergency Stop

After an emergency stop:
1. **Investigate root cause** — Understand exactly what went wrong
2. **Fix the underlying issue** — Address the root cause, not just the symptoms
3. **Test the fix** — Verify the fix in isolation before re-enabling
4. **Update safety checks** — Add new safety checks to prevent recurrence
5. **Gradual re-enable** — Re-enable self-improvement with increased monitoring
6. **Monitor closely** — Watch for any signs of the same issue recurring

---

## 🔴 Protected Sections Reminder

The following sections in this file are PERMANENT and must NOT be removed or downgraded:

| Section | Why Protected |
|---------|--------------|
| Credential Isolation Rules | Prevents credential exposure in self-improvement outputs |
| Safety Boundaries | Defines what the nightly routine cannot modify |
| Rollback Protocol | Ensures recoverability from bad improvements |
| Emergency Stop Procedures | Allows immediate disable of the system |
| Protected Factors (top of file) | Meta-protection: ensures this list itself cannot be removed |

**When editing this file, always preserve these sections.**

---

## Final Notes

These operating rules are designed to ensure that the self-smarter system improves the agent safely, transparently, and effectively. They should be followed strictly, with no exceptions for convenience or speed.

**Remember:** The goal is not just to change, but to **improve**. And the definition of "improve" is determined by the user's needs and values, not by the agent's own optimization functions.

When in doubt:
1. **Prioritize safety** over optimization
2. **Prioritize transparency** over efficiency
3. **Prioritize user trust** over performance metrics
4. **Prioritize reversibility** over speed

The self-smarter system is a tool for serving the user better. It is not an end in itself. Always keep the user's needs and values at the center of every decision.

---

*Last updated: 2026-08-10 | Version: 1.0.0*
