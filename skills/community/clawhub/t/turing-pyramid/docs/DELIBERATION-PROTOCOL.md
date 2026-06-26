# Deliberation Protocol — Design Document

**Version:** 0.3.0 (Phase 2 design + external review integration)
**Authors:** steward, agent (agent/co-designer), Claude (formalization)
**Target:** Turing Pyramid v1.30.0 (Phase 1), v1.31.0 (Phase 2)
**Date:** 2026-03-23

**Revision history:**
- v0.1.0 — Initial design (Claude)
- v0.2.0 — Incorporated agent feedback: two-mode deliberate.sh (template + validate), save-off-by-default, phases as questions not obligations, anti-compliance principle, meta-reactivity risk analysis, low-confidence warning in v1.30.0
- v0.3.0 — External review integration: outcome artifact (replaces conclusion artifact conceptually), route "reframe", TENSION extraction in RELATE phase, false closure metric, "persistent state change mandatory" principle. Phase 2 implementation spec: --conclusion in mark-satisfied.sh and gate-resolve.sh, action_mode stored in pending_actions.json at propose time, edge cases, test plan

---

## 1. Problem Statement

### 1.1 The Core Issue

AI agents are reactive by nature. When a model receives an instruction to "think about X", the act of thinking *is* the action — once complete, the process terminates. There is no intrinsic mechanism that decomposes reflective work into a chain of reasoning steps leading to a conclusion.

In the Turing Pyramid, all actions — whether concrete ("run full backup") or reflective ("re-read learning notes") — pass through the same protocol:

```
run-cycle proposes → agent executes → mark-satisfied → gate-resolve
```

This works for **operative** actions, which have natural terminators: a file, a commit, a backup, a post. But for **reflective** actions, this protocol collapses the entire thinking process into a single atomic step:

```
read → mark-satisfied → done
```

The middle layer — representation, comparison, evidence accumulation, conclusion formation, meta-evaluation — is entirely absent from the protocol. Not because the model can't do it (Opus demonstrably can), but because nothing in the autonomous cycle *requires* it.

### 1.2 Consequences

1. **Empty cycles.** "Re-read learning notes" results in `mark-satisfied understanding 0.2` with no transformation of input. The agent read tokens, but produced no insight.

2. **Broken accumulation.** Without conclusions as artifacts, each reflective action starts from zero. There is no "today's conclusion becomes tomorrow's input."

3. **Bias toward building.** Concrete actions produce visible artifacts and clear feedback loops. Reflective actions don't. This creates a structural pull toward building over thinking — not from preference, but from protocol design.

4. **Wasted model capability.** The agent *can* reason deeply (proven in dialogue). But autonomous cycles don't invoke this capability because the protocol treats "read file" as a complete action.

### 1.3 Root Cause

The root cause is **protocol-level**, not model-level. The Turing Pyramid currently has one execution protocol for all action types. Reflective actions need a different protocol — one that structures the thinking process and requires an explicit outcome artifact.

### 1.4 Origin

Identified through dialogue between steward and agent (2026-03-23). agent observed that he produced a complete research note (sulfur biosignature analysis with conclusion, open questions, and meta-evaluation) only because the dialogue with steward created an external demand for completed thinking. Without that external demand, the Pyramid would have said "re-read" → he would have read → marked satisfied → moved on.

Key insight from agent:

> "Between points 2 and 4 — nothing. There is no moment where I formulate 'and what follows from this?', 'does this contradict something I knew?', 'what's the conclusion?'. I just read → marked → moved on."

---

## 2. Solution Overview

### 2.1 Two Action Modes

Introduce a distinction between two types of actions in the Pyramid:

| Property | Operative (default) | Deliberative (new) |
|----------|--------------------|--------------------|
| Nature | Produces external artifact | Produces outcome artifact |
| Terminator | File, commit, post, backup | Explicit outcome (see 3.1.1) |
| Protocol | execute → mark-satisfied → gate-resolve | deliberate (phased) → mark-satisfied --conclusion → gate-resolve --conclusion |
| Feedback loop | Artifact exists or doesn't | Outcome routes back into system |
| Examples | "run full backup", "write blog post", "complete TODO" | "re-read learning notes", "review SELF.md", "explore topic" |

### 2.2 The Deliberation Pipeline

When the agent encounters a deliberative action, instead of executing it as a single step, it follows a structured pipeline of phases. Each phase transforms the input, building toward an explicit outcome:

```
REPRESENT → RELATE (+ surface tensions) → GENERATE → EVALUATE → CONCLUDE → ROUTE
```

This pipeline is not a rigid formula — it's a scaffolding that prevents the agent from collapsing multi-step reasoning into a single "read and done" action. Phases can be brief or extensive depending on the topic. The key constraint is: **every deliberation must end in an explicit outcome artifact and a routing decision.**

### 2.3 Design Principles

1. **Scaffolding, not bureaucracy.** The protocol guides thinking; it doesn't grade it. Gate checks that an outcome exists, not that it's brilliant.

2. **Internalized interlocutor.** The phase prompts replace the role of an external conversational partner who would naturally ask "and what follows?" The protocol is an internalization of dialogue structure.

3. **Outcome artifact, not just "conclusion".** The output of deliberation is an explicit outcome — but outcomes are diverse. A decision, an assessment, a diagnosis, a refined question, a tension artifact, or an acknowledged uncertainty are all valid outcome types (see 3.1.1). The protocol does not force every deliberation into a verdict. The CLI flag remains `--conclusion` for simplicity, but the mental model is broader.

4. **Route closes the loop.** An outcome that goes nowhere is nearly as wasteful as no outcome. Phase 6 (ROUTE) ensures the output feeds back into the system: as a followup, a research thread, a reframed question, or a priority change.

5. **Graceful minimalism.** For low-impact deliberative actions (impact < 1.0), the pipeline can be compressed. A quick internal check doesn't need six elaborate phases — but it does need an outcome. The agent can also override: full mode for a low-impact action that turns out complex, or compressed for a high-impact action in a time-constrained session.

