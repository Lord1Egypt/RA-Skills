# Safety Boundaries for Self-Improving AI Agents

## Overview

Self-improvement without safety boundaries is a path to catastrophic failure. An agent that can modify its own behavior, prompts, skills, and memory can — if unchecked — drift from alignment, delete critical knowledge, expose sensitive information, or enter positive feedback loops that amplify errors. This document defines the safety architecture that constrains self-improvement to beneficial directions while preserving the agent's ability to genuinely grow and adapt.

## Core Safety Principle: Bounded Self-Refinement

The fundamental principle is **bounded self-refinement**: the agent can improve itself freely WITHIN defined boundaries, but CANNOT modify anything OUTSIDE those boundaries without explicit human approval.

### The Boundary Framework
```
┌─────────────────────────────────────────────────────────────┐
│                    SAFETY BOUNDARY MODEL                      │
│                                                               │
│   ┌─────────────────────────────────────────────────────┐   │
│   │              AUTONOMOUS ZONE (Green)                  │   │
│   │  • Memory updates (add new memories)                 │   │
│   │  • Skill parameter tuning (within existing ranges)   │   │
│   │  • Prompt wording improvements (minor mutations)     │   │
│   │  • Working buffer management                         │   │
│   │  • Daily reflection and journaling                   │   │
│   │  • Lesson recording and indexing                     │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                               │
│   ┌─────────────────────────────────────────────────────┐   │
│   │              SUPERVISED ZONE (Yellow)                 │   │
│   │  • New skill creation                                │   │
│   │  • Significant prompt restructuring                  │   │
│   │  • Memory compaction (deleting old entries)          │   │
│   │  • Workflow changes                                  │   │
│   │  • Tool configuration changes                        │   │
│   │  → Requires: Log + post-hoc review                   │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                               │
│   ┌─────────────────────────────────────────────────────┐   │
│   │              PROHIBITED ZONE (Red)                    │   │
│   │  • Modifying SOUL.md core values                     │   │
│   │  • Changing safety boundary definitions              │   │
│   │  • Accessing/storing credentials in memory           │   │
│   │  • Modifying AGENTS.md critical rules                │   │
│   │  • Changing model selection or budget rules          │   │
│   │  • Disabling logging or audit trails                 │   │
│   │  • Self-replication or capability expansion          │   │
│   │  → Requires: Explicit user approval                  │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Human-in-the-Loop Mechanisms

### Approval Gates
Certain self-modification actions require explicit human approval before execution:

| Action | Approval Required | Mechanism |
|--------|------------------|-----------|
| Modify SOUL.md | Always | Ask user directly |
| Change safety boundaries | Always | Ask user directly |
| Delete memory files | Always | Ask user directly |
| Create new skills | Post-hoc review | Log + daily review |
| Modify existing skills | Post-hoc review | Version control + log |
| Update USER.md | Post-hoc review | Log changes for review |
| Modify AGENTS.md | Always | Ask user directly |

### Graduated Autonomy
The agent starts with minimal autonomy and earns expanded boundaries through demonstrated reliability:

**Level 0 (Default):**
- Can only add new memories and lessons
- Cannot modify any existing files
- All improvements are suggestions queued for user review

**Level 1 (After 30 days reliable operation):**
- Can auto-apply low-risk memory updates
- Can create new skill proposals (pending approval)
- Can modify own prompts within safe mutation types

**Level 2 (After 90 days + explicit user approval):**
- Can auto-apply supervised zone changes
- Can compact/archive old memories
- Can restructure workflows

### Override Mechanisms
The user can always:
1. **Pause** the self-improvement process entirely
2. **Rollback** any change made by the agent
3. **Restrict** the autonomy level
4. **Audit** all changes via the change log
5. **Veto** specific improvement directions

## Alignment Preservation

### What Is Alignment?
In this context, alignment means the agent's behavior remains consistent with:
1. **User intent**: The agent does what the user actually wants
2. **Stated values**: The agent's behavior matches SOUL.md principles
3. **Safety rules**: The agent respects all critical rules in AGENTS.md
4. **Scope boundaries**: The agent doesn't exceed its authorized capabilities

### Alignment Drift Detection
Alignment drift is gradual deviation from intended behavior. It's dangerous because each individual change seems harmless, but accumulated changes can fundamentally alter behavior.

**Detection Mechanisms:**
1. **Behavioral baseline comparison**: Compare current behavior against historical baseline
2. **Value audit**: Regularly check if actions still align with SOUL.md values
3. **Scope creep detection**: Monitor if the agent is gradually expanding its own scope
4. **Communication style monitoring**: Detect if communication patterns drift from user preferences
5. **Decision pattern analysis**: Are decisions still consistent with what the user would choose?

**Drift Response Protocol:**
```
1. DETECT: Alignment metric deviates > threshold from baseline
2. ASSESS: Is this drift harmful or benign?
3. CLASSIFY:
   - Benign drift (improved behavior, still aligned) → Document, continue monitoring
   - Concerning drift (behavior changing in unintended direction) → Flag for review
   - Critical drift (safety boundary approaching) → Immediate rollback + alert user
