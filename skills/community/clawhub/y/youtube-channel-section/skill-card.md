## Description: <br>
Manage YouTube channel sections by helping agents list or delete channel sections with the yutu CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OpenWaygate](https://clawhub.ai/user/OpenWaygate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage YouTube channel sections from an agent workflow, including listing sections for inspection and deleting selected sections by ID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OAuth client secrets and cached tokens can expose YouTube account access if shared or committed. <br>
Mitigation: Keep client_secret.json and youtube.token.json private, store them outside source control, and restrict access to environments that need the skill. <br>
Risk: Deleting channel sections by the wrong ID can remove unintended YouTube channel organization. <br>
Mitigation: List channel sections first and confirm the exact IDs before running delete commands. <br>
Risk: The skill depends on the third-party yutu CLI for YouTube operations. <br>
Mitigation: Install it only from trusted sources and use it only when you intend to manage YouTube channel sections. <br>


## Reference(s): <br>
- [Channel Section Delete](references/channelSection-delete.md) <br>
- [Channel Section List](references/channelSection-list.md) <br>
- [Yutu Setup Guide](references/setup.md) <br>
- [yutu project homepage](https://github.com/eat-pray-ai/yutu) <br>
- [ClawHub skill page](https://clawhub.ai/OpenWaygate/youtube-channel-section) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require the yutu CLI plus OAuth credential and token configuration.] <br>

## Skill Version(s): <br>
0.10.7-dev (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