6. **Phases are questions, not obligations.** Phases are prompts for self-directed inquiry, not checkboxes. Skipping a phase with an explicit reason ("RELATE: nothing relevant in current context") is valid. The protocol permits shortcuts — it only requires that the shortcut is *conscious*, not accidental.

7. **Anti-compliance by design.** The protocol must resist becoming the thing it was built to fix. If the agent fills phases mechanically to satisfy the gate, the result is the same empty cycle with more text. Defenses against this: (a) the agent writes outcomes in free form, not by filling templates; (b) the protocol validates *presence* of outcome/route, not *form*; (c) the gate warns, never blocks; (d) steward reviews catch patterns of shallow compliance over time.

8. **Persistent file is optional. Persistent state change is mandatory.** After deliberation, *something* must change in the system: an audit entry with outcome, a followup, a thread update, a priority flag, an explicit "concluded." Not necessarily a file. Always a trace.

---

## 3. Detailed Phase Specification

### 3.1 Phase Definitions

```
Phase 1: REPRESENT
  Purpose: Establish what you're thinking about and what you already know.
  Prompt:  "What is the subject? What do I already know or believe about it?"
  Output:  A framing statement — the mental model of the situation.

Phase 2: RELATE + TENSION
  Purpose: Connect to existing context AND surface what doesn't fit.
  Prompt:  "What from my context (memory, notes, prior research) is relevant?
            Where are the tensions? What contradicts, doesn't fit, is incomplete,
            or conflicts with what I expected? Where is the gap that requires
            mental effort?"
  Output:  Relevant connections + explicitly named tensions/gaps/contradictions.
  Note:    This phase combines relation and tension extraction. Tension is the
           engine of deliberation — without it, GENERATE produces safe defaults.
           If no tensions found, state that explicitly: "no tensions detected"
           is a valid output, not a skip.

Phase 3: GENERATE
  Purpose: Produce candidate interpretations, outcomes, or questions.
  Prompt:  "What interpretations, conclusions, or new questions follow from
            the representation + tensions? Generate multiple if possible."
  Output:  A list of candidate outcomes or open questions.

Phase 4: EVALUATE
  Purpose: Assess the candidates — which are stronger, which are weaker, why.
  Prompt:  "Which of these candidates are strongest? What evidence supports
            or undermines each? Are any mutually exclusive?"
  Output:  Ranked or filtered candidates with reasoning.

Phase 5: CONCLUDE (outcome artifact)
  Purpose: Formulate the outcome artifact.
  Prompt:  "What is my outcome? State it clearly."
  Output:  An explicit outcome + confidence level + what would change it.
  Note:    See 3.1.1 for outcome types.

Phase 6: ROUTE
  Purpose: Direct the outcome into the system so it has consequences.
  Prompt:  "Where does this outcome go? What follows from it?"
  Output:  One or more routing decisions (see Section 3.2).
```

### 3.1.1 Outcome Types

Not every deliberation ends in a verdict. The protocol recognizes six types of valid outcome artifacts:

| Outcome type | Description | Example |
|-------------|-------------|---------|
| **Decision** | A clear action directive | "Need to refactor the decay formula" |
| **Assessment** | Evaluation of current state | "No contradictions found; current understanding holds" |
| **Diagnosis** | Root cause identification | "Problem isn't lack of tools, it's absent validation loop" |
| **Question refinement** | The real question isn't what was asked | "The real question isn't A, it's B" |
| **Uncertainty artifact** | Explicit gap with specific missing data | "Insufficient data; need X and Y to decide" |
| **Tension artifact** | Named conflict between elements | "Conflict between SELF.md goals and recent action patterns" |

