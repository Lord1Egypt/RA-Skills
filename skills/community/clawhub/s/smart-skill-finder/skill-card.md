## Description: <br>
Finds and recommends relevant AI agent skills across multiple ecosystems (Skills CLI, Clawhub, GitHub) using intelligent semantic understanding to match user needs with available capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edkuo7](https://clawhub.ai/user/edkuo7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to find relevant installable agent skills from Skills CLI, ClawHub, and GitHub based on a natural language request. It returns ranked recommendations, source context, security status when available, and installation guidance for review before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Normal search text can be passed into a local shell command when the skill searches Skills CLI. <br>
Mitigation: Review or patch the Skills CLI subprocess call to use an argument list instead of shell=True before enabling the skill in a normal agent environment. <br>
Risk: Security labels and trust claims may be overbroad or stale. <br>
Mitigation: Check the original registry or repository before installing or relying on a recommended skill. <br>
Risk: The server security verdict is suspicious. <br>
Mitigation: Install only after review or patching, and use the skill only for explicit skill-search requests. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/edkuo7/smart-skill-finder) <br>
- [README](artifact/README.md) <br>
- [Usage examples](artifact/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown recommendation list with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Limits recommendations to the most relevant results and includes security status when the source ecosystem provides it.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, CHANGELOG released 2026-03-19) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
