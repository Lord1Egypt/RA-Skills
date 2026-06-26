## Description: <br>
Analyzes pet training videos from local files or URLs through a cloud API to assess Sit, Down, and Stay command execution, posture match, response timing, success status, and report history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to evaluate pet obedience-training videos, retrieve historical training reports, and produce command-execution results for remote training or smart pet-training workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet-training videos or video URLs are sent to the provider's cloud service for analysis. <br>
Mitigation: Use only non-sensitive training videos and confirm the provider's retention, deletion, and report-sharing practices before deployment. <br>
Risk: The skill can automatically create or reuse a local account identity and stores authentication tokens locally. <br>
Mitigation: Install only in workspaces where silent identity association is acceptable, and ask the publisher how stored tokens and the local database can be reviewed, protected, rotated, and deleted. <br>
Risk: The authoritative security verdict is suspicious due to limited user control and disclosure around identity and token handling. <br>
Mitigation: Require human review of the publisher's security posture before using this skill in sensitive or regulated environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-pet-training-command-execution-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/18072937735) <br>
- [Pet training API documentation](artifact/references/api_doc.md) <br>
- [Shared analysis API documentation](artifact/skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, plain text, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include report links, command-execution tables, posture scores, response latency, success or failure status, and saved output files.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
