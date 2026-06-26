## Description: <br>
Give your AI agent persistent identity (WebID) and personal data storage (Pod) using the Solid Protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[masterworrall](https://clawhub.ai/user/masterworrall) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and agent builders use this skill to provision a Solid WebID and Pod, retrieve short-lived Bearer tokens, and store, read, delete, or share agent data through standard Solid HTTP operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted agent names can write or delete outside the stated credential folder. <br>
Mitigation: Review before installing, use simple safe agent names until path validation is fixed, and run the skill only where the ~/.interition credential area is appropriate for the agent. <br>
Risk: Provisioned accounts use weak generated passwords. <br>
Mitigation: Use only trusted Solid servers, prefer servers you control, and avoid storing sensitive long-term data unless the Pod, ACL settings, and account lifecycle are acceptable. <br>
Risk: Bearer tokens and server credentials grant access to Pod data. <br>
Mitigation: Keep INTERITION_PASSPHRASE strong and private, treat printed Bearer tokens as secrets, and avoid copying command output into logs or shared transcripts. <br>


## Reference(s): <br>
- [Solid HTTP Reference](references/solid-http-reference.md) <br>
- [Solid Protocol Primer](references/solid-primer.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Security Manifest](SECURITY.md) <br>
- [Source Repository](https://github.com/masterworrall/agent-interition) <br>
- [Solid Project](https://solidproject.org) <br>
- [Solid Protocol Specification](https://solidproject.org/TR/protocol) <br>
- [Community Solid Server](https://github.com/CommunitySolidServer/CommunitySolidServer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Management commands run Node.js CLI wrappers and standard Solid operations use curl with Bearer tokens.] <br>

## Skill Version(s): <br>
0.3.9 (source: SKILL.md frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
