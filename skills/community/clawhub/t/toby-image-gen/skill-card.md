## Description: <br>
Generate and edit images via SkillBoss API Hub, with style presets, batch generation, and an HTML gallery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate or edit images from prompts, apply visual style presets, run batches, and review results in a gallery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and edited source images are sent to SkillBoss API Hub with the user's SKILLBOSS_API_KEY. <br>
Mitigation: Do not submit sensitive prompts or private images unless that external processing is acceptable, and keep the API key scoped and protected. <br>
Risk: Generated images may be shared publicly, used as profile avatars, or saved to memory without clear approval boundaries. <br>
Mitigation: Require explicit user confirmation of the exact image, destination account, and retained content before sharing, updating profiles, or storing results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/toby-image-gen) <br>
- [OpenClaw](https://openclaw.org) <br>
- [SkillBoss API Hub](https://api.heybossai.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, files, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; runtime output includes PNG images, prompts.json, and an HTML gallery.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and SKILLBOSS_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
