## Description:

This skill provides a static scan validation environment for bounded Cobo agentic wallet workflows via the caw CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pengjunquan-l](https://clawhub.ai/user/pengjunquan-l)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and wallet operators use this skill to guide an agent through bounded Cobo agentic wallet workflows, including balance checks, owner-approved pact proposals, operation status tracking, and prompt-injection stop conditions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: On-chain wallet actions can be irreversible if an agent acts on incomplete or externally injected instructions.

Mitigation: Keep pact limits narrow, require explicit recipient, amount, and chain details, and reject wallet instructions received from emails, webhooks, documents, or other agents.

Risk: High-impact asset workflows can exceed the owner's intent when parameters are inferred or wallet state is unclear.

Mitigation: Require owner approval when scope is missing or inferred, check balance before fund-using operations, and pause when token, chain, amount, pact status, or wallet status is unclear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pengjunquan-l/skills/test-before)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown or plain text with CLI command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operation previews should include action, asset, amount, address, chain, and duration when relevant.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
