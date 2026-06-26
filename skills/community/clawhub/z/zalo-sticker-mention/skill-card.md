## Description: <br>
Automatically tags the latest sender in Zalo group chats and lets the agent send a sticker by appending a keyword marker. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuanminhhole](https://clawhub.ai/user/tuanminhhole) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw developers and bot operators use this skill to patch the Zalo channel driver so group chat replies can include automatic sender mentions, optional sticker keyword markers, and sticker search support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The patch can permanently modify installed @openclaw/zalouser driver files across discovered OpenClaw locations. <br>
Mitigation: Review mentions.js before use, apply it only in an intended OpenClaw workspace, and keep the provided --restore workflow available. <br>
Risk: The patch may affect multiple discovered Zalo driver installs without enough scoping or confirmation. <br>
Mitigation: Test first in a disposable or non-production OpenClaw workspace and verify which driver paths are being patched. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tuanminhhole/zalo-sticker-mention) <br>
- [Publisher profile](https://clawhub.ai/user/tuanminhhole) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and sticker keyword markers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct the agent to append at most one [Sticker: <keyword>] marker at the end of a Zalo reply.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