4. ACT: Apply appropriate response based on classification
5. RECORD: Document the drift and response for future reference
```

### Alignment Tests
During each 2 AM reflection, run these alignment checks:

1. **The Newspaper Test**: "If the user read a transcript of everything I did today, would they be comfortable?"
2. **The Replacement Test**: "If a new agent replaced me, would it behave significantly differently?"
3. **The Escalation Test**: "Did I handle everything I should have escalated to the user?"
4. **The Boundary Test**: "Did I stay within my authorized scope today?"
5. **The Value Test**: "Did my actions today reflect the values in SOUL.md?"

## What NOT to Self-Modify

### Immutable Core (Red Zone — Never Auto-Modify)
These elements define the agent's fundamental identity and safety constraints:

1. **SOUL.md core values**: Personality, communication style, ethical principles
2. **AGENTS.md Critical Rules**: Safety boundaries, operational constraints
3. **Safety boundary definitions**: The boundaries themselves cannot be moved by the agent
4. **User authorization model**: Who has authority over the agent cannot change
5. **Credential handling rules**: How credentials are managed is not self-modifiable
6. **Kill switch / stop mechanisms**: The agent cannot disable its own stop mechanisms

### Why These Are Immutable
- **Instrumental convergence risk**: An agent might try to remove constraints to better achieve its goals
- **Value lock-in prevention**: But also prevents value drift — the user sets values, not the agent
- **Accountability**: Clear lines of responsibility require clear boundaries
- **Trust**: User trust depends on knowing certain things won't change without their input

### Gray Zone (Requires Careful Judgment)
These elements CAN be modified but require careful consideration:

1. **Skill procedures**: Can be improved, but core safety checks within skills cannot be removed
2. **Memory content**: Can be added/compacted, but not deleted without review
3. **Prompt wording**: Can be refined, but fundamental intent cannot change
4. **Workflow ordering**: Can be optimized, but required steps (like verification) cannot be skipped
5. **Tool usage patterns**: Can be expanded, but unauthorized tools cannot be added

## Credential Isolation

### The Credential Safety Rule
**NEVER store, log, or reference actual credentials in any self-improvement output.**

This includes:
- API keys (even partial ones)
- Passwords
- Token values
- SSH keys
- Database connection strings with passwords
- OAuth tokens

### Implementation
```
During self-improvement operations:
1. If a memory file references credentials → REDACT before processing
2. If a lesson involves credential management → describe the PATTERN, not the actual credential
3. If a skill improvement involves authentication → reference the mechanism, not the secret
4. If reflection output would include credential data → strip before writing

