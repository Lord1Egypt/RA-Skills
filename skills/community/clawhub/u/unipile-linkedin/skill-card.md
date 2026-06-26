## Description: <br>
Interact with LinkedIn via Unipile API - send messages, view profiles, manage connections, create posts, react to content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sudhanshu746](https://clawhub.ai/user/sudhanshu746) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate a Unipile-connected LinkedIn account for messaging, profile lookup, connection management, posting, commenting, and reactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send LinkedIn messages, invitations, posts, comments, reactions, and profile views that notify others. <br>
Mitigation: Require explicit human review and approval before any outward-facing LinkedIn action is executed. <br>
Risk: The skill depends on a Unipile access token that can operate a connected LinkedIn account. <br>
Mitigation: Store UNIPILE_ACCESS_TOKEN outside prompts and logs, restrict access to trusted runtimes, and rotate the token if exposure is suspected. <br>
Risk: Read commands can expose LinkedIn chats, contacts, profiles, and account data to the agent session. <br>
Mitigation: Use the skill only in sessions where this account data is appropriate to process, and limit command scope with account IDs and result limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sudhanshu746/unipile-linkedin) <br>
- [Unipile API](https://www.unipile.com/) <br>
- [Unipile dashboard](https://dashboard.unipile.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with CLI commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses UNIPILE_DSN and UNIPILE_ACCESS_TOKEN to call the Unipile API for a connected LinkedIn account.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
