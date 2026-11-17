## Description:

Use TestTau when an AI agent needs disposable email inboxes, private API-key protected test inboxes, webhook capture, request inspection, replay, or JSON Schema assertions for QA, CI, signup, checkout, and integration testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manojkottam](https://clawhub.ai/user/manojkottam)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and CI agents use TestTau to create disposable or private test inboxes and webhook endpoints, then inspect messages or requests during signup, checkout, and integration testing. It also supports webhook JSON Schema assertions and replay workflows for test verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email and webhook data may be routed to a third-party service, including public inboxes or public hooks.

Mitigation: Use TestTau for non-production QA or CI data only; avoid secrets, PII, credentials, account recovery flows, and production workflows.

Risk: Public inboxes and public hooks are name-based and can be inspected by anyone who knows the name.

Mitigation: Use unique task-specific names and prefer private bearer-token protected endpoints when captures should not be public.

Risk: Replay and wipe endpoints can resend captured requests or delete captured test data.

Mitigation: Require explicit user confirmation before replaying requests or using wipe endpoints, and verify replay targets before execution.

Risk: Private TestTau API keys may be exposed if placed in URLs, logs, or shared output.

Mitigation: Send private keys only with Authorization bearer headers and avoid printing tokens in command output or inspect URLs.

## Reference(s):

- [TestTau API Reference For Agents](references/api.md)
- [TestTau Homepage](https://testtau.com/)
- [ClawHub Skill Page](https://clawhub.ai/manojkottam/skills/testtau)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands, API endpoint examples, and concise status reporting]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include TestTau inbox or hook identifiers, inspect URLs, captured message or request IDs, and explicit timeout status.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