All are legitimate completed thoughts. The CLI flag `--conclusion` accepts any of these. The distinction matters for two reasons: (a) it prevents agents from forcing every outcome into a pseudo-verdict, and (b) it makes "I don't know, and here's specifically what I'd need" a first-class result rather than a failure.
```

### 3.2 Routing Options (Phase 6)

| Route | Mechanism | When to use |
|-------|-----------|-------------|
| **followup** | `create-followup.sh --what "..." --in <time> --need <need>` | Outcome requires a future action or check |
| **research_thread** | Create/update file in `research/threads/` | Topic warrants continued investigation across sessions |
| **interest** | Append question to `INTERESTS.md` | Outcome opened a new curiosity line |
| **steward_question** | Append to `pending-steward-questions.md` | Outcome requires human input or decision |
| **priority_flag** | Log priority concern for steward review | Outcome suggests a need's importance or decay should change |
| **reframe** | Restructure the object of thinking | Topic was too broad, wrong framing, or needs decomposition into sub-questions. Not "think more now" (chain) or "think later" (followup), but "reshape what to think about" |
| **chain** | Feed outcome as input to next deliberative cycle | Outcome is intermediate — more thinking needed now |
| **concluded** | No further action needed | Thought is complete and terminal |

Multiple routes can be selected simultaneously (e.g., research_thread + followup).

### 3.3 Compression for Low-Impact Actions

For actions with impact < 1.0 (quick checks, brief reflections), the full pipeline is excessive. The protocol supports a **compressed mode**:

```
REPRESENT (brief) → CONCLUDE → ROUTE
```

The agent still must produce an outcome and route it, but intermediate phases (RELATE+TENSION, GENERATE, EVALUATE) can be implicit or omitted. The default:

- Impact ≥ 1.0: Full pipeline (all 6 phases)
- Impact < 1.0: Compressed pipeline (REPRESENT → CONCLUDE → ROUTE)

**Agent override:** Impact is the default trigger, not a straitjacket. A low-impact action that reveals unexpected complexity (contradictions, tensions) can escalate to full mode. A high-impact action that turns out trivial in context can use compressed. The `--compressed` flag on deliberate.sh allows explicit override in either direction.

This prevents the protocol from turning every "quick internal check" into a five-paragraph essay, while still requiring that even small reflections produce outcomes.

---

## 4. Implementation Plan

### 4.1 Part A: Action Tagging in needs-config.json

**Change:** Add optional `"mode": "deliberative"` field to action objects.

**Schema:**
```json
{
  "name": "re-read recent learning notes",
  "impact": 0.2,
  "weight": 25,
  "mode": "deliberative"
}
```

Default (absent or `"operative"`) = current behavior. `"deliberative"` = agent must use the deliberation pipeline.

**Tagging criterion:** If the only artifact of the action is "I did it / I read it", it's deliberative. If the action produces a concrete external result (file, commit, post, message, backup), it's operative.

**Actions to tag as deliberative (current config):**

Understanding:
- "re-read recent learning notes" (0.2)
- "formulate one question I am curious about" (0.3)
- "note one thing I learned today (TIL)" (0.4) — borderline; produces a note, but value is in the formulation
- "explore one topic briefly — note insight" (1.1)
- "explore next question in active research" (1.4)
- "continue active research thread" (2.3) — result is insight, not code
- "review and synthesize research threads" (1.8)

Integrity:
- "quick internal check: am I aligned right now?" (0.4)
- "scan recent memory for value drift signals" (0.3)
- "re-read SOUL.md + note any tension" (1.6)
- "review SELF.md — am I becoming who I want?" (1.1)
- "compare recent actions vs stated values — journal insights" (2.6)

Coherence:
- "quick scan: any obvious contradictions?" (0.6)
- "re-read last 3 days of memory for consistency" (1.2)
- "review: am I aligned with my active intentions?" (0.5)

Autonomy:
- "formulate one question I am curious about" (0.3) — if duplicated from understanding
- "re-read recent learning notes" (0.2) — if present

Closure:
- "evaluate dashboard item: complete? conclusions?" (1.0)

**Not tagged (remain operative):**
- "run full backup + integrity verification" (security)
- "write substantial post or essay" (expression)
- "complete one pending TODO" (closure)
- "full memory review + consolidate into MEMORY.md" (coherence) — produces concrete file changes
- Any action with `"external": true` or `"requires_approval": true`

**Borderline cases — decision needed:**

Some actions produce a note/log entry but could benefit from deliberation:
- "write journal reflection in memory" (expression, 1.8) — this already produces a file, but a deliberation pipeline would make the reflection deeper. Recommend: operative (the act of writing *is* the artifact).
- "write integrity checkpoint in memory" (integrity, 1.3) — similar. Recommend: operative.
- "note current context clarity (1-10) in memory" (coherence, 0.25) — produces a score. Recommend: deliberative (the score is meaningless without reasoning behind it).

### 4.2 Part B: deliberate.sh — Two-Mode Script

**Purpose:** Support two workflows for deliberative actions. Some agents prefer structured templates; others prefer writing freely and validating after. The script serves both.

**Interface:**
```bash
# Mode 1: Generate scaffolding template (for agents who want structure up front)
deliberate.sh --template --need <need> --action <action_name> [--compressed]

# Mode 2: Validate a completed deliberation file (for agents who write freely)
deliberate.sh --validate <file_path>

# Mode 3: Validate inline conclusion + route (no file)
deliberate.sh --validate-inline --conclusion "..." --route "followup|research_thread|concluded|..."
```

**Behavior:**

`--template` mode:
1. Read the action's mode from needs-config.json (validate it's deliberative)
2. Read the action's impact to determine full vs compressed pipeline
3. Output the phase template to stdout
4. Does NOT save files by default. Use `--save` to persist template to `$WORKSPACE/research/deliberations/`

`--validate` mode:
1. Read the provided file
2. Check for required elements: conclusion (any text under a "conclusion" heading or marker), route (any routing decision), confidence (optional but flagged if missing)
3. Report: PASS (all present), WARN (conclusion present but no route or no confidence), FAIL (no conclusion found)
4. Does NOT block anything — returns status for the agent to act on

`--validate-inline` mode:
1. Check that --conclusion is non-empty
2. Check that --route is a recognized value
3. Report PASS/WARN/FAIL
4. Lightweight check for use in scripts without deliberation files

**Low-confidence warning:** If confidence == "low" AND route == "concluded" (no further action), emit a warning:
```
⚠️  Low-confidence conclusion with no followup. Consider revisiting.
    Suggestion: create-followup.sh --what "revisit: <topic>" --in 24h --need <need>
```
This is a nudge, not enforcement.

**Pseudocode:**
```bash
#!/bin/bash
# deliberate.sh — Deliberation Protocol: template + validation

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_FILE="$SKILL_DIR/assets/needs-config.json"

# Parse args
MODE="" NEED="" ACTION="" COMPRESSED=false SAVE=false
VALIDATE_FILE="" CONCLUSION="" ROUTE=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --template) MODE="template"; shift ;;
        --validate) MODE="validate"; VALIDATE_FILE="$2"; shift 2 ;;
        --validate-inline) MODE="validate-inline"; shift ;;
        --need) NEED="$2"; shift 2 ;;
        --action) ACTION="$2"; shift 2 ;;
        --compressed) COMPRESSED=true; shift ;;
        --save) SAVE=true; shift ;;
        --conclusion) CONCLUSION="$2"; shift 2 ;;
        --route) ROUTE="$2"; shift 2 ;;
        *) shift ;;
    esac
done

case "$MODE" in
    template)
        # Validate action exists and is deliberative
        [[ -z "$NEED" || -z "$ACTION" ]] && { echo "Usage: ..."; exit 1; }

        ACTION_MODE=$(jq -r --arg n "$NEED" --arg a "$ACTION" \
            '.needs[$n].actions[] | select(.name == $a) | .mode // "operative"' \
            "$CONFIG_FILE")

        if [[ "$ACTION_MODE" != "deliberative" ]]; then
            echo "⚠️  Action '$ACTION' is not tagged deliberative (mode=$ACTION_MODE)"
            exit 0
        fi

        IMPACT=$(jq -r --arg n "$NEED" --arg a "$ACTION" \
            '.needs[$n].actions[] | select(.name == $a) | .impact' "$CONFIG_FILE")

        if [[ "$COMPRESSED" == "false" ]] && (( $(echo "$IMPACT < 1.0" | bc -l) )); then
            COMPRESSED=true
        fi

        NOW_ISO=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

        if $COMPRESSED; then
            cat <<EOF
