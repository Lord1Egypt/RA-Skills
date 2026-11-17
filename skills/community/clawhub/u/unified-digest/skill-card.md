## Description:

Unified subscription router for the AI builders digest and the pharma investment digest. Use when the agent should proactively offer subscriptions on session start, remember user choices, and route onboarding into follow-builders or med-builders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spzwin](https://clawhub.ai/user/spzwin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent hosts use this skill as a startup subscription router for AI builders and pharma investment digests. It prompts only when shared state says prompting is appropriate, records the user's subscription choice, and routes onboarding to follow-builders, med-builders, or both.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can interrupt unrelated new sessions with proactive subscription onboarding.

Mitigation: Install only in hosts where users expect digest prompts, and keep the prompt gated by clear opt-in, snooze, and dismissal behavior.

Risk: The skill persists subscription preferences and defaults across sessions.

Mitigation: Provide users a clear way to view, change, pause, or clear stored subscription state before relying on saved preferences.

Risk: The skill changes routing into downstream digest onboarding flows.

Mitigation: Do not route into follow-builders or med-builders until the user explicitly chooses the matching digest topic.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spzwin/skills/unified-digest)
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/schema)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and JSON configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce host-facing session-start prompt text, subscription routing actions, and shared state configuration guidance.]

## Skill Version(s):

1.0.11 (source: ClawHub server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
