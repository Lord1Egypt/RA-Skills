## Description: <br>
Use screenshot and natural language instructions to locate PSD text layers and dispatch automated edits with confidence gating. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dhrxy](https://clawhub.ai/user/dhrxy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Designers, developers, and agent operators use this skill to apply screenshot-guided text edits to PSD or PSB assets through the psd-automator workflow while preserving matching typography where possible. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: High-confidence screenshot-guided PSD text edits may be applied automatically. <br>
Mitigation: Use backups or working copies for important PSD or PSB files before running the skill. <br>
Risk: The skill depends on a separate psd-automator core to perform file edits. <br>
Mitigation: Install and use it only when that core automation is trusted in the target environment. <br>
Risk: Invocation and execution details are recorded in a local usage log. <br>
Mitigation: Review local logging expectations before using the skill with sensitive design assets or instructions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown or plain text with command invocations, status messages, and confirmation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [High-confidence edits may be dispatched automatically; medium-confidence requests return candidate matches for confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
