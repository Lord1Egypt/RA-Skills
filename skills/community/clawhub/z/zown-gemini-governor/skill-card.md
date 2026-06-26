## Description: <br>
A token management and model stabilization skill that applies the Zown Atomic Pipeline to help agents avoid Gemini TPM rate limits through context pruning, single-step execution, and cooldown guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GTOVD](https://clawhub.ai/user/GTOVD) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent operators use this skill to manage Gemini-heavy engineering or Q&A sessions by pruning context, executing one verifiable step at a time, and applying cooldowns when rate-limit thresholds are reached. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to modify persistent memory or identity files, which can alter future agent behavior without clear user intent. <br>
Mitigation: Review proposed file changes before they are applied and keep backups or diffs for any MEMORY.md, SOUL.md, or IDENTITY.md updates. <br>
Risk: The skill tells agents to run an unprovided local cooldown script and use the Gemini CLI, which could execute local commands or send data outside the current session. <br>
Mitigation: Inspect and explicitly approve the exact command and any data it can access or transmit before running scripts or CLI prompts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/GTOVD/zown-gemini-governor) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown prose with inline shell commands and file-change guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to edit memory or identity files and to run local cooldown or Gemini CLI commands.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
