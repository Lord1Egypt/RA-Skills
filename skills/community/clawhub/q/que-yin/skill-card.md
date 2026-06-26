## Description: <br>
Que Yin is a local load-balancing helper that reports machine resource status, assigns simple task scheduling output, and generates load reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lt8899789](https://clawhub.ai/user/lt8899789) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect local CPU and memory usage, simulate task assignment, and generate simple load recommendations for agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can report local machine resource details such as CPU model, memory usage, platform, and uptime. <br>
Mitigation: Run it only where those local resource details are acceptable in agent output, and avoid forwarding logs to audiences that should not see machine metadata. <br>
Risk: The artifact documentation is Chinese-only, which may make behavior and command expectations harder for some reviewers to confirm. <br>
Mitigation: Review the documented commands and outputs with translation support before deployment when the operating team does not read Chinese. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lt8899789/que-yin) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include local CPU model, memory usage, platform, uptime, timestamps, and simulated queue metrics.] <br>

## Skill Version(s): <br>
1.0.35 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
