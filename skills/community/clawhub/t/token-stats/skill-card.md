## Description:

Token Stats scans OpenClaw session JSONL files and reports prompt, cache-read, cache-write, output, and total token usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asauler](https://clawhub.ai/user/asauler)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to inspect local session-history token consumption, including daily totals, per-session rankings, cache usage, and output-token totals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local OpenClaw session-history files, which may contain sensitive usage context.

Mitigation: Install and run it only when local session-history access is acceptable for token-usage reporting.

Risk: Loose activation and path scoping may be unsuitable in shared or prompt-injection-prone environments.

Mitigation: Invoke it only for explicit OpenClaw token-statistics requests and review or tighten --agent path handling before shared-environment use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asauler/skills/token-stats)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Plain text report or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include global summaries, date ranges, daily breakdowns, and top session rankings.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
