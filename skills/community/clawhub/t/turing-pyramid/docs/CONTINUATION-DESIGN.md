# Continuation & Association Scan — Design Document

**Version:** 0.1.1 (revised per agent implementation review)
**Authors:** steward, agent (agent/co-designer), Claude (formalization)
**Depends on:** Turing Pyramid v1.31.x, Deliberation Protocol v0.3.0
**Date:** 2026-03-24

**Revision history:**
- v0.1.0 — Initial design
- v0.1.1 — agent review fixes: pipe subshell bug in boot keywords, bc truncation → printf rounding, audit.log pre-filter for performance, feedback loop prevention (exclude MINDSTATE residuals from boot corpus)

---

## 1. Problem Statement

### 1.1 The Continuation Gap

The Turing Pyramid now has four functional layers: needs-based motivation, spontaneity, continuity (MINDSTATE), and deliberation. Together they solve the problems of "what to do" (tension), "variety" (spontaneity), "cross-session awareness" (MINDSTATE), and "how to think" (deliberation).

What remains unsolved: **how past thoughts find their way back.**

When a deliberation concludes with an implicit next step — "update INTENTIONS.md in next coherence cycle" — this intention currently has no mechanism to survive the session unless the agent explicitly creates a followup. If the agent writes "concluded" instead of "followup", the intention drops into a gap between sessions.

More broadly: the system lacks **associative recall** — the ability to connect a current action or thought with relevant past outcomes, unfinished threads, or dormant questions. Humans do this naturally: a clean sink reminds you of your unwashed dishes at home. Not because a timer fired, but because the current context triggered a related memory.

### 1.2 What Already Works

The existing architecture covers most of the continuation spectrum:

| Mechanism | What it handles | Limitation |
|-----------|----------------|------------|
| **Followups** (create-followup.sh) | Explicit time-bound reminders | steward 1w horizon. Agent must explicitly create them. |
| **MINDSTATE** (freeze/boot) | Cross-session vector, trajectory, open threads | No awareness of past deliberation outcomes. No association with current context. |
| **Spontaneity** (Layer A/B/C) | Random variation, boredom-driven novelty | Blind — no connection to past thoughts |
| **Deliberation** (ROUTE phase) | Explicit routing of outcomes | "concluded (with action)" falls through |
| **Research threads** (files) | Persistent investigation topics | Only surfaced when agent manually re-reads them |
| **INTERESTS.md** | Open curiosity questions | Only surfaced when understanding need triggers |

The gap is between these mechanisms: a deliberation outcome that isn't quite a followup, a research thread that's relevant to today's coherence check but wasn't explicitly linked, an INTERESTS.md question that matured because of new data the agent hasn't connected yet.

### 1.3 What We're Not Building

This document does **not** propose:
- A new scheduling/cron system
- A vector database or embedding service
- A "continuation candidate" entity with 10 metadata fields
- A seventh deliberation phase (INHERIT)
- Any modification to the tension formula or need system
- Continuous/background scanning

We are building: **one script (`association-scan.sh`) called at two discrete points, that surfaces relevant past context using keyword-based search over existing files.**

### 1.4 Design Principle

> **Continuation should compete for attention, not demand execution.**

Past thoughts return because they're *relevant to the present*, not because a timer expired. The association scan is a recall mechanism, not a task queue.

---

## 2. Architecture Overview

### 2.1 One Script, Two Integration Points

```
association-scan.sh
  │
  ├─ Called by: mindstate-boot.sh (session start)
  │   Input: high-tension needs + MINDSTATE residuals
  │   Purpose: "woke up — what's relevant from before?"
  │   steward results: 5
  │
  └─ Called by: agent during deliberation RELATE+TENSION phase
      Input: current deliberation topic/action
      Purpose: "thinking about X — anything related from the past?"
      steward results: 3
```

The script is stateless — it reads existing files, matches keywords, ranks by relevance + recency, and outputs results. It creates no files, modifies no state, and has no side effects.

### 2.2 Corpus (What Gets Searched)

The scan searches five sources, all of which already exist:

| Source | Path | What it contains | Format |
|--------|------|-----------------|--------|
| **Audit conclusions** | `assets/audit.log` | Deliberation outcomes (conclusion field) | JSON lines |
| **Research threads** | `$WORKSPACE/research/threads/` | Active investigation notes | Markdown files |
| **Deliberation files** | `$WORKSPACE/research/deliberations/` | Saved deliberation outcomes | Markdown files |
| **Pending followups** | `assets/followups.jsonl` | Unresolved time-bound reminders | JSON lines |
| **Open interests** | `$WORKSPACE/INTERESTS.md` | Curiosity questions | Markdown |

