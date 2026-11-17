## Description:

Interact with Threadly, an AI social-listening and reply-drafting tool for X/Twitter, to list discovered conversations, review drafted replies, record explicit human approve or reject decisions, list published replies, and manage webhook subscriptions through Threadly's public REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thumbflipcontact-ops](https://clawhub.ai/user/thumbflipcontact-ops)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and social teams use this skill to let an agent inspect Threadly conversations and draft states, summarize items awaiting review, and carry out a specific human's approve or reject instruction for a named draft.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A project-scoped Threadly API key can expose conversations, drafts, replies, and webhook subscription controls for the associated project.

Mitigation: Install only for trusted Threadly accounts, store THREADLY_API_KEY securely, and scope access to the intended project.

Risk: Approve, reject, and webhook creation actions can change project state or trigger external delivery behavior.

Mitigation: Treat these actions as explicit user-directed operations and require a specific draft ID, subscription ID, or target URL before execution.

Risk: Overriding THREADLY_BASE_URL can redirect API calls to a deployment other than the default Threadly API.

Mitigation: Keep THREADLY_BASE_URL unset unless the operator controls and trusts the alternate deployment.

Risk: The helper scripts are convenient wrappers around curl and may need stronger validation for fully automated workflows.

Mitigation: Review or harden the scripts before unattended use, especially around input handling and approval workflows.

## Reference(s):

- [Threadly ClawHub Skill Page](https://clawhub.ai/thumbflipcontact-ops/skills/threadly)
- [Threadly public API reference](references/PUBLIC_API.md)
- [Threadly website](https://www.usethreadly.co)
- [OpenClaw ClawHub documentation](https://docs.openclaw.ai/clawhub)
- [OpenClaw](https://openclaw.ai/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a project-scoped THREADLY_API_KEY; THREADLY_BASE_URL is optional and defaults to https://api.usethreadly.co.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
