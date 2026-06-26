## Description: <br>
Auto-switch music scenes by workday time slot and send matching greeting emails with scene-specific GIFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Home automation users and agent operators use this skill to switch workday music scenes by time slot and send matching greeting emails. It supports one-off runs, forced time slots, dry runs, and scheduled weekday automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A configurable music command can execute shell commands when the skill switches scenes. <br>
Mitigation: Keep MUSIC_CMD fixed to a trusted music controller command and avoid shell metacharacters or user-supplied command strings. <br>
Risk: Scheduled runs can send greeting emails automatically to the configured recipient. <br>
Mitigation: Verify GREETING_TO and SMTP settings before live use, test with --dry-run first, and use an app-specific SMTP password. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/workday-music-greeting) <br>
- [Publisher profile](https://clawhub.ai/user/terrycarter1985) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational instructions for an agent to run Node.js automation scripts that control music scenes and send SMTP email.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