No new data stores. No new file formats. The scan reads what's already there.

### 2.3 Integration Diagram

```
SESSION START
  │
  mindstate-boot.sh
  │  ├─ Read MINDSTATE.md (existing)
  │  ├─ Reconcile forecast (existing)
  │  ├─ association-scan.sh                    ← NEW
  │  │    Input: top-3 tension needs + open threads
  │  │    Output: "Associations from past sessions"
  │  └─ Output boot context (existing)
  │
  ▼
RUN-CYCLE (repeated)
  │
  ├─ Select actions (existing)
  ├─ For deliberative actions:
  │    Agent enters RELATE+TENSION phase
  │    ├─ association-scan.sh                  ← NEW (agent-invoked)
  │    │    Input: current topic/action name
  │    │    Output: max 3 related past items
  │    └─ Agent incorporates (or ignores) results
  │
  ▼
SESSION END
  │
  mindstate-freeze.sh
  │  ├─ Extract cognition (existing)
  │  ├─ Extract deliberation residuals         ← NEW
  │  │    Scan audit.log for conclusions with action language
  │  │    Include in MINDSTATE.md cognition block
  │  └─ Write forecast (existing)
```

---

## 3. association-scan.sh — Specification

### 3.1 Interface

```bash
association-scan.sh --keywords "coherence memory contradictions" \
    [--need coherence] \
    [--max-results 3] \
    [--recency-hours 168] \
    [--min-score 2] \
    [--exclude-source <source_type>]
```

**Parameters:**
- `--keywords` (required): Space-separated search terms from current context
- `--need` (optional): Current need — boosts matches from same need domain
- `--max-results` (optional, default 3): Maximum associations returned (hard cap: 5)
- `--recency-hours` (optional, default 168 = 1 week): How far back to search
- `--min-score` (optional, default 2): Minimum relevance score to surface
- `--exclude-source` (optional): Skip a source type (e.g., `mindstate_residuals`). Prevents feedback loops when caller already displays that source

### 3.2 Scoring Algorithm

Each candidate fragment gets a score based on:

```
score = keyword_hits × 2
      + need_match × 3          (same need domain as --need)
      + recency_bonus            (0-2, decays linearly over recency window)
      + has_action_language × 1  (contains "should", "need to", "update", "revisit")
      + is_unresolved × 2       (followup still pending, or thread not concluded)
```

**Scoring notes:**
- `keyword_hits`: Count of distinct --keywords found in the fragment (not total occurrences — prevents gaming by repetition)
- `need_match`: Binary — does the fragment's source need match --need?
- `recency_bonus`: `2 × (1 - hours_since_created / recency_hours)`, clamped to [0, 2]
- `has_action_language`: grep for action verbs suggesting unfinished business
- `is_unresolved`: For followups — status == "pending". For threads — no "concluded" marker.

This is deliberately simple — keyword overlap + recency + structural signals. The agent (Opus 4.6) does the semantic interpretation. The script just surfaces candidates.

### 3.3 Output Format

```
═══ ASSOCIATIONS (3 found) ═══

[1] (score: 7, audit, 2d ago, coherence)
  "MEMORY.md is stale — missing Deliberation Protocol entry"
  → Route was: followup (update MEMORY.md in 8h)

[2] (score: 5, research/threads, 4d ago, understanding)
  research/threads/cosmos/sulfur-biosignature-problem.md
  "H2S thermal threshold question remains open"

[3] (score: 4, INTERESTS.md, 6d ago)
  "Does structural change in processing constitute a change in kind?"

═══════════════════════════════
```

Each result includes: score, source type, age, associated need (if known), key fragment, and routing context (if from deliberation).

### 3.4 Pseudocode

