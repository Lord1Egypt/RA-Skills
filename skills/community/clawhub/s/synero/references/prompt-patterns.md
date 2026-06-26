# Prompt Patterns

Use these patterns when asking Synero's council for higher-signal answers. Synero works best on questions with real uncertainty, tradeoffs, or competing interpretations.

## Product decision

```text
What are the 3 strongest arguments for and against shipping <feature> in the next 30 days?
Assume a startup context with limited engineering capacity.
End with a concrete recommendation, the main risk, and what evidence would change your mind.
```

## Strategy debate

```text
Debate this position from multiple angles: <claim>.
I want disagreement, hidden assumptions, second-order effects, and a final synthesis.
Keep it practical, not academic.
```

## Leadership or hiring

```text
I'm deciding between <option A> and <option B>.
Evaluate tradeoffs across speed, quality, org complexity, cost, and execution risk.
Then give me the best recommendation for the next 90 days.
```

## Technical architecture

```text
Evaluate this technical plan: <plan>.
Identify likely bottlenecks, hidden migration costs, failure modes, and what I should prototype first.
Return a clear go / no-go recommendation.
```

## Research or synthesis

```text
I need a reliable synthesis on <topic>.
Compare the strongest explanations or schools of thought, call out uncertainty, and end with the most decision-useful takeaway.
```

## Positioning or messaging

```text
I need a point of view on <topic>.
Give me the strongest contrarian angle, the strongest mainstream angle, and a synthesis that would resonate with operators.
```

## Best practices

- Ask for a recommendation, not just exploration.
- Add operating constraints such as timeline, team size, budget, risk tolerance, or target audience.
- Ask for assumptions, failure modes, and disconfirming evidence when the decision matters.
- Use `--thread-id` when continuing the same topic across multiple rounds.
- Use `--quiet` when another tool or script needs clean final text only.
- Use `--raw` when debugging streaming behavior or inspecting advisor outputs.
