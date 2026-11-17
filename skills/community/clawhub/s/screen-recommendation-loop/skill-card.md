## Description:

Runs a low-friction movie and anime recommendation loop that recommends one title at a time, collects minimal feedback, and adapts future picks from preference signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gloryxia](https://clawhub.ai/user/gloryxia)

### License/Terms of Use:

MIT-0

## Use Case:

External users and recommendation-focused agents use this skill to run an ongoing movie and anime recommendation cycle with short feedback, automatic follow-up timing, and lightweight preference updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recommendation state may include watch history, preference signals, and follow-up timing.

Mitigation: Keep the state local or in a trusted store, and avoid adding account IDs, chat IDs, tokens, private schedules, or other direct identifiers.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gloryxia/skills/screen-recommendation-loop)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance with concise recommendation messages, feedback prompts, and minimal JSON or SQLite record schemas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains per-title state, preference signals, and content-type-based follow-up timing.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