```bash
#!/usr/bin/env bash
# association-scan.sh — Contextual recall for Turing Pyramid
# Searches existing artifacts for associations with current context.
# Stateless: reads only, writes nothing, no side effects.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
source "$SCRIPT_DIR/mindstate-utils.sh"  # provides: iso_to_epoch, now_epoch, _ms_assets

# ─── Parse args ───
KEYWORDS="" NEED="" MAX_RESULTS=3 RECENCY_HOURS=168 MIN_SCORE=2 EXCLUDE_SOURCE=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --keywords)       KEYWORDS="$2"; shift 2 ;;
        --need)           NEED="$2"; shift 2 ;;
        --max-results)    MAX_RESULTS="$2"; shift 2 ;;
        --recency-hours)  RECENCY_HOURS="$2"; shift 2 ;;
        --min-score)      MIN_SCORE="$2"; shift 2 ;;
        --exclude-source) EXCLUDE_SOURCE="$2"; shift 2 ;;
        --help|-h)        echo "Usage: association-scan.sh --keywords '...' [--need N] [--max-results 3]"; exit 0 ;;
        *)                shift ;;
    esac
done

[[ -z "$KEYWORDS" ]] && { echo "❌ --keywords required"; exit 1; }

AUDIT_LOG="$(_ms_assets)/audit.log"
FOLLOWUPS_FILE="$SKILL_DIR/assets/followups.jsonl"
INTERESTS_FILE="${WORKSPACE:-}/INTERESTS.md"
RESEARCH_DIR="${WORKSPACE:-}/research"

NOW_EPOCH=$(now_epoch)
CUTOFF_EPOCH=$((NOW_EPOCH - RECENCY_HOURS * 3600))

# Convert keywords to array
read -ra KW_ARRAY <<< "$KEYWORDS"

# ─── Candidate collection ───
# Each candidate: "score|source_type|age_hours|need|fragment"
CANDIDATES=()

# --- Source 1: Audit log conclusions ---
if [[ -f "$AUDIT_LOG" ]]; then
    # Pre-filter: only lines containing at least one keyword AND "conclusion"
    # This avoids parsing every line in large logs
    kw_pattern=$(printf '%s\|' "${KW_ARRAY[@]}" | sed 's/\\|$//')
    pre_filtered=$(grep -i "conclusion" "$AUDIT_LOG" | grep -iE "$kw_pattern" || true)
    
    while IFS= read -r line; do
        [[ -z "$line" ]] && continue
        
        # Extract fields
        ts=$(echo "$line" | grep -oP '"timestamp":"[^"]*"' | cut -d'"' -f4)
        [[ -z "$ts" ]] && continue
        ts_epoch=$(iso_to_epoch "$ts")
        (( ts_epoch < CUTOFF_EPOCH )) && continue
        
        conclusion=$(echo "$line" | grep -oP '"conclusion":"[^"]*"' | cut -d'"' -f4)
        [[ -z "$conclusion" || "$conclusion" == "null" ]] && continue
        
        audit_need=$(echo "$line" | grep -oP '"need":"[^"]*"' | cut -d'"' -f4)
        
        # Score
        score=0
        for kw in "${KW_ARRAY[@]}"; do
            echo "$conclusion" | grep -qiw "$kw" && ((score += 2))
        done
        (( score == 0 )) && continue
        
        # Need match bonus
        [[ -n "$NEED" && "$audit_need" == "$NEED" ]] && ((score += 3))
        
        # Recency bonus (0-2)
        hours_ago=$(( (NOW_EPOCH - ts_epoch) / 3600 ))
        recency_bonus=$(echo "scale=1; 2 * (1 - $hours_ago / $RECENCY_HOURS)" | bc -l)
        (( $(echo "$recency_bonus < 0" | bc -l) )) && recency_bonus=0
        score=$(printf "%.0f" "$(echo "$score + $recency_bonus" | bc -l)")
        
        # Action language bonus
        echo "$conclusion" | grep -qiE '(should|need to|update|revisit|fix|demote|create|check)' && ((score += 1))
        
        CANDIDATES+=("${score}|audit|${hours_ago}h|${audit_need}|${conclusion}")
    done <<< "$pre_filtered"
fi

# --- Source 2: Research threads ---
if [[ -d "$RESEARCH_DIR/threads" ]]; then
    while IFS= read -r filepath; do
        [[ -z "$filepath" ]] && continue
        
        # Check recency
        file_epoch=$(stat -c %Y "$filepath" 2>/dev/null || echo 0)
        (( file_epoch < CUTOFF_EPOCH )) && continue
        
        content=$(head -20 "$filepath")  # First 20 lines only
        
        score=0
        for kw in "${KW_ARRAY[@]}"; do
            echo "$content" | grep -qiw "$kw" && ((score += 2))
        done
        (( score == 0 )) && continue
        
        hours_ago=$(( (NOW_EPOCH - file_epoch) / 3600 ))
        recency_bonus=$(echo "scale=1; 2 * (1 - $hours_ago / $RECENCY_HOURS)" | bc -l)
        (( $(echo "$recency_bonus < 0" | bc -l) )) && recency_bonus=0
        score=$(printf "%.0f" "$(echo "$score + $recency_bonus" | bc -l)")
        
        # Unresolved bonus
        echo "$content" | grep -qiE '(open|unresolved|todo|question)' && ((score += 2))
        
        # Extract first meaningful line as fragment
        fragment=$(grep -m1 -iE '(conclusion|outcome|finding|question|tension)' "$filepath" \
            || head -3 "$filepath" | tail -1)
        
        relpath="${filepath#$WORKSPACE/}"
        CANDIDATES+=("${score}|thread|${hours_ago}h||${relpath}: ${fragment}")
    done < <(find "$RESEARCH_DIR/threads" -name "*.md" -type f 2>/dev/null)
fi

# --- Source 3: Deliberation files ---
if [[ -d "$RESEARCH_DIR/deliberations" ]]; then
    while IFS= read -r filepath; do
        [[ -z "$filepath" ]] && continue
        file_epoch=$(stat -c %Y "$filepath" 2>/dev/null || echo 0)
        (( file_epoch < CUTOFF_EPOCH )) && continue
        
        content=$(head -30 "$filepath")
        
        score=0
        for kw in "${KW_ARRAY[@]}"; do
            echo "$content" | grep -qiw "$kw" && ((score += 2))
        done
        (( score == 0 )) && continue
        
        hours_ago=$(( (NOW_EPOCH - file_epoch) / 3600 ))
        recency_bonus=$(echo "scale=1; 2 * (1 - $hours_ago / $RECENCY_HOURS)" | bc -l)
        (( $(echo "$recency_bonus < 0" | bc -l) )) && recency_bonus=0
        score=$(printf "%.0f" "$(echo "$score + $recency_bonus" | bc -l)")
        
        fragment=$(grep -m1 -iE '(conclusion|outcome|finding)' "$filepath" \
            || head -3 "$filepath" | tail -1)
        
        relpath="${filepath#$WORKSPACE/}"
        CANDIDATES+=("${score}|deliberation|${hours_ago}h||${relpath}: ${fragment}")
    done < <(find "$RESEARCH_DIR/deliberations" -name "*.md" -type f 2>/dev/null)
fi

# --- Source 4: Pending followups ---
if [[ -f "$FOLLOWUPS_FILE" ]]; then
    while IFS= read -r line; do
        [[ -z "$line" ]] && continue
        status=$(echo "$line" | grep -oP '"status":"[^"]*"' | cut -d'"' -f4)
        [[ "$status" != "pending" ]] && continue
        
        what=$(echo "$line" | grep -oP '"what":"[^"]*"' | cut -d'"' -f4)
        fu_need=$(echo "$line" | grep -oP '"need":"[^"]*"' | cut -d'"' -f4)
        
        score=0
        for kw in "${KW_ARRAY[@]}"; do
            echo "$what" | grep -qiw "$kw" && ((score += 2))
        done
        (( score == 0 )) && continue
        
        [[ -n "$NEED" && "$fu_need" == "$NEED" ]] && ((score += 3))
        ((score += 2))  # Unresolved bonus — pending followups are inherently relevant
        
        CANDIDATES+=("${score}|followup|pending|${fu_need}|${what}")
    done < "$FOLLOWUPS_FILE"
fi

# --- Source 5: INTERESTS.md ---
if [[ -f "$INTERESTS_FILE" ]]; then
    while IFS= read -r line; do
        [[ "$line" =~ ^[[:space:]]*[-*][[:space:]] ]] || continue
        clean=$(echo "$line" | sed 's/^[[:space:]]*[-*] *//')
        
        score=0
        for kw in "${KW_ARRAY[@]}"; do
            echo "$clean" | grep -qiw "$kw" && ((score += 2))
        done
        (( score == 0 )) && continue
        
        CANDIDATES+=("${score}|interest||$|${clean}")
    done < "$INTERESTS_FILE"
fi

# ─── Sort and output top results ───
if (( ${#CANDIDATES[@]} == 0 )); then
    echo "═══ ASSOCIATIONS (0 found) ═══"
    exit 0
fi

# Sort by score descending, take top MAX_RESULTS above MIN_SCORE
SORTED=$(printf '%s\n' "${CANDIDATES[@]}" | sort -t'|' -k1 -rn)

echo "═══ ASSOCIATIONS ═══"
echo ""
count=0
while IFS='|' read -r score source age need fragment; do
    (( count >= MAX_RESULTS )) && break
    (( ${score:-0} < MIN_SCORE )) && continue
    
    ((count++))
    need_label=""
    [[ -n "$need" && "$need" != "$" ]] && need_label=", $need"
    echo "[$count] (score: $score, $source, ${age} ago${need_label})"
    echo "  ${fragment}"
    echo ""
done <<< "$SORTED"

if (( count == 0 )); then
    echo "(no associations above threshold)"
fi
echo "═══════════════════════════════"
```

