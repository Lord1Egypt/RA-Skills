## Description: <br>
Automatically sets up a three-layer OpenClaw memory system with long-term memory, daily notes, and nightly fact extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[casperzinou](https://clawhub.ai/user/casperzinou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to create durable AI memory files, record daily notes, and configure recurring extraction of important facts from conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Long-term memory files may retain secrets or sensitive personal information from conversations. <br>
Mitigation: Define allowed data categories, add rules to avoid storing secrets or sensitive personal information, and review generated memory files before relying on them. <br>
Risk: The scheduled nightly extraction job may continue reviewing conversations without clear consent, limits, or removal guidance. <br>
Mitigation: Confirm consent, allowed scope, timezone, disable steps, and deletion or redaction process before enabling the cron job. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/casperzinou/talonforge-memory) <br>
- [Publisher profile](https://clawhub.ai/user/casperzinou) <br>
- [TalonForge homepage](https://talonforge.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with memory-file templates and an OpenClaw cron command.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill directs an agent to create persistent memory files and configure a recurring nightly extraction job.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
