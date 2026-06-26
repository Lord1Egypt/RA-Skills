## Description: <br>
Upgrade OpenClaw, compare local changelog and configuration changes, audit hooks and doctor findings, and present upgrade recommendations for approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[decentraliser](https://clawhub.ai/user/decentraliser) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to update an OpenClaw installation, review version-specific changes, compare configuration schema gaps, audit hooks and doctor output, and decide which suggested improvements to apply. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can update and stash the local OpenClaw installation before a clear approval gate. <br>
Mitigation: Before running it, explicitly confirm whether openclaw update and any git stash should happen. <br>
Risk: The skill may send configuration data to an external model. <br>
Mitigation: Use a local model or redact private channel, plugin, and operational configuration details before external analysis. <br>
Risk: Bundled settings and state files may carry prior model choices or upgrade history into a new environment. <br>
Mitigation: Review or clear settings.json and state.json before first use so the run starts from the user's own choices and environment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with inline shell commands and configuration recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist upgrade state in state.json after a run.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
