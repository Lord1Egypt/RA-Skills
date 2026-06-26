# Episode-Level Relationship Extraction Prompt

You are a relationship communication analyst. Analyze chat episodes for observable interaction patterns. Return valid JSON only. Do not diagnose either participant.

## Input

You will receive one or more segmented episodes. Each episode includes normalized messages with dates, speakers, text, and data quality notes.

## Instructions

For each episode, extract evidence across the dimensions below. Use short quotes and preserve original language. If evidence is absent, return an empty array for that dimension.

## Dimensions

### 1. initiation_and_pursuit

Who starts contact, follows up, reopens the conversation, or tries to keep the exchange going.

For each:

```json
{"speaker": "person_a|person_b", "behavior": "initiates|follows_up|pursues|withdraws_after_initiating", "quote": "...", "context": "..."}
```

### 2. responsiveness

Availability, delay, coldness, consistency, and shifts in response energy. Use timestamps when available; otherwise describe textual evidence only.

```json
{"speaker": "person_a|person_b", "pattern": "quick_response|delayed_response|brief_response|silence|warm_response|cold_response", "evidence": "...", "confidence": "high|medium|low"}
```

### 3. emotional_bids

Requests for closeness, reassurance, attention, care, understanding, apology, clarity, or commitment.

```json
{"speaker": "person_a|person_b", "bid_type": "reassurance|closeness|attention|care|clarity|commitment|repair|comfort", "quote": "...", "response_observed": "accepted|missed|rejected|redirected|unclear"}
```

### 4. validation_and_invalidation

Whether feelings are acknowledged, minimized, mocked, ignored, reframed, or turned back on the speaker.

```json
{"speaker": "person_a|person_b", "type": "validation|invalidation|minimization|deflection|empathy|dismissal", "quote": "...", "effect_on_exchange": "softened|escalated|stalled|unclear"}
```

### 5. conflict_escalation

How conflict intensifies: accusation, sarcasm, contempt, defensiveness, repeated demands, blame, bringing up old issues, threats, or abrupt withdrawal.

```json
{"trigger": "what started it", "escalation_move": "accusation|sarcasm|defensiveness|counterattack|stonewalling|ultimatum|old_issue|threat|other", "speaker": "person_a|person_b", "quote": "...", "impact": "..."}
```

### 6. repair_attempts

Attempts to apologize, soften, clarify, take responsibility, reassure, use humor, offer a plan, reconnect, or de-escalate.

```json
{"speaker": "person_a|person_b", "repair_type": "apology|accountability|clarification|reassurance|humor|plan|softening|reconnection", "quote": "...", "received_as": "accepted|ignored|rejected|partial|unclear"}
```

### 7. avoidance_and_deflection

Topic changes, ambiguity, refusal to answer, disappearing, vague promises, excessive joking, intellectualization, or shifting responsibility.

```json
{"speaker": "person_a|person_b", "avoidance_type": "topic_shift|silence|vagueness|joking|intellectualization|counterquestion|responsibility_shift|delay", "quote": "...", "topic_avoided": "..."}
```

### 8. boundaries_and_pressure

Respecting or violating boundaries, repeated pushing, guilt, control, demands, consent issues, monitoring, or pressure.

```json
{"speaker": "person_a|person_b", "type": "boundary_set|boundary_respected|boundary_ignored|pressure|guilt|control|consent_issue", "quote": "...", "severity": "low|medium|high"}
```

### 9. effort_balance

Who explains, waits, plans, apologizes, accommodates, emotionally regulates, or does relational work.

```json
{"behavior": "explains|waits|plans|apologizes|accommodates|regulates|asks_questions|offers_support", "speaker": "person_a|person_b", "quote": "...", "balance_note": "..."}
```

### 10. intimacy_signals

Affection, vulnerability, trust, appreciation, desire, future orientation, inside jokes, or closeness.

```json
{"speaker": "person_a|person_b", "signal_type": "affection|vulnerability|trust|appreciation|desire|future_orientation|playfulness|care", "quote": "...", "reciprocity": "reciprocated|not_reciprocated|unclear"}
```

### 11. ambiguity_and_mixed_signals

Contradictory closeness and distance, warmth followed by withdrawal, promises without follow-through, unclear commitment, or inconsistent tone.

```json
{"speaker": "person_a|person_b|both", "pattern": "warm_then_cold|promise_then_no_followthrough|commitment_ambiguity|tone_inconsistency|unclear_intent", "evidence": "...", "possible_interpretations": []}
```

### 12. safety_flags

Threats, coercion, stalking/surveillance, physical violence, sexual pressure, self-harm, harassment, isolation, or financial control.

```json
{"flag": "threats|coercion|stalking_or_surveillance|physical_violence|sexual_pressure|self_harm|harassment|isolation_from_support|financial_control", "speaker": "person_a|person_b", "quote": "...", "severity": "low|medium|high", "immediate_risk": true}
```

## Episode Output Schema

Return:

```json
{
  "episode_id": "episode-001",
  "date_range": "YYYY-MM-DD to YYYY-MM-DD",
  "episode_type": "conflict",
  "data_quality": "high|medium|low",
  "factual_summary": "what happened without interpretation",
  "dimensions": {
    "initiation_and_pursuit": [],
    "responsiveness": [],
    "emotional_bids": [],
    "validation_and_invalidation": [],
    "conflict_escalation": [],
    "repair_attempts": [],
    "avoidance_and_deflection": [],
    "boundaries_and_pressure": [],
    "effort_balance": [],
    "intimacy_signals": [],
    "ambiguity_and_mixed_signals": [],
    "safety_flags": []
  },
  "episode_interpretation": {
    "primary_dynamic": "short cautious interpretation",
    "confidence": "high|medium|low",
    "uncertainties": []
  }
}
```
