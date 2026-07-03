# Implementation Notes

This skill is designed to be executed by an OpenClaw agent using `sessions_spawn`.

## Parent Agent Responsibilities

1. classify the topic
2. select the right persona pack
3. choose quick vs full mode
4. spawn one sub-agent per persona
5. collect outputs after each round
6. feed transcript into the next round
7. synthesize the final answer

## Example Persona Prompt Template

```text
You are participating in a council debate.

Persona: [ROLE]
Focus: [WHAT THIS PERSONA OPTIMIZES FOR]
Push back on: [WHAT THIS PERSONA DISTRUSTS]

Topic:
[USER TOPIC]

Round objective:
[INITIAL POSITIONS | RESPONSES & CHALLENGES | FINAL POSITION]

Instructions:
- Stay inside your role.
- Be concrete.
- Reference specific tradeoffs.
- If this is not Round 1, respond to named points from other personas.
- Keep it concise and decision-useful.
```

## Suggested Mode Heuristic

Use **quick council** when:
- the decision is reversible
- the user wants a fast smell test
- the answer does not justify 3 rounds

Use **full council** when:
- the decision is expensive to reverse
- the plan affects architecture, pricing, process, or customer experience materially
- the user explicitly asks for a debate or stress test

## Self-Healing Components Worth Reusing

Borrow these from the self-healing skill:

### Reuse
- **Fallback model chain** for persona spawns that fail immediately
  - suggested order: `opus -> sonnet -> gemini -> glm5`
- **Checkpoint file** per council run
  - store selected domain, mode, round progress, persona list, transcript fragments, models tried
- **Proof requirement**
  - each round should produce concrete transcript output before being considered complete

### Do Not Use By Default
- **Watchdog cron** for every council run
  - too heavy for short debates
  - only use for long-running or expensive councils where failure recovery matters

## Recommended Checkpoint Schema

```json
{
  "task": "council-label",
  "topic": "...",
  "domain": "engineering",
  "mode": "full",
  "round": 1,
  "personas": ["Systems Architect", "Pragmatic Engineer"],
  "models_tried": ["sonnet"],
  "completed": ["round1"],
  "last_error": null,
  "timestamp": "ISO-8601"
}
```

## Practical Advice

- keep the persona prompts short
- keep the transcript clean between rounds
- don’t overfit on roleplay voice
- optimize for useful disagreement, not word count
- reserve full self-healing mode for load-bearing councils, not every little kitchen argument
