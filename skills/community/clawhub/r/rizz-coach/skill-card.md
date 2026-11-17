## Description:

AI texting and flirting coach that grades messages, improves texts, generates replies, simulates conversations, and creates shareable results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vajih](https://clawhub.ai/user/vajih)

### License/Terms of Use:

MIT-0

## Use Case:

External users use Rizz Coach to evaluate draft dating or social messages, rewrite them in different confidence levels, generate reply options, practice simulated conversations, and create shareable text result cards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may paste private chats, names, contact details, or sensitive relationship context for analysis or rewriting.

Mitigation: Show clear privacy and third-party processing notices before use, and advise users to avoid entering unnecessary personal data.

Risk: Conversation simulation accepts caller-supplied session state and conversation history.

Mitigation: Validate simulator state shape and bounds, limit retained history size, and reject malformed or oversized state before processing.

Risk: Generated dating advice could include unsafe or policy-violating text if model output filtering misses a case.

Mitigation: Keep input and output safety checks enabled for every mode and review generated text fields before broad deployment.

Risk: Dependency versions may drift because package.json uses range specifiers.

Mitigation: Pin or routinely update dependencies and review the lockfile before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vajih/skills/rizz-coach)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Structured JSON results with display-ready Markdown or plain text blocks and ASCII share cards.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes message scores, rewrite tiers, reply options with risk labels, simulator state updates, coaching feedback, and safety-blocked responses when applicable.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
