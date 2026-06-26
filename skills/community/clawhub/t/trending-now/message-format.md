# Message Format - Trending Now

## Alert Message Template

Use this structure for each alert:

```text
[Topic] [Signal Level: High|Medium]
What changed: <one sentence>
Why it matters: <one sentence tied to user goal>
Confidence: <high|medium|low> (based on <brief reason>)
Risk: <main uncertainty or contradiction>
Action: <single concrete next step>
Sources: <2-4 short links or source labels>
```

## No-Op Contract

If nothing is actionable, return exactly:

```text
HEARTBEAT_OK
```

No extra text.

## Escalation Message Template

```text
[Escalation] [Topic]
Change acceleration detected compared with last cycle.
Reason: <threshold crossed or major event>
Immediate action: <what to do now>
```

## Writing Rules

- Keep alerts under 120 words when possible.
- Lead with what changed, not background context.
- Include uncertainty explicitly.
- Avoid sensational language.
- Always provide one action, even if action is "wait and monitor".

## Example

```text
[AI coding assistants] [Signal Level: High]
What changed: X and Reddit both showed a surge in reports about smaller context windows causing production errors in long sessions.
Why it matters: This can reduce trust and increase debugging time for your team this week.
Confidence: medium (cross-source confirmation, limited publisher coverage)
Risk: Surge may be concentrated in enterprise workflows only.
Action: Audit your top three long-context tasks and add fallback prompts today.
Sources: X thread cluster, Reddit r/LocalLLaMA discussion, Google Trends snapshot
```