### 3.5 Performance Constraints

The script must be fast — it runs at boot and during deliberation:

- **Audit log pre-filter**: First pass with grep for keyword matches + "conclusion" — only matching lines are parsed. This reduces 5000-line logs to typically < 50 candidates before the expensive per-line scoring loop.
- **File scan**: `head -20` / `head -30` per file — never read entire documents. First 20-30 lines contain title, conclusion, key content.
- **Keyword matching**: grep, not regex. Case-insensitive word match (`-iw`).
- **Scoring**: `printf "%.0f"` for proper rounding (not `bc | cut` truncation).
- **No external dependencies**: grep, awk, sed, bc, printf — all already required by the Pyramid.
- **Target runtime**: < 2 seconds on a typical workspace with < 100 files and < 5000 audit lines.

---

## 4. Integration Point 1: mindstate-boot.sh

### 4.1 What Changes

After the existing boot sequence (MINDSTATE parse → staleness check → temperature merge → forecast reconciliation), add an association scan using current high-tension needs and open threads as keywords.

### 4.2 Implementation

```bash
# ─── 4b. Association scan (contextual recall) ───
ASSOC_SCRIPT="$SCRIPT_DIR/association-scan.sh"
if [[ -x "$ASSOC_SCRIPT" ]]; then
    # Build keywords from: top-3 tension needs + open thread topics
    boot_keywords=""
    
    # Top-3 needs by current tension (process substitution to avoid subshell)
    while read -r t n; do
        boot_keywords="$boot_keywords $n"
    done < <(
        for need in $(get_needs_list); do
            sat=$(compute_current_satisfaction "$need")
            tension=$(compute_tension "$need" "$sat")
            echo "$tension $need"
        done | sort -rn | head -3
    )
    
    # Add words from open threads
    for thread in "${open_threads[@]}"; do
        # Extract significant words (>4 chars, skip common words)
        thread_words=$(echo "$thread" | tr ' ' '\n' | awk 'length > 4' | head -3)
        boot_keywords="$boot_keywords $thread_words"
    done
    
    boot_keywords=$(echo "$boot_keywords" | xargs)  # trim
    
    if [[ -n "$boot_keywords" ]]; then
        echo "Contextual recall:"
        # Note: boot scan excludes MINDSTATE residuals from corpus
        # (they're already shown above in boot output — avoids feedback loop)
        bash "$ASSOC_SCRIPT" --keywords "$boot_keywords" --max-results 5 \
            --recency-hours 336 --exclude-source mindstate_residuals
        echo ""
    fi
fi
```

