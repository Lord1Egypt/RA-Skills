## Description:

Run real user interviews via Usercall when qualitative feedback is needed for onboarding drop-off, feature confusion, pricing clarity, prototype testing, and similar research topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junetic](https://clawhub.ai/user/junetic)

### License/Terms of Use:

MIT-0

## Use Case:

External users, product teams, founders, researchers, and developers use this skill to create Usercall interview studies, share participant links, and retrieve summarized interview themes and quotes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to echo USERCALL_API_KEY, which can expose a live credential in terminal logs or transcripts.

Mitigation: Use a presence-only check for the environment variable and never print the key value.

Risk: The skill recommends storing the API key permanently in shell startup files as plaintext.

Mitigation: Prefer a credential manager or session-only environment variable, and rotate any key that may have been exposed.

Risk: Study context, prototypes, media URLs, and interview results are transmitted to the third-party Usercall service.

Mitigation: Avoid sending confidential product plans, personal data, or unreleased material unless that third-party transmission is intended and approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/junetic/skills/user-interview)
- [Junetic publisher profile](https://clawhub.ai/user/junetic)
- [Usercall app](https://app.usercall.co)
- [Usercall agent studies API endpoint](https://app.usercall.co/api/v1/agent/studies)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Configuration, Markdown, Guidance]

**Output Format:** [Markdown with bash and JSON code blocks plus concise study-result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires USERCALL_API_KEY and sends study context, optional media URLs, and interview-management requests to Usercall.]

## Skill Version(s):

1.0.2 (source: server release evidence, created 2026-03-17T01:25:20Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
