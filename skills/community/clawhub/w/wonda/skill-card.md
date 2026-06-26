## Description: <br>
Wonda helps agents use the Wonda CLI to generate and edit media, run social research, automate selected social workflows, and publish content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[degausai](https://clawhub.ai/user/degausai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, marketers, and agent operators use this skill to route content generation, media editing, local video finishing, social research, and publishing through the Wonda CLI. It is intended for accounts and content the user controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide high-impact social actions such as signup, posting, direct messages, follows, votes, connection requests, permission grants, Terms acceptance, and deletes. <br>
Mitigation: Require explicit user approval before any account, consent, permission, posting, messaging, voting, following, connection, or delete action. <br>
Risk: The skill uses Wonda credentials and may handle social tokens, verification codes, API keys, and short-lived device stream URLs. <br>
Mitigation: Keep credentials, verification data, and stream URLs private; use accounts the user controls and rotate or revoke exposed credentials. <br>
Risk: The security summary flags suspicious social automation behavior, including stealth or detection-avoidance language. <br>
Mitigation: Install only if the Wonda CLI provider is trusted, review automation plans before execution, and stop for human handoff on rate-limit, CAPTCHA, consent, or ambiguous screens. <br>


## Reference(s): <br>
- [Wonda homepage](https://wonda.sh) <br>
- [ClawHub Wonda listing](https://clawhub.ai/degausai/wonda) <br>
- [Degaus AI publisher profile](https://clawhub.ai/user/degausai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke external Wonda services and create, edit, or publish media depending on user-approved commands.] <br>

## Skill Version(s): <br>
1.2.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
