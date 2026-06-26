## Description: <br>
Read SignUpGenius sign-up sheets, slot reports, and groups, and add members to groups from a signed-in account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent inspect SignUpGenius profile, group, sign-up, and slot information for their own account. It can also help add group members or RSVP to public sign-up slots when the user confirms the intended change. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive SignUpGenius account access through cookies, direct credentials, or a Pro API key. <br>
Mitigation: Use the narrowest authentication mode that works, prefer avoiding stored plaintext passwords, and install only when the npm package is trusted. <br>
Risk: The skill includes write-capable actions for RSVPs and adding group members. <br>
Mitigation: Require the agent to show and confirm RSVP or group-member changes before sending them. <br>
Risk: Slot reports require a SignUpGenius Pro API key and some session-mode or SSO account flows are unsupported. <br>
Mitigation: Use the Pro API key for report tools and use the fetchproxy mode for accounts that rely on SSO or two-factor authentication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chrischall/signupgenius-mcp) <br>
- [SignUpGenius](https://www.signupgenius.com) <br>
- [signupgenius-mcp npm package](https://www.npmjs.com/package/signupgenius-mcp) <br>
- [signupgenius-mcp source repository](https://github.com/chrischall/signupgenius-mcp) <br>
- [fetchproxy extension](https://github.com/chrischall/fetchproxy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call MCP tools that return SignUpGenius account, group, sign-up, slot, RSVP, and member data.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
