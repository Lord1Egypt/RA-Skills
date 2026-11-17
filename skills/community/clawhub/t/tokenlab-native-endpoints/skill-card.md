## Description:

Guides agents in choosing TokenLab native endpoints and preserving provider-specific request semantics when OpenAI-compatible chat is not the right fit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hedging8563](https://clawhub.ai/user/hedging8563)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to select TokenLab's native API routes, prepare compatible requests, and recover from endpoint or model-contract errors without changing request semantics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example calls can send prompts, request content, and API credentials to TokenLab.

Mitigation: Confirm TokenLab is an intended recipient and review content and credentials before invoking examples.

Risk: Installing from a floating package or repository reference can introduce unreviewed changes.

Mitigation: Install from a reviewed commit or pinned package version.

Risk: Treating a System One decision result as permission to act can trigger unintended actions.

Mitigation: Keep decision outputs as typed answers and require separate authorization before acting.

## Reference(s):

- [TokenLab Native Endpoints on ClawHub](https://clawhub.ai/hedging8563/skills/tokenlab-native-endpoints)
- [TokenLab model catalog](https://api.tokenlab.sh/v1/models)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands]

**Output Format:** [Markdown with a runnable code or cURL block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes an endpoint rationale and a model-contract or catalog recovery path.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
