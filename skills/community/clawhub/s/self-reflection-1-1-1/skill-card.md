## Description: <br>
Continuous self-improvement through structured reflection and memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[86293073](https://clawhub.ai/user/86293073) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to help an AI agent periodically check whether reflection is due, read prior lessons, and log new lessons into a persistent memory file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup references an external CLI source outside the scanned package. <br>
Mitigation: Review and pin the external CLI source before running installation or command examples. <br>
Risk: The skill can store long-lived reflection memory that may capture sensitive prompts, incident details, or proprietary workflow notes. <br>
Mitigation: Avoid logging secrets, customer data, private prompts, incident details, or proprietary notes; configure the memory file location and retention deliberately. <br>
Risk: Heartbeat-based reflection can create recurring agent activity even when it is not wanted. <br>
Mitigation: Enable the heartbeat only when recurring self-reflection is intended, and review the interval and active-hours configuration before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/86293073/self-reflection-1-1-1) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires jq and date; may write reflection notes and timer state to configured local files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact manifest/frontmatter reports 1.1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
