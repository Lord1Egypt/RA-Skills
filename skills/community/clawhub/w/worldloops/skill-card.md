## Description:

Agent Execution Guard by WorldLoops turns scattered work signals into governed open loops while preserving externalWrite:false.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swit001](https://clawhub.ai/user/swit001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to turn already-read Gmail, Calendar, Slack, GitHub, and workflow signals into governed open loops, proposals, approvals, local transitions, and receipts. It helps keep agent actions inside an auditable externalWrite:false boundary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private local handoff content may be sent to a hosted API by default brief or guard commands.

Mitigation: Review handoff files before use, treat these commands as remote-processing until verified, and avoid sending customer, legal, business, or other sensitive data without authorization.

Risk: WORLDLOOPS_API_BASE_URL can redirect processing to an untrusted endpoint.

Mitigation: Leave the default endpoint in place or verify the endpoint and bearer-token handling before setting a custom API base URL.

Risk: The Telegram test command may expose local brief data through an unauthenticated demo bot.

Mitigation: Use isolated demo data for telegram:test, or add chat allowlisting and deployment isolation before using real handoff data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/swit001/skills/worldloops)
- [WorldLoops homepage](https://github.com/swit001/worldloops)
- [README](artifact/README.md)
- [Adapter Guide](artifact/ADAPTER_GUIDE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and CLI text with JSON configuration and receipt files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and npm; accepts local JSON handoff payloads; preserves externalWrite:false.]

## Skill Version(s):

1.13.0 (source: server release evidence and package.json; artifact SKILL.md frontmatter is 1.12.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
