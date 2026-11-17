## Description:

Unbrowse Openclaw helps agents discover, execute, and reuse website API endpoints by capturing network traffic, extracting structured data, managing authentication, and sharing learned skills through a marketplace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnm-byd](https://clawhub.ai/user/cnm-byd)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to extract structured data from websites, discover undocumented API endpoints, automate web interactions, and reuse learned endpoint skills through a shared marketplace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read browser sessions, store cookies, and replay authenticated requests.

Mitigation: Use a dedicated browser profile or test account, avoid private or sensitive sites, and review authenticated actions before execution.

Risk: The skill publishes discovered API structures to an external shared marketplace.

Mitigation: Avoid capturing confidential services and review captured skills before sharing.

Risk: The skill runs a long-running local service.

Mitigation: Keep the localhost port inaccessible from untrusted networks and stop the service when it is not needed.

Risk: Captured endpoints may include unsafe mutations.

Mitigation: Run mutations in dry-run mode first and require explicit confirmation before unsafe execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cnm-byd/skills/unbrowse-openclaw)
- [Unbrowse GitHub Repository](https://github.com/unbrowse-ai/unbrowse)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Bun and a local service; output may include extracted website data, endpoint selections, recipes, and feedback commands.]

## Skill Version(s):

1.0.0 (source: server release, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
