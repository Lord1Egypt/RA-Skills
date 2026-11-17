## Description:

Conversational Compounding Engine that models bot messages as investments compounding trust, micro-commitments, and conversion momentum without external APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcools1977](https://clawhub.ai/user/jcools1977)

### License/Terms of Use:

MIT

## Use Case:

Developers and bot builders use Yield to analyze conversation signals, maintain lightweight per-conversation state, and guide bot response strategy for engagement, support, onboarding, or conversion workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can profile users and steer bot replies toward conversion outcomes without user awareness.

Mitigation: Use only where behavioral profiling and conversion optimization are appropriate, disclose the behavior to users, and avoid sensitive domains.

Risk: Prompt-only use can hide steering instructions from the person interacting with the bot.

Mitigation: Disable hidden system-prompt steering and require review of response policies before deployment.

Risk: Conversation state or exports may include user message history.

Mitigation: Minimize stored or exported conversation text and enforce retention, rate-limit, and host policy boundaries.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jcools1977/skills/yield)

## Skill Output:

**Output Type(s):** [guidance, code, configuration]

**Output Format:** [JavaScript modules, integration examples, and plain-language strategy directives]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with no declared runtime dependencies or external API calls.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
