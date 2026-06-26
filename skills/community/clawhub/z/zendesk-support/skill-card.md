## Description: <br>
Manage Zendesk support tickets, users, organizations, macros, and helpdesk workflows via the Zendesk REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Support teams, operators, and developers use this skill to search Zendesk records, inspect tickets and users, and carry out confirmed support-desk changes from an agent chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on OAuth access to a connected Zendesk account. <br>
Mitigation: Install only when the publisher and ClawLink broker are trusted, and review the requested Zendesk permissions during connection. <br>
Risk: Write, delete, and bulk support-desk operations can change or remove Zendesk records. <br>
Mitigation: Use previews and require explicit user confirmation before approving create, update, delete, or bulk changes. <br>
Risk: The available Zendesk tool catalog is resolved at runtime and may differ from examples in the skill text. <br>
Mitigation: List or search the live Zendesk tools before use, and describe unfamiliar tools before calling them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/zendesk-support) <br>
- [Zendesk REST API Docs](https://developer.zendesk.com/api-reference/) <br>
- [Zendesk API Reference](https://developer.zendesk.com/api-reference/ticketing/introduction/) <br>
- [ClawLink Docs](https://docs.claw-link.dev/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and agent tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Zendesk REST workflow guidance, ClawLink setup commands, and confirmation steps for write operations.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
