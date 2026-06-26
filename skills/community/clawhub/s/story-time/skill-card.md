## Description: <br>
Choose-your-own-adventure interactive fiction through your agent. Pre-built stories and a framework for building your own. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to play choice-driven interactive fiction through an agent and to build custom story scenarios with tracked choices, inventory, and save/load state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Story progress is saved to a local JSON file in the working directory or a configured path. <br>
Mitigation: Use a non-sensitive save path, keep backups for important story data, and avoid storing saves in directories with confidential files. <br>
Risk: Custom scenarios or multiplayer story content may include material users did not intend to share. <br>
Mitigation: Review custom scenarios and generated story state before sharing them in group chats or with other users. <br>


## Reference(s): <br>
- [StoryTime ClawHub page](https://clawhub.ai/TheShadowRose/story-time) <br>
- [Publisher profile](https://clawhub.ai/user/TheShadowRose) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown and plain text story scenes, choices, scenario templates, and JavaScript usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save and load local game state as JSON when the included StoryTime module is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
