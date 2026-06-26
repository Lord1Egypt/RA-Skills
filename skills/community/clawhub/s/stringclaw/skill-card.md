## Description: <br>
Make real phone calls via Stringclaw by initiating an outbound voice call that connects the user to a live session with the agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OscarWoHA](https://clawhub.ai/user/OscarWoHA) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill when a user asks to talk by voice and the agent needs to place an outbound phone call through a configured Stringclaw account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real phone calls through the user's Stringclaw account. <br>
Mitigation: Install only when phone-call capability is intended, and require confirmation of the action, destination or account, and possible charges before every call. <br>
Risk: Calls can be triggered too broadly if the agent treats casual voice-related language as final authorization. <br>
Mitigation: Add an explicit final confirmation step before running the bridge call command. <br>
Risk: Incorrect gateway or bridge setup can expose call failures or unexpected behavior during use. <br>
Mitigation: Review the gateway and bridge setup, verify the bridge reports ready, and resolve setup errors before placing a call. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/OscarWoHA/stringclaw) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/OscarWoHA) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown with inline bash commands and JSON success or error examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires STRINGCLAW_API_KEY and the stringclaw-bridge binary; successful calls return a JSON call identifier.] <br>

## Skill Version(s): <br>
0.0.9 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
