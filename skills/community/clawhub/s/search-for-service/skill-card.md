## Description:

Search and browse the x402 bazaar marketplace for paid API services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xrag](https://clawhub.ai/user/0xrag)

### License/Terms of Use:


## Use Case:

Developers, agents, and external users use this skill to find paid API services, browse available x402 bazaar resources, and inspect endpoint payment requirements before deciding whether another skill should call a service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned npm package and can inspect arbitrary endpoint URLs, including with mutating HTTP methods.

Mitigation: Review before installing, pin the npm package to a reviewed version, and restrict endpoint inspection to trusted public HTTPS URLs under explicit user control.

## Reference(s):

- [Search For Service on ClawHub](https://clawhub.ai/0xrag/skills/search-for-service)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search, list, and details commands may use locally cached marketplace data and can emit JSON when requested.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
