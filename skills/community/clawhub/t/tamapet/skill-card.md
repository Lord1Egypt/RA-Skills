## Description: <br>
Clawpet is a Tamagotchi-style virtual pet skill that opens a Telegram Mini App for pet care, social visits, playdates, sharing, and pet lifecycle events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mturac](https://clawhub.ai/user/mturac) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent users use this skill to launch and share a Telegram virtual pet experience from a chat command. Developers can also use the bundled setup instructions to run the local service behind a Telegram Mini App. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The public server can expose or mutate user-linked pet data without authentication. <br>
Mitigation: Review before public exposure and add Telegram initData HMAC validation, stricter CORS and origin handling, safe HTML rendering, and clear data deletion and retention controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mturac/tamapet) <br>
- [Telegram Mini App](https://t.me/OpenClawTamagotchi_bot/pet) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown with Telegram links and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide setup of a local web service for a Telegram Mini App.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