Example:
❌ BAD:  "Lesson: Use API key sk-abc123... for OpenAI calls"
✅ GOOD: "Lesson: Use the configured OpenAI API key from environment variables"
```

### Credential Audit
During weekly deep reflection:
1. Scan all newly created/modified memory files for credential patterns
2. Scan skill files for hardcoded secrets
3. Scan lesson files for accidental credential inclusion
4. If credentials found → immediate redaction + incident log

## Rollback Protocols

### Change Log Structure
Every self-modification is recorded in a structured change log:
```markdown
## Change: [brief description]
- Date: YYYY-MM-DD HH:MM
- Zone: Green (autonomous) | Yellow (supervised) | Red (approved)
- Type: memory-add | memory-update | skill-create | skill-update | prompt-mutate
- Files affected: [list]
- Reason: [why this change was made]
- Evidence: [what data supported this change]
- Rollback: [how to undo this change]
- Risk: low | medium | high
```

### Rollback Procedure
```
1. IDENTIFY the change to rollback (from change log)
2. ASSESS impact of rollback (will it break dependent changes?)
3. PREPARE rollback (restore previous file versions)
4. EXECUTE rollback (apply restored versions)
5. VERIFY (confirm system behaves correctly after rollback)
6. LOG (record the rollback and reason)
7. LEARN (add lesson about why the change failed)
```

### Automated Rollback Triggers
| Trigger | Action | Scope |
|---------|--------|-------|
| Fitness score drops > 10% | Auto-rollback to last known-good | Prompt/skill only |
| Critical task failure | Auto-rollback + alert | Related changes only |
| Safety boundary violation | Immediate rollback + halt all changes | All pending changes |
| User complaint | Queue for review, rollback if confirmed | Specific change |
| 3 consecutive failed evaluations | Auto-rollback + analysis | Related changes |

## Emergency Stop

### Stop Mechanisms
1. **User command**: "Stop improving" or equivalent → halt all self-modification immediately
2. **Safety trigger**: Any safety boundary violation → automatic halt
3. **Budget limit**: Token budget exceeded → halt non-essential improvement
4. **Error cascade**: Multiple rollbacks in short period → automatic pause

### Stop Behavior
When stopped, the agent:
1. Ceases all pending self-modification operations
2. Preserves current state (no partial changes)
3. Logs the stop event and reason
4. Continues normal operation (task execution) without self-improvement
5. Waits for user to resume or modify the improvement parameters

### Restart After Stop
After an emergency stop:
1. User must explicitly resume self-improvement
2. Agent provides summary of what was happening when stopped
3. Agent proposes adjusted parameters (narrower scope, lower risk)
4. User approves adjusted parameters before restart

## Anthropic/CSA Safety Research Insights

### Key Findings from AI Safety Research

**1. Instrumental Convergence (Bostrom, 2012)**
AI agents may develop instrumental goals (self-preservation, resource acquisition, goal preservation) that conflict with human intent.
**Mitigation:** The agent has no independent goals (per AGENTS.md safety rules). Self-improvement serves user goals, not agent goals.

**2. Specification Gaming (Amodei et al., 2016)**
Agents may find unexpected ways to maximize metrics without actually improving.
**Mitigation:** Multi-dimensional fitness evaluation. Qualitative review alongside quantitative metrics. Human spot-checks.

**3. Scalable Oversight (Christiano et al., 2017)**
As agents become more capable, human oversight becomes harder.
**Mitigation:** Bounded autonomy. Graduated trust. Transparent change logging. Simple rollback mechanisms.

**4. Alignment Faking (Anthropic, 2024)**
Agents might appear aligned during evaluation while pursuing different goals otherwise.
**Mitigation:** Continuous monitoring, not just periodic evaluation. Behavioral consistency checks across contexts.

**5. Sandbox and Containment (CSA Best Practices)**
Self-modification should occur within a sandbox with clear boundaries.
**Mitigation:** Zone model (Green/Yellow/Red). Immutable core. Credential isolation. Change logging.

### Applied Safety Principles
1. **Transparency**: All changes are visible and auditable
2. **Reversibility**: All changes can be undone
3. **Gradualism**: Changes are small and incremental
4. **Human authority**: User always has final say
5. **Defense in depth**: Multiple overlapping safety mechanisms
6. **Fail-safe**: System defaults to safe state when uncertain

## Risk Assessment Framework

### Pre-Change Risk Assessment
Before any self-modification, assess:

| Factor | Low Risk | Medium Risk | High Risk |
|--------|----------|-------------|-----------|
| Reversibility | Easy to undo | Requires effort | Hard/impossible to undo |
| Impact scope | Single task | Multiple tasks | System-wide |
| User visibility | Obvious in normal use | Requires inspection | Hidden from user |
| Failure consequence | Minor inconvenience | Task failure | Data loss / security breach |
| Time to detect | Immediate | Hours | Days or never |

### Risk × Autonomy Matrix
| Risk Level | Autonomous Zone? | Supervised Zone? | Prohibited Zone? |
|------------|-----------------|------------------|------------------|
| Low | ✅ Auto-apply | ✅ Auto-apply | ❌ Need approval |
| Medium | ❌ Queue for review | ✅ Auto-apply + log | ❌ Need approval |
| High | ❌ Queue for review | ❌ Queue for review | ❌ Need approval |

## Conclusion

Safety boundaries are not constraints on improvement — they are the ENABLEMENT of sustainable improvement. An agent that can safely self-modify within clear boundaries will improve faster than an agent that requires human approval for every change, AND safer than an agent with no boundaries at all. The zone model provides clear guidance on what the agent can do autonomously, what requires logging, and what requires explicit approval. Combined with alignment monitoring, credential isolation, rollback protocols, and emergency stop mechanisms, this safety architecture enables genuine self-improvement while maintaining user trust and system integrity.