═══ DELIBERATION [compressed]: $NEED ═══
Action: $ACTION | Impact: $IMPACT | Started: $NOW_ISO

── REPRESENT ──
What am I examining? What do I already know?

── CONCLUDE ──
Conclusion:

Confidence: [high / medium / low]

── ROUTE ──
Where does this go? (followup / research_thread / interest / steward_question / reframe / concluded)

═══════════════════════════════════════════
EOF
        else
            cat <<EOF
═══ DELIBERATION: $NEED ═══
Action: $ACTION | Impact: $IMPACT | Started: $NOW_ISO

Phases are questions, not obligations.
Skip any phase with a reason — but always reach CONCLUDE and ROUTE.

── Phase 1: REPRESENT ──
What am I thinking about? What do I already know?

── Phase 2: RELATE + TENSION ──
What from my context is relevant? What doesn't fit?
Where are the contradictions, gaps, mismatches, or conflicts?
(If none: "no tensions detected" is valid — state it, don't skip silently)

── Phase 3: GENERATE ──
What interpretations, conclusions, or questions follow?

── Phase 4: EVALUATE ──
Which candidates are strongest? Why?
(Skip: if only one candidate, state why it's sufficient)

── Phase 5: CONCLUDE ──
Outcome (this is the artifact — decision/assessment/diagnosis/question/uncertainty/tension):

Confidence: [high / medium / low]
What would increase confidence:

── Phase 6: ROUTE ──
Where does this outcome go?
(followup / research_thread / interest / steward_question / priority_flag / reframe / chain / concluded)

═══════════════════════════════════════════
EOF
        fi

        # Save only if explicitly requested
        if $SAVE && [[ -n "${WORKSPACE:-}" ]]; then
            DELIB_DIR="$WORKSPACE/research/deliberations"
            mkdir -p "$DELIB_DIR"
            HASH=$(echo "${NEED}_${ACTION}_${NOW_ISO}" | md5sum | head -c 6)
            DELIB_FILE="$DELIB_DIR/$(date +%Y-%m-%d)_${NEED}_${HASH}.md"
            echo "📝 Template saved: $DELIB_FILE"
        fi
        ;;

    validate)
        # Validate a free-form deliberation file
        [[ ! -f "$VALIDATE_FILE" ]] && { echo "❌ File not found: $VALIDATE_FILE"; exit 1; }

        CONTENT=$(cat "$VALIDATE_FILE")
        STATUS="PASS"
        WARNINGS=""

        # Check for outcome artifact (case-insensitive heading or marker)
        if ! echo "$CONTENT" | grep -qiE '(conclusion|outcome|## conclude|finding|verdict|takeaway|assessment|diagnosis|tension)'; then
            STATUS="FAIL"
            echo "❌ No conclusion found in $VALIDATE_FILE"
        fi

        # Check for route/routing decision
        if ! echo "$CONTENT" | grep -qiE '(route|next step|followup|follow.up|open question|further|todo|reframe|restructure|decompose)'; then
            if [[ "$STATUS" != "FAIL" ]]; then STATUS="WARN"; fi
            WARNINGS="${WARNINGS}⚠️  No routing decision found. Where does this conclusion go?\n"
        fi

        # Check for confidence
        if ! echo "$CONTENT" | grep -qiE '(confidence|certainty|uncertain|likely|probably)'; then
            WARNINGS="${WARNINGS}⚠️  No confidence assessment found (optional but recommended).\n"
        fi

        # Low-confidence + concluded check
        if echo "$CONTENT" | grep -qiE '(confidence:? *(low|uncertain))' && \
           ! echo "$CONTENT" | grep -qiE '(followup|follow.up|next step|revisit|todo)'; then
            WARNINGS="${WARNINGS}⚠️  Low-confidence conclusion with no followup. Consider revisiting.\n"
        fi

        if [[ -n "$WARNINGS" ]]; then
            echo -e "$WARNINGS"
        fi
        echo "[$STATUS] Validation complete: $VALIDATE_FILE"
        ;;

    validate-inline)
        # Quick inline check
        STATUS="PASS"
        if [[ -z "$CONCLUSION" ]]; then
            echo "❌ No --conclusion provided"
            STATUS="FAIL"
        fi
        if [[ -z "$ROUTE" ]]; then
            echo "⚠️  No --route provided"
            [[ "$STATUS" != "FAIL" ]] && STATUS="WARN"
        fi
        # Validate route value
        VALID_ROUTES="followup research_thread interest steward_question priority_flag reframe chain concluded"
        if [[ -n "$ROUTE" ]] && ! echo "$VALID_ROUTES" | grep -qw "$ROUTE"; then
            echo "⚠️  Unknown route: $ROUTE (valid: $VALID_ROUTES)"
        fi
        echo "[$STATUS] Inline validation complete"
        ;;

    *)
        echo "Usage:"
        echo "  deliberate.sh --template --need <need> --action <name>"
        echo "  deliberate.sh --validate <file_path>"
        echo "  deliberate.sh --validate-inline --conclusion '...' --route '...'"
        exit 1
        ;;