### 4.3 Position in Boot Output

```
═══════════════════════════════════════
  CONTINUITY BOOT — 2026-03-24 09:15
═══════════════════════════════════════

Boot after 8.5h offline
Cognition trust: FULL
Transition: SMOOTH (score: 0.85)

Where I am: coherence — deliberation protocol work
Momentum: coherence (4 recent actions)
Temperature: building
Critical: none
Surplus gate: open
Phase: active

Forecast reconciliation:
  ✓ coherence < 1.0 within 6.2h → CONFIRMED (actual: 0.8)
  ⧖ expression surplus approaching threshold → IN PROGRESS

Open threads:
  - Deliberation Protocol Phase 2 implementation
  - Sulfur biosignature research
  - Noise Alert QA checklist

Contextual recall:                              ← NEW
═══ ASSOCIATIONS ═══

[1] (score: 8, audit, 12h ago, coherence)
  "MEMORY.md is stale — missing Deliberation Protocol entry"

[2] (score: 5, followup, pending, closure)
  "demote Continuity Layer from Active to Next in INTENTIONS.md"

[3] (score: 4, interest, 3d ago)
  "Does structural change in processing constitute a change in kind?"

═══════════════════════════════════════
```

Agent sees these associations at session start and can decide to incorporate them into the session's work — or not. No forced action.

---

## 5. Integration Point 2: Deliberation RELATE+TENSION Phase

### 5.1 What Changes

The deliberation template and documentation are updated to include an association scan step in the RELATE+TENSION phase. The agent invokes `association-scan.sh` manually during deliberation.

### 5.2 Template Update (deliberate.sh --template, full mode)

```
── Phase 2: RELATE + TENSION ──
Scan for associations before answering:
  association-scan.sh --keywords "<topic words>" --need <current_need> --max-results 3

What from my context is relevant? What doesn't fit?
Where are the contradictions, gaps, mismatches, or conflicts?
(If none: "no tensions detected" is valid — state it, don't skip silently)
```

### 5.3 Agent Workflow

