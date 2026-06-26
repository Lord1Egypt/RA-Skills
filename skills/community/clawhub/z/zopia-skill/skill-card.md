## Description: <br>
Zopia Skills helps agents manage Zopia projects for AI video and image creation, including scripts, characters, storyboards, multi-episode projects, progress polling, rendering, and result downloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lambdua](https://clawhub.ai/user/lambdua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agent users use this skill to create and manage Zopia AI video or image projects, send creative instructions to Zopia, monitor generation progress, render episodes, and download generated media. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Zopia access key that authorizes API calls. <br>
Mitigation: Keep ZOPIA_ACCESS_KEY private, provide it only through the environment, and rotate it if it may have been exposed. <br>
Risk: Creative prompts, project identifiers, and session identifiers are sent to Zopia APIs during normal operation. <br>
Mitigation: Avoid sending sensitive or confidential prompts unless Zopia is approved for that data. <br>
Risk: Generation and rendering actions can consume Zopia credits. <br>
Mitigation: Check account balance before starting work and confirm costly generation or render requests before running them. <br>
Risk: Downloaded media is written to local paths chosen by the agent or user. <br>
Mitigation: Choose output directories deliberately and inspect downloaded files before sharing or relying on them. <br>
Risk: Episode deletion is irreversible. <br>
Mitigation: Confirm the exact base and episode IDs before running delete operations. <br>


## Reference(s): <br>
- [Zopia](https://zopia.ai) <br>
- [Zopia Skills on ClawHub](https://clawhub.ai/lambdua/zopia-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON script outputs, and local media file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and ZOPIA_ACCESS_KEY; generated media can be downloaded to user-selected local directories.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