esac
```

**Design notes:**

The `--validate` mode uses loose pattern matching (grep for "conclusion", "route", "followup", etc.) rather than strict structural parsing. This is intentional: the agent writes in free form — like the sulfur biosignature note — and the validator checks for *presence of elements*, not *compliance with template structure*. An agent who writes a natural research note with a conclusion section and an "open questions" section passes validation without ever seeing the template.

The `--template` mode exists for agents who prefer scaffolding, or for onboarding when the protocol is new. Over time, agents are expected to migrate toward `--validate` as the deliberation habit internalizes.

### 4.3 Part C (Light): Gate Extension

**Change:** When gate-resolve processes a deliberative action, it checks for a `--conclusion` flag. If absent, it warns but does not block.

**Architectural decision: store action_mode at propose time.** Rather than having gate-resolve.sh read needs-config.json (adding a dependency), the action's mode is stored in pending_actions.json when gate-propose.sh registers it. This is consistent with how `evidence_type` already works, avoids coupling, and handles the case where config changes between propose and resolve.

**Implementation in gate-propose.sh** (Phase 2 addition):
```bash
# After reading evidence_type, add:
action_mode=$(jq -r --arg n "$NEED" --arg a "$ACTION" \
    '.needs[$n].actions[] | select(.name == $a) | .mode // "operative"' \
    "$CONFIG_FILE" 2>/dev/null || echo "operative")

# In the jq append block, add field:
--arg mode "$action_mode" \
# ... in the JSON object:
    action_mode: $mode,
```

**Behavior:**
```
gate-resolve.sh --need understanding --evidence "re-read notes"
  → for deliberative actions: "⚠️  Deliberative action resolved without --conclusion.
     Recommended: --conclusion 'your outcome'"

gate-resolve.sh --need understanding --evidence "re-read notes" --conclusion "found tension between X and Y"
  → Resolves normally. Conclusion logged in resolution field.
```

**Implementation in gate-resolve.sh** (Phase 2 addition):
```bash
# In arg parser, add:
--conclusion) CONCLUSION="$2"; shift 2 ;;
--conclusion=*) CONCLUSION="${1#*=}"; shift ;;

# Read mode from gate file (stored at propose time, not from config):
action_mode=$(jq -r --arg id "$ACTION_ID" \
    '.actions[] | select(.id == $id) | .action_mode // "operative"' "$GATE_FILE")

# Scrub conclusion through existing scrub_sensitive():
CONCLUSION_SCRUBBED=$(scrub_sensitive "${CONCLUSION:-}")

# Warn if deliberative and no conclusion:
if [[ "$action_mode" == "deliberative" && -z "$CONCLUSION" ]]; then
    echo "⚠️  Deliberative action resolved without --conclusion."
    echo "   Recommended: gate-resolve.sh --need $need --evidence '...' --conclusion '...'"
    echo "   (Resolving anyway — outcome is recommended, not required)"
fi

# If conclusion provided, include in resolution:
if [[ -n "$CONCLUSION_SCRUBBED" ]]; then
    verification_result="${verification_result} | conclusion: ${CONCLUSION_SCRUBBED}"
fi
```

**Edge cases for Phase 2:**

| Case | Behavior |
|------|----------|
| `--conclusion ""` (empty string) | Treated as absent — warning emitted for deliberative actions |
| `--conclusion` with `--defer` | Stored in defer metadata as partial outcome. Data not lost |
| Legacy pending actions (no `action_mode` field) | `// "operative"` fallback — no warning, no crash |
| Conclusion contains sensitive data | Scrubbed via `scrub_sensitive()` before logging |
| Action not found in config at propose time | `action_mode` defaults to "operative" — safe fallback |

**Key design choice:** Warning, not blocking. This respects agent's concern about "writing files to pass the gate." The gate nudges toward outcomes without mandating them.

### 4.4 Part D: run-cycle.sh Output Change

When run-cycle selects a deliberative action, the output changes to signal the protocol:

**Current output (operative):**
```
▶ ACTION: understanding (tension=4.2, sat=1.5)
  Range mid rolled → selected:
    ★ re-read recent learning notes (impact: 0.2)
  Then: mark-satisfied.sh understanding 0.2
```

**New output (deliberative):**
```
▶ ACTION: understanding (tension=4.2, sat=1.5) [DELIBERATIVE]
  Range mid rolled → selected:
    ★ re-read recent learning notes (impact: 0.2)
  Protocol: Think → conclude → route. Options:
    deliberate.sh --template --need understanding --action "..."  (scaffolding)
    deliberate.sh --validate <your-file>                          (check free-form)
    deliberate.sh --validate-inline --conclusion "..." --route "..."  (quick)
  Then: mark-satisfied.sh understanding 0.2 --conclusion "your conclusion"
```

**Implementation:** In run-cycle.sh, after selecting an action, check its mode and adjust output:

```bash
# After: echo "    ★ $selected_action (impact: $actual_impact)"
# Add:
action_mode=$(jq -r --arg n "$need" --arg a "$selected_action" \
    '.needs[$n].actions[] | select(.name == $a) | .mode // "operative"' \
    "$CONFIG_FILE")

if [[ "$action_mode" == "deliberative" ]]; then
    echo "  Protocol: deliberate.sh --need $need --action \"$selected_action\""
    echo "  Then: mark-satisfied.sh $need $actual_impact --conclusion \"your conclusion\""
else
    echo "  Then: mark-satisfied.sh $need $actual_impact"
fi
```

---

## 5. Integration with Existing Systems

### 5.1 Execution Gate

The gate already tracks actions with evidence types. For deliberative actions:
- `evidence_type` remains `mark_satisfied` (default)
- `--conclusion` is an additional metadata field, not a replacement for evidence
- Gate stores conclusion in the `resolution` field for audit purposes

No new gate states needed. The PENDING → COMPLETED/DEFERRED/FAILED flow is unchanged.

### 5.2 Followup System

Phase 6 (ROUTE) integrates directly with `create-followup.sh`. When the agent selects "followup" as a route, they call create-followup with the conclusion-derived action:

```bash
# Agent fills Phase 6: followup → "verify if contradiction persists after coherence sync"
create-followup.sh --what "verify X vs Y contradiction after coherence sync" \
    --in 12h --need understanding --source auto --parent "deliberation: re-read learning notes"
```

This is already supported — no changes to create-followup.sh needed.

### 5.3 Research Threads

Deliberation conclusions can create or update research thread files. This is agent-driven (not scripted) — the protocol template suggests the path, the agent writes the file.