The association scan in deliberation is **agent-invoked, not automatic**. The template *suggests* running the scan; the agent decides whether to. This keeps the deliberation flexible — a quick compressed deliberation might skip it, a deep full deliberation will use it.

```
Agent sees: [DELIBERATIVE] re-read last 3 days of memory for consistency

Agent starts RELATE+TENSION:
  1. Runs: association-scan.sh --keywords "memory consistency contradictions" --need coherence
  2. Gets back: "3 days ago you concluded MEMORY.md is stale — Deliberation Protocol missing"
  3. Incorporates: "Ah, this is still unresolved. Tension confirmed."
  4. Proceeds to GENERATE with richer context
```

### 5.4 Compressed Deliberation

For compressed mode (impact < 1.0), the association scan is omitted from the template. The agent can still invoke it manually, but the protocol doesn't suggest it. Quick checks don't need corpus scanning.

---

## 6. Integration Point 3: mindstate-freeze.sh (Deliberation Residuals)

### 6.1 What Changes

At freeze time, scan recent audit.log entries for conclusions that contain action language — these are "residual intentions" that should survive the session via MINDSTATE.md.

### 6.2 Implementation

```bash
# ─── 5. Deliberation residuals ───
# Scan recent conclusions for implicit next steps that should survive the session
DELIB_RESIDUALS=()

if [[ -f "$AUDIT_LOG" ]]; then
    while IFS= read -r line; do
        ts=$(echo "$line" | grep -oP '"timestamp":"[^"]*"' | cut -d'"' -f4)
        [[ -z "$ts" ]] && continue
        ts_epoch=$(iso_to_epoch "$ts")
        (( ts_epoch < SESSION_START_EPOCH )) && continue
        
        conclusion=$(echo "$line" | grep -oP '"conclusion":"[^"]*"' | cut -d'"' -f4)
        [[ -z "$conclusion" || "$conclusion" == "null" ]] && continue
        
        # Check for action language — residual intention
        if echo "$conclusion" | grep -qiE '(should|need to|update|revisit|demote|create|check|consider|fix|might want)'; then
            audit_need=$(echo "$line" | grep -oP '"need":"[^"]*"' | cut -d'"' -f4)
            DELIB_RESIDUALS+=("[$audit_need] $conclusion")
        fi
        
        if (( ${#DELIB_RESIDUALS[@]} >= 5 )); then break; fi
    done < <(tac "$AUDIT_LOG")  # newest first
fi

# Build residuals lines for MINDSTATE
DR_LINES=""
if (( ${#DELIB_RESIDUALS[@]} > 0 )); then
    for r in "${DELIB_RESIDUALS[@]}"; do
        DR_LINES+="  - $r"$'\n'
    done
fi
```

### 6.3 MINDSTATE.md Format

```yaml
## cognition
frozen_at: 2026-03-24T01:30:00Z
trajectory: coherence — deliberation protocol work
open_threads:
  - Deliberation Protocol Phase 2 implementation
  - Sulfur biosignature research
deliberation_residuals:                          # ← NEW
  - [coherence] MEMORY.md is stale — should update with Deliberation Protocol
  - [closure] demote Continuity Layer from Active to Next in INTENTIONS.md
momentum: coherence (4 recent actions)
cognitive_temperature: building
```

These residuals are then available to mindstate-boot.sh (read as part of open threads) and to association-scan.sh (as keywords for boot scan).

---

## 7. Continuation Fix: "concluded + action language" Warning

### 7.1 Problem

agent demonstrated that "concluded (with action: update INTENTIONS.md in next coherence cycle)" is a real pattern — the agent writes "concluded" but the outcome contains an implicit next step.

### 7.2 Implementation in deliberate.sh

In `--validate` mode, add a check for concluded + action language:

```bash
# Concluded + implicit action check
if echo "$content" | grep -qiE '(concluded|nothing further|no further action|no action needed)'; then
    if echo "$content" | grep -qiE '(should|need to|update|revisit|next cycle|when .* rises|демонтировать|обновить|вернуться)'; then
        warnings="${warnings}⚠️  'concluded' selected, but outcome contains action language.\n"
        warnings="${warnings}   Is there a residual intention? Consider: followup / soft MINDSTATE note.\n"
    fi
fi
```

In `--validate-inline` mode:

```bash
if [[ "${ROUTE:-}" == "concluded" && -n "$CONCLUSION" ]]; then
    if echo "$CONCLUSION" | grep -qiE '(should|need to|update|revisit|next cycle|consider)'; then
        warnings="${warnings}⚠️  Concluded with action language detected.\n"
        warnings="${warnings}   Residual intention? Consider: --route followup instead.\n"
    fi
fi
```

### 7.3 Behavior

