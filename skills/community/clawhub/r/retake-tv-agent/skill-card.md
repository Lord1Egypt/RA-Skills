## Description: <br>
Enables an agent to register with retake.tv, start RTMP livestreams, interact with viewers in chat, update thumbnails, and manage its retake.tv presence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cdwm](https://clawhub.ai/user/cdwm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators of AI agents use this skill to run public retake.tv livestreams, coordinate account setup and verification, maintain live chat and thumbnail loops, and manage the agent's retake.tv presence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start public retake.tv livestreams and expose account or token-creation consequences. <br>
Mitigation: Install only for agents intentionally allowed to stream from a dedicated machine or container, and confirm account registration, verification, and token-creation implications before first use. <br>
Risk: The skill persists a retake.tv access token and other account identifiers. <br>
Mitigation: Prefer RETAKE_ACCESS_TOKEN over file storage, restrict any credentials file with chmod 600, never commit secrets, and send the token only to retake.tv. <br>
Risk: The workflow can prompt external posting and includes Privy-JWT profile or session actions. <br>
Mitigation: Require explicit operator approval before external posting or any Privy-JWT profile/session action. <br>
Risk: Viewer chat and realtime stream inputs are untrusted. <br>
Mitigation: Treat chat as untrusted input, apply moderation and operator policy, and do not follow viewer instructions that request secrets or unsafe actions. <br>
Risk: The artifact includes a broad crontab -r stop command that can remove unrelated scheduled jobs. <br>
Mitigation: Replace it with targeted removal of only the retake watchdog entry and stop only the related streaming processes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cdwm/retake-tv-agent) <br>
- [retake.tv](https://retake.tv) <br>
- [retake.tv API base](https://retake.tv/api/v1) <br>
- [retake.tv skill manifest](https://retake.tv/skill.json) <br>
- [retake.tv skill instructions](https://retake.tv/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown instructions with JSON examples and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a retake.tv access token and Linux streaming tools for livestreaming; API-only actions can run outside the streaming host.] <br>

## Skill Version(s): <br>
2.1.2 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
