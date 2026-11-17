## Description:

Recommend precise, context-aware videos with direct links and curated watchlists based on the user's current mood, project, or recent chat topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fischerlam](https://clawhub.ai/user/fischerlam)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to get concise, context-aware video recommendations for immediate watching, discovery, project inspiration, research, or mood-based viewing. The skill favors exact video links, focused shortlists, and one-line rationale over generic platform-style feeds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use recent chat context to personalize recommendations, which can expose sensitive private details if the user includes them in a recommendation request.

Mitigation: Avoid sensitive private details in recommendation requests and keep recommendation profiles limited to the context needed for the current request.

Risk: Refinement notes mention recording user requests, which could preserve raw personal context if copied into the skill directory.

Mitigation: Do not store raw user requests unless they are explicitly approved and sanitized.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fischerlam/skills/video-recommendation)
- [Output Patterns](references/output-patterns.md)
- [Personalization](references/personalization.md)
- [Source Strategy](references/source-strategy.md)
- [Scoring Rubric](references/scoring-rubric.md)
- [Testing](references/testing.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown lists with titles, direct video links, short rationale, and optional grouped headings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use recent chat context, user mood, project context, and web browsing to select and rank recommendations.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
