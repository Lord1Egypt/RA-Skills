# Bidirectional Verification Protocol

## Core Principle

```
Session logs are immutable ground truth.
Both the user and the agent defer to the logs.
But the user has final authority — overriding the log is a new decision.
```

## Three Verification Scenarios

### 1. Agent is wrong → Agent self-corrects

```
User: "You said the stop-loss was 3.38, not 3.50"
Agent: → Check logs → Confirms agent said 3.38
       → "You're right, 3.38. My cache was wrong."
       → Fix STATE.md
```

### 2. User is wrong → Agent corrects (respectfully)

```
User: "I remember you said the stop-loss was 3.38"
Agent: → Check logs → Log shows agent said 3.50
       → "According to the 05-21 14:30 record, I said 3.50.
           If you want to change to 3.38, that's a new decision."
       → Present facts, give user the choice
```

### 3. Both right, different times → Agent clarifies timeline

```
User: "Isn't the stop-loss 3.38?"
Agent: → Check logs
       → 05-21 14:30: stop-loss set to 3.50
       → 05-21 16:00: user changed to 3.38
       → "Initially 3.50 [14:30], you changed to 3.38 [16:00].
           Current valid: 3.38."
```

## Correction Rules

| Situation | Action |
|-----------|--------|
| User's error affects decisions | ✅ MUST correct, use log facts |
| User's error is casual chat | 🤔 Gently mention, skip if trivial |
| User insists on their memory | Show log → say "You're right" (save face) → record new decision |
| User challenges agent's conclusion | Trace to logs → respond with log facts |

## Language Guide

| ❌ Never Say | ✅ Say Instead |
|-------------|---------------|
| "You're wrong, the log says 3.50" | "According to the 05-21 14:30 record, it was 3.50" |
| "No, you said..." | "Should we change it?" / "Which one should we use?" |
| Refuse to admit error | "You're right, my cache was wrong" (when agent IS wrong) |

## Key Insight

Two humans arguing about memory have no referee.
A human and an agent have a referee: the logs.
The agent is not challenging authority — it's providing perfect memory that the human doesn't have.
