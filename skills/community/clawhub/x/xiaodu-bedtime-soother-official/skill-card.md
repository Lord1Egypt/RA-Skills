## Description: <br>
Orchestrates child bedtime routines through the installed xiaodu-control-official skill, using XiaoDu smart screens and XiaoDu IoT devices for scene-first bedtime setup, announcements, bedtime media, and delayed story shutdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dueros-mcp](https://clawhub.ai/user/dueros-mcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and home-automation agents use this skill to turn broad bedtime requests into a conservative XiaoDu routine: select an existing bedtime scene when available, safely adjust supported IoT devices, announce the bedtime transition, start story or calming media, and schedule a stop or screen-off follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control XiaoDu smart screens, supported IoT devices, media playback, and delayed stop or screen-off behavior. <br>
Mitigation: Install only for agents that should manage bedtime home-automation flows, and review the xiaodu-control-official dependency before deployment because it performs the underlying device actions. <br>
Risk: A broad bedtime request could affect the wrong room or device if available targets are ambiguous. <br>
Mitigation: Follow the skill's minimum-confirmation rule: ask for clarification when multiple reasonable smart screens, rooms, or device targets exist, and avoid whole-home control by default. <br>
Risk: User bedtime preferences may be written to local memory files. <br>
Mitigation: Store only preferences that the user actually provided, and avoid claiming that a preference was remembered unless the file write completed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dueros-mcp/xiaodu-bedtime-soother-official) <br>
- [Usage Notes](references/usage-notes.md) <br>
- [Test Cases](references/test-cases.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Natural-language guidance with inline shell commands and optional preference file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May schedule delayed stop and screen-off commands through scripts/bedtime_story_tail.sh when a smart screen target is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