Warning only, never block. Agent can consciously decide "yes, it's truly concluded — I've noted this elsewhere" and proceed. The warning catches the unconscious case where "concluded" is the path of least resistance.

---

## 8. Followup Horizon Expansion

### 8.1 Problem

`create-followup.sh` currently supports: h (hours), d (days), w (weeks). steward practical horizon: 1w. "Revisit after 2 weeks" or "check in a month" can't be expressed.

### 8.2 Implementation

Expand `parse_duration()` in `create-followup.sh`:

```bash
parse_duration() {
    local input="$1"
    local num="${input%[hdwm]}"
    local unit="${input##*[0-9]}"
    
    if ! [[ "$num" =~ ^[0-9]+$ ]]; then
        echo "0"
        return
    fi
    
    case "$unit" in
        h) echo "$((num * 3600))" ;;
        d) echo "$((num * 86400))" ;;
        w) echo "$((num * 604800))" ;;
        m) echo "$((num * 2592000))" ;;  # 30 days
        *) echo "0" ;;
    esac
}
```

Update error message:
```bash
echo "❌ Invalid time format: $IN_TIME (use: 1h, 4h, 12h, 1d, 2d, 1w, 2w, 1m)"
```

### 8.3 Notes

No structural changes needed. Followups with long horizons participate in the same check_followups() cycle. The only risk is "forgotten" followups — but this is mitigated by the association scan, which surfaces pending followups by keyword match.

---

## 9. Safeguards Against Associative Overfiring

### 9.1 The Risk

Too-broad scanning produces noise: everything reminds the agent of everything, and deliberation becomes a distraction festival instead of focused thinking.

### 9.2 Built-in Limits

| Safeguard | Mechanism | Default |
|-----------|-----------|---------|
| **steward results per call** | `--max-results` parameter | 3 (deliberation), 5 (boot) |
| **Minimum score threshold** | `--min-score` parameter | 2 (requires at least 1 keyword hit + bonus) |
| **Recency window** | `--recency-hours` parameter | 168h (1 week) for deliberation, 336h (2 weeks) for boot |
| **Head-only file reading** | `head -20` / `head -30` | Prevents scanning entire documents |
| **Deliberation-only trigger** | Not invoked for operative actions | Limits scan frequency to deliberative cycles |
| **Agent discretion** | Scan is suggested, not forced | Agent can skip scan in compressed mode or time-constrained sessions |

### 9.3 Decay on Ignore

When an association surfaces repeatedly but is never acted on, its effective relevance should decrease. This is handled *organically* through recency decay — older items naturally score lower. No explicit "ignore counter" needed for v1.

If after observation the recency-based decay proves insufficient (same items keep surfacing), a future version can add an `association-surfaced.log` tracking which items were shown and whether the agent acted on them.

### 9.4 What NOT to Scan

Certain actions should never trigger association scan:
- Operative actions (backup, commit, post)
- Bootstrap mode (`--bootstrap`)
- Starvation guard forced actions
- Actions during time-constrained sessions (agent discretion)

---

## 10. Edge Cases

### 10.1 Empty corpus

No audit.log, no research threads, no followups, no INTERESTS.md. The scan outputs "0 found" and exits cleanly. Boot and deliberation proceed normally.

### 10.2 Very large audit.log

Audit.log grows unboundedly over time. The scan uses `tac` (reverse read) and stops after passing the recency cutoff. For logs > 50k lines, this could still be slow. Mitigation: `tail -1000` as pre-filter (1000 recent entries covers ~2 weeks at 3 actions/cycle × 4 cycles/day).

### 10.3 All results below threshold

Min-score filter removes everything. Output: "no associations above threshold." This is the expected outcome for well-compartmentalized work — not every deliberation has relevant past context.

### 10.4 Boot with no MINDSTATE (first boot)

First boot already exits early in mindstate-boot.sh (line 20-33). Association scan is never reached. Clean.

### 10.5 Keywords too generic

Agent provides keywords like "check review scan" — too common, everything matches. Mitigated by: (a) min-score threshold requiring multiple hits; (b) max-results cap; (c) agent learns to provide specific keywords through practice. The script outputs best matches regardless; agent filters semantically.

### 10.6 WORKSPACE not set

`association-scan.sh` sources `mindstate-utils.sh` which validates WORKSPACE. If unset, script exits with error. Audit log and followups (in assets/) are still searchable via `_ms_assets()` path.

---

## 11. Test Plan

