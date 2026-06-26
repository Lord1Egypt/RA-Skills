## Description: <br>
Rtk Compressor intelligently compresses CLI output by removing comments, blank lines, boilerplate, and redundancy while preserving key information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Efficiency97](https://clawhub.ai/user/Efficiency97) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to reduce the token footprint of command output, logs, JSON, directory listings, and file contents before passing them to an agent or model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Command output or logs provided for compression may contain secrets or sensitive operational details. <br>
Mitigation: Review inputs before use and avoid granting credentials or allowing account or file changes unless the agent action has been explicitly reviewed. <br>


## Reference(s): <br>
- [Rtk Compressor on ClawHub](https://clawhub.ai/Efficiency97/rtk-compressor) <br>
- [rtk-compressor on PyPI](https://pypi.org/project/rtk-compressor/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and concise text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces compressed text intended to preserve core information while reducing token usage.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