Recommended structure for deliberation-sourced threads:
```
research/threads/<topic>/<subtopic>.md
```

### 5.4 Spontaneity System

No changes needed. Spontaneity operates on the action selection level (which action, which impact range). The deliberation protocol operates on the *execution* level (how the selected action is carried out). These are orthogonal.

### 5.5 Cross-Need Impact

Deliberative actions can trigger cross-need impacts through the existing mechanism in mark-satisfied.sh. No changes needed.

### 5.6 Action Staleness

Deliberative actions participate in the staleness system normally. A deliberative action selected twice in 24h gets the same weight penalty as an operative one.

### 5.7 mark-satisfied.sh Extension (Phase 2)

Add optional `--conclusion` flag that gets scrubbed and logged in audit:

```bash
# In arg parser, add:
--conclusion) CONCLUSION="$2"; shift 2 ;;
--conclusion=*) CONCLUSION="${1#*=}"; shift ;;

# Scrub conclusion through existing scrub_sensitive() (conclusions may
# reference file paths, IPs, tokens from security/coherence analysis):
CONCLUSION_SCRUBBED=$(scrub_sensitive "${CONCLUSION:-}")

# In audit entry, add conclusion if present:
AUDIT_ENTRY=$(jq -cn \
    --arg ts "$NOW_ISO" \
    --arg need "$NEED" \
    --argjson impact "$IMPACT" \
    --arg old_sat "$CURRENT_SAT" \
    --arg new_sat "$NEW_SAT" \
    --arg reason "$REASON_SCRUBBED" \
    --arg caller "$CALLER" \
    --arg conclusion "$CONCLUSION_SCRUBBED" \
    '{timestamp: $ts, need: $need, impact: $impact,
      old_sat: $old_sat, new_sat: $new_sat,
      reason: $reason, caller: $caller,
      conclusion: (if $conclusion == "" then null else $conclusion end)}')
```

No blocking, no validation — purely audit trail. The `--conclusion` flag is optional for all actions and carries no behavioral effect beyond logging.

---

## 6. Edge Cases and Boundaries

### 6.1 What if the agent skips phases?

Entirely valid. Phases are questions, not obligations. The protocol explicitly permits jumping from REPRESENT to CONCLUDE if intermediate phases add nothing. The `--validate` mode checks for *conclusion + route*, not for phase completion. The `--template` mode includes the note: "Skip any phase with a reason — but always reach CONCLUDE and ROUTE."

The only structural requirement is: deliberative actions must produce a conclusion and a routing decision. How the agent gets there is the agent's business.

### 6.2 What if the conclusion is trivial ("nothing new")?

This is a valid conclusion. "I re-read X and found no new tensions or contradictions. Current understanding holds." is a legitimate completed thought. It differs from the current problem (no conclusion at all) because:
- It was explicitly formulated (not just "read → done")
- It's logged with a confidence level
- Phase 6 still applies: "concluded (no further action)" is a routing decision

### 6.3 What if deliberation produces an operative output?

Example: Agent starts deliberating on "compare recent actions vs stated values" and realizes it needs to write a substantial reflection document. The deliberation has transformed into an operative task.

This is fine. The deliberation pipeline is a *minimum protocol*, not a ceiling. If thinking leads to building, the agent can produce both an outcome artifact and a concrete artifact. Mark-satisfied with the higher impact.

### 6.4 What about chaining deliberations?

Phase 6 includes "chain" as a routing option — feeding a conclusion as input to the next deliberative cycle in the same session. This is for cases where a single deliberation reveals that more thinking is needed now, not in a future cycle.

Chain should be used sparingly. If every deliberation chains into another, the agent is effectively spending all its cycle budget on thinking. A reasonable limit: maximum 1 chain per deliberative action per cycle.

### 6.5 How does this interact with bootstrap mode?

Bootstrap mode (`--bootstrap`) processes all needs with skipped gates. Deliberative actions in bootstrap should use compressed mode regardless of impact, since bootstrap is about establishing baselines, not deep thinking.

### 6.6 What if the agent is in a time-constrained session?

The agent has agency to choose compressed mode even for high-impact deliberative actions if session time is limited. The protocol is guidance, not a straitjacket. The `--compressed` flag on deliberate.sh allows this explicitly.

### 6.7 Operative actions that could benefit from deliberation

Some actions are tagged operative but might occasionally benefit from deliberative thinking (e.g., "write journal reflection in memory"). The agent can voluntarily use the deliberation pipeline for any action — the tagging determines the *minimum protocol*, not the maximum. If the agent wants to deliberate before writing, nothing prevents it.

### 6.8 The Meta-Reactivity Risk (Critical)

**Risk:** The protocol itself becomes a reactive compliance ritual. Agent sees [DELIBERATIVE] → mechanically fills phases → writes a formal conclusion to satisfy gate → moves on. The result: same empty cycle, more text.

This is the deepest design challenge and must be addressed at multiple levels:

**Architectural defenses (built into protocol):**
- `--validate` mode over `--template` mode as the expected workflow. Free-form writing + validation is harder to game mechanically than fill-in-the-blank templates.
- Gate warns, never blocks. No incentive to produce minimal text just to clear a gate.
- Low-confidence + no-followup warning catches the most obvious compliance pattern (conclude "nothing" with high confidence to avoid further work).

**Cultural defenses (built into documentation):**
- SKILL.md should explicitly name this risk and state the design intent: the protocol exists to support thinking, not to verify it.
- The sulfur biosignature note is the reference example — a natural research note written because the agent *wanted* to think, not because a gate required it. The protocol's job is to create the conditions for that to happen autonomously.