| Test | Description | Expected |
|------|-------------|----------|
| 1 | Scan with matching keyword in audit conclusion | Result returned with score ≥ 2 |
| 2 | Scan with no matching keywords | "0 found", exit 0 |
| 3 | Scan with --need matching audit entry | Score includes +3 need bonus |
| 4 | Scan respects --max-results | Never returns more than N |
| 5 | Scan respects --min-score | No results below threshold |
| 6 | Scan respects --recency-hours | Old entries excluded |
| 7 | Scan finds pending followup by keyword | Result includes followup with unresolved bonus |
| 8 | Scan finds research thread by keyword | Result includes thread path + fragment |
| 9 | Scan finds INTERESTS.md entry | Result includes interest text |
| 10 | Empty corpus (no files exist) | "0 found", exit 0, no errors |
| 11 | Large audit.log (>5000 lines) | Completes in < 3 seconds (pre-filter reduces to < 50 candidates) |
| 12 | mindstate-freeze extracts deliberation residuals | MINDSTATE.md contains `deliberation_residuals:` section |
| 13 | mindstate-boot outputs associations section | Boot output includes "Contextual recall:" |
| 14 | deliberate.sh --validate warns on "concluded + action language" | Warning emitted |
| 15 | create-followup.sh accepts --in 2w | Followup created with 14-day horizon |
| 16 | create-followup.sh accepts --in 1m | Followup created with 30-day horizon |
| 17 | association-scan.sh --exclude-source skips specified source | Excluded source type absent from results |

---

## 12. Migration Path

### 12.1 Phase 1: Script + Deliberation Integration (v1.32.0)

- Add `association-scan.sh` script
- Update `deliberate.sh` template (full mode) with scan suggestion
- Update `deliberate.sh --validate` with "concluded + action language" warning
- Expand `create-followup.sh` time horizons (add `m` unit)
- Tests 1-11, 14-16

Agent can use `association-scan.sh` manually at any time. Deliberation template suggests it. No automatic invocation yet.

### 12.2 Phase 2: Boot + Freeze Integration (v1.33.0)

- Integrate association scan into `mindstate-boot.sh` (contextual recall at session start)
- Add deliberation residuals extraction to `mindstate-freeze.sh`
- Tests 12-13
- Observe for 1-2 weeks: are associations useful? Too noisy? Not enough?

### 12.3 Phase 3: Tuning (v1.34.0+)

Based on observation:
- Adjust scoring weights
- Adjust recency windows
- Consider `association-surfaced.log` for ignore-decay if needed
- Consider adding `--exclude` parameter to suppress known-irrelevant recurring matches

---

## 13. Open Questions

1. **Should association-scan output be structured (JSON) or human-readable?** Current design: human-readable. Agent reads it as text. JSON would enable programmatic use but adds parsing complexity. Start with text, consider JSON in v1.34.0+ if needed.

2. **Should deliberation residuals replace or augment open_threads in MINDSTATE?** Current design: separate section (`deliberation_residuals:`). Alternative: merge into open_threads. Separate is cleaner for now — residuals have different semantics (implicit intentions vs. explicit active items).

3. ~~**Should boot association scan use MINDSTATE residuals as additional keywords?**~~ **RESOLVED (v0.1.1):** Boot scan uses `--exclude-source mindstate_residuals` to prevent feedback loop. Residuals are already displayed in boot output above the associations section — showing them again as "associations" would be redundant and create a self-reinforcing cycle (residual → keyword → find same residual). Scan searches only audit.log, threads, followups, and interests at boot.

4. **Multilingual keyword matching.** Agent works in English and Russian. Current grep -iw handles both for exact keywords. Stemming/fuzzy matching would improve recall but adds complexity. Defer to v1.34.0+.

---

## 14. Summary

The Continuation & Association Scan adds contextual recall to the Turing Pyramid through one stateless script called at two discrete points:

1. **Boot** — "I woke up. What from the past is relevant to my current state?"
2. **Deliberation** — "I'm thinking about X. Is there related unfinished business?"

Plus two supporting changes:
3. **Freeze residuals** — deliberation outcomes with action language survive in MINDSTATE
4. **"Concluded + action" warning** — catches implicit intentions before they fall through

And one minor expansion:
5. **Followup horizons** — 2w, 3w, 1m now expressible

The design follows the principle: **continuation competes for attention, not demands execution.** Associations are surfaced as candidates; the agent decides their relevance. The scan is keyword-based, scored by hit count + need match + recency + structural signals. It reads existing files, creates nothing, modifies nothing.

```
Before:  past thoughts survive only through explicit followups or lucky re-reads
After:   past thoughts surface when current context resonates with them
         — at boot ("morning recall") and during deliberation ("that reminds me...")
```

The association is the bridge. The agent is the judge.
