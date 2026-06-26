## Description: <br>
Provides LinkedIn automation through Unipile's Node.js SDK for profile and post retrieval, messaging, invitations, posts, comments, and reactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mohit21GoJs](https://clawhub.ai/user/Mohit21GoJs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to connect to a Unipile-backed LinkedIn account, retrieve LinkedIn profiles, posts, chats, and connections, and perform reviewed write actions such as sending messages, invitations, comments, reactions, or posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate with full LinkedIn account read/write authority, including sending messages, invitations, posts, comments, and reactions. <br>
Mitigation: Set UNIPILE_PERMISSIONS=read for normal use and enable write access only for a specific reviewed action. <br>
Risk: A Unipile access token can perform actions on behalf of the connected LinkedIn account. <br>
Mitigation: Keep UNIPILE_ACCESS_TOKEN in environment variables or a secrets manager, and avoid storing it in shared or version-controlled files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Mohit21GoJs/unipile-linkedin-sdk) <br>
- [Unipile API documentation](https://developer.unipile.com/docs/list-provider-features) <br>
- [Unipile dashboard](https://dashboard.unipile.com) <br>
- [Unipile Node.js SDK repository](https://github.com/unipile/unipile-node-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with JavaScript and shell examples; the bundled CLI emits JSON for read operations and status text for write operations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires UNIPILE_DSN and UNIPILE_ACCESS_TOKEN; UNIPILE_PERMISSIONS controls read and write command access.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