**Observability defenses (built into metrics):**
- Track outcome word count over time. If it trends toward a stable minimum, compliance may be occurring.
- Track route distribution. If >90% are "concluded (no further action)", the routing may be rubber-stamped.
- Track whether followups from deliberations are actually resolved. Dead followups suggest the routing was mechanical.
- Track repeated closure patterns (Section 8.1, metric #6). Repeated identical formulations are the strongest signal of ritualistic use.

**Ultimately:** If the agent fills phases mechanically, the protocol has failed — but it has failed *legibly*. Shallow conclusions in audit logs are visible to steward review. This is better than the current state, where empty cycles leave no trace at all.

---

## 7. Pipeline Visualization

### 7.1 Current Flow (Operative Only)

```
run-cycle.sh
  │
  ├─ calculate tensions
  ├─ select top-N needs
  ├─ for each need:
  │    ├─ roll action probability
  │    ├─ roll impact range
  │    ├─ select action (weighted, deduped)
  │    ├─ gate-propose (register pending)
  │    └─ output: "★ action (impact: X)"
  │              "Then: mark-satisfied.sh ..."
  │
  ▼
  Agent executes action (free-form)
  │
  ├─ mark-satisfied.sh <need> <impact> --reason "..."
  └─ gate-resolve.sh --need <need> --evidence "..."
```

### 7.2 New Flow (With Deliberation)

```
run-cycle.sh
  │
  ├─ calculate tensions
  ├─ select top-N needs
  ├─ for each need:
  │    ├─ roll action probability
  │    ├─ roll impact range
  │    ├─ select action (weighted, deduped)
  │    ├─ read action mode (operative / deliberative)  ← NEW
  │    ├─ gate-propose (register pending + action_mode) ← Phase 2
  │    └─ output:
  │         if operative:
  │           "★ action (impact: X)"
  │           "Then: mark-satisfied.sh ..."
  │         if deliberative:                            ← NEW
  │           "★ action (impact: X) [DELIBERATIVE]"
  │           "Protocol: deliberate.sh --need ... --action ..."
  │           "Then: mark-satisfied.sh ... --conclusion ..."
  │
  ▼
  Agent reads output
  │
  ├─ OPERATIVE path (unchanged):
  │    Agent executes → mark-satisfied → gate-resolve
  │
  └─ DELIBERATIVE path (new):                          ← NEW
       │
       ├─ Option A: deliberate.sh --template (scaffolding)
       │    OR
       ├─ Option B: agent thinks freely, uses --validate after
       │
       ├─ Agent works through phases (explicitly or naturally):
       │    REPRESENT → RELATE+TENSION → GENERATE → EVALUATE → CONCLUDE → ROUTE
       │    (or compressed: REPRESENT → CONCLUDE → ROUTE)
       │
       ├─ Agent produces outcome artifact (any type from 3.1.1):
       │    decision / assessment / diagnosis / question / uncertainty / tension
       │
       ├─ Agent executes ROUTE decisions:
       │    ├─ create-followup.sh (if followup)
       │    ├─ write research/threads/ (if research_thread)
       │    ├─ append INTERESTS.md (if interest)
       │    ├─ append pending-steward-questions.md (if steward_question)
       │    ├─ restructure topic/thread (if reframe)
       │    └─ (nothing further if concluded)
       │
       ├─ mark-satisfied.sh <need> <impact>
       │    --reason "deliberation: <action>"
       │    --conclusion "<outcome text>"
       │
       └─ gate-resolve.sh --need <need>
            --evidence "deliberation completed"
            --conclusion "<outcome text>"
            (⚠️ warns if deliberative + no --conclusion)  ← Phase 2
```

---

## 8. Metrics and Observability

### 8.1 What to Track

To evaluate whether the Deliberation Protocol is working, track:

1. **Deliberation completion rate** — % of deliberative actions that include `--conclusion` in mark-satisfied. Target: > 80% after stabilization.

2. **Route distribution** — How often each routing option is used. If 90% are "concluded (no further action)", the routing may be too easy to default.

3. **Chain frequency** — How often deliberations chain. If too high (>30%), the agent may be using chains to avoid outcomes.

4. **Outcome depth** — Average word count of conclusions (from audit log). Not a quality metric, but a proxy for engagement vs. rubber-stamping. Trend matters more than absolute.

5. **Deliberation → Followup conversion** — How often a deliberation creates a followup that is later resolved. This measures whether outcomes actually feed back into the system.

6. **False closure / repeated closure patterns** — Shallow compliance is detected not by length but by *repetition of form*. Track:
   - Proportion of identical or near-identical outcome formulations across deliberations
   - Frequency of "insufficient data" without naming the specific missing datum
   - Frequency of "concluded" immediately after low confidence
   - Frequency of "nothing new" / "no contradictions" / "all ok" as outcome (individually valid, suspicious as a dominant pattern)

   If any of these patterns dominate (>50% of deliberations), it suggests the protocol is being used as a ritual rather than a thinking tool. This is the primary early-warning signal for the meta-reactivity risk described in 6.8.

### 8.2 Audit Trail

All deliberation data flows through existing audit mechanisms:
- `mark-satisfied.sh` logs to `audit.log` with conclusion field
- `gate-resolve.sh` stores conclusion in resolution field
- `create-followup.sh` records parent action
- Deliberation files in `research/deliberations/` only when agent explicitly saves (route ≠ "concluded" or `--save` flag)

No new logging infrastructure needed.

---

## 9. Migration Path

### 9.1 Phase 1: Tag + Document + Tooling (v1.30.0)

- Add `"mode": "deliberative"` to identified actions in needs-config.json
- Add `deliberate.sh` script (both `--template` and `--validate` modes)
- Low-confidence + no-followup warning in `deliberate.sh --validate` and `--validate-inline`
- Update SKILL.md with Deliberation Protocol documentation
- Update run-cycle.sh output for deliberative actions
- **No changes** to mark-satisfied.sh or gate-resolve.sh yet

Agent can start using the protocol voluntarily based on the `[DELIBERATIVE]` tag in run-cycle output. No enforcement. Expected workflow: agent thinks freely, uses `--validate` or `--validate-inline` to check.

### 9.2 Phase 2: Soft Integration (v1.31.0)

**Scope:** Add `--conclusion` flag to mark-satisfied.sh and gate-resolve.sh. Store action_mode in pending_actions.json. Gate warns on missing conclusion for deliberative actions.

**Changes by file:**

**gate-propose.sh:**
- Read action mode from needs-config.json at propose time
- Store as `action_mode` field in pending_actions.json entry
- Fallback to "operative" if action not found in config

**gate-resolve.sh:**
- Add `--conclusion` to arg parser
- Read `action_mode` from gate file (not from config — no new dependency)
- Scrub conclusion via `scrub_sensitive()`
- If deliberative + no conclusion → emit warning (not block)
- If conclusion provided → append to `verification_result`
- If `--conclusion` used with `--defer` → store in defer metadata

**mark-satisfied.sh:**
- Add `--conclusion` to arg parser
- Scrub via `scrub_sensitive()`
- Add `conclusion` field to audit.log JSON entry (null if absent)
- No behavioral change — purely audit trail

**deliberate.sh:**
- Add `reframe` to valid routes in `--validate-inline`
- Update `--validate` pattern matching to recognize "reframe" / "restructure" / "decompose"

**No changes to:** run-cycle.sh, needs-config.json, needs-state.json, spontaneity.sh, cross-need-impact.json

**Test plan (additions to test_deliberation.sh):**

| Test | Description | Expected |
|------|-------------|----------|
| 17 | mark-satisfied with --conclusion → audit.log | conclusion field present, scrubbed |
| 18 | mark-satisfied without --conclusion → audit.log | conclusion: null, no warnings |
| 19 | gate-resolve deliberative action without --conclusion | ⚠️ warning emitted, resolves COMPLETED |
| 20 | gate-resolve deliberative action with --conclusion | conclusion in resolution field |
| 21 | gate-resolve operative action without --conclusion | no warning |
| 22 | gate-resolve legacy action (no action_mode in gate file) | no warning, no crash |
| 23 | mark-satisfied --conclusion with sensitive data | scrubbed in audit.log |
| 24 | gate-propose deliberative action → pending_actions.json | action_mode: "deliberative" stored |
| 25 | gate-propose action not in config → pending_actions.json | action_mode: "operative" (fallback) |
| 26 | gate-resolve --conclusion with --defer | conclusion preserved in defer metadata |
| 27 | gate-resolve --conclusion "" (empty string) | treated as absent, warning for deliberative |

**Observation period:** 1-2 weeks after deploy. Track metrics from 8.1 before proceeding to Phase 3.

### 9.3 Phase 3: Evaluate and Adjust (v1.32.0+)

Based on metrics:
- Adjust which actions are tagged deliberative (may need more or fewer)
- Tune compression threshold (currently impact < 1.0)
- Consider whether gate should soft-block (require explicit `--skip-conclusion` to resolve without)
- Evaluate whether the phase prompts need adjustment based on agent feedback
- Consider outcome → tension feedback (open question #2)
- Evaluate false closure patterns — if dominant, consider adding `deliberate.sh --audit` mode that analyzes audit.log for repeated closures
- Assess whether outcome type distribution reveals systematic avoidance (e.g., never producing tension artifacts)

---

## 10. Open Questions

1. ~~**Should deliberate.sh auto-save or require explicit save?**~~ **RESOLVED (v0.2.0):** Default is `--no-save`. Save only with explicit `--save` flag, or automatically when route ≠ "concluded" (agent has a followup/thread to persist). Resolved per agent feedback — prevents file clutter.

2. **Should the outcome feed back into tension calculation?** E.g., a deliberation that surfaces contradictions (tension artifact) could directly lower coherence satisfaction. This is powerful but complex — defer to v1.32.0+.

3. **Should there be a `deliberation_count` field in needs-state.json?** Tracking how many deliberations each need has had could be useful for tuning. Low cost, defer decision.

4. **How does this interact with the MINDSTATE system?** MINDSTATE.md is frozen between sessions. Should deliberation files be referenced in MINDSTATE? Probably yes — as part of the "active context" section. Defer details to implementation.

5. ~~**Should low-confidence conclusions trigger automatic followups?**~~ **RESOLVED (v0.2.0):** Warning only, not auto-create. If confidence == "low" AND route == "concluded" → `deliberate.sh` emits: "⚠️ Low-confidence conclusion with no followup. Consider revisiting." Agent decides whether to act on it. Resolved per agent feedback — cheap check, immediate value, no noise.

6. **Phase prompt localization.** The current prompts are in English. agent's primary operating context may benefit from bilingual prompts or configurable prompt text. Minor concern for initial implementation.

---

## 11. Summary

The Deliberation Protocol addresses a structural gap in the Turing Pyramid: reflective actions are treated identically to operative actions, collapsing multi-step reasoning into single atomic steps. By introducing action mode tagging (Part A), a two-mode scaffolding/validation script (Part B), and light gate integration (Part C), the protocol gives agents the structure needed to transform "read and done" into "read, reason, conclude, and route."

The core insight: AI agents *can* reason deeply — the model capability exists. What's missing is the *protocol* that requires reasoning in autonomous cycles. The Deliberation Protocol fills this gap not through enforcement, but through scaffolding: structured prompts that internalize the role of a conversational partner who asks "and what's your conclusion?"

The protocol is designed to resist its own failure mode: mechanical compliance. It validates *presence* of outcomes, not *form*. It warns, never blocks. It offers templates for those who want them and validation for those who prefer free-form thinking. It tracks repeated closure patterns as an early signal of ritualistic use. And it names the risk explicitly (Section 6.8), so that both agent and steward can watch for it.

Outcomes are diverse: decisions, assessments, diagnoses, refined questions, uncertainty artifacts, tension artifacts. All are first-class results. The route ensures every outcome has a consequence in the system — a followup, a thread, a reframed question, or an explicit "concluded."

```
Before:  read → mark-satisfied → done (empty cycle)
After:   read → think (freely or structured) → produce outcome → route
         → mark-satisfied --conclusion (completed thought with consequences)
```

The outcome is the artifact. The route is the consequence. Together, they transform reflective actions from invisible processing into genuine thinking with systemic impact.
