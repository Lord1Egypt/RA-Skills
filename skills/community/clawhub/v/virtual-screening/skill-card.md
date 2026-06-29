## Description: <br>
Virtual screening workflows for open and proprietary chemical libraries, including transformer-based screening and docking-based screening through SciMiner. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sciminer](https://clawhub.ai/user/sciminer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and computational drug discovery researchers use this skill to screen open or proprietary compound libraries against protein targets, using transformer-based ranking when only a sequence is available or docking-based screening when a structure or PDB ID is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote SciMiner API documentation drives request construction and may change between runs. <br>
Mitigation: Read the selected SciMiner documentation before each invocation and review generated code or shell commands before execution. <br>
Risk: The workflow uses a local SciMiner API key and uploads screening inputs to sciminer.tech. <br>
Mitigation: Store the API key outside the repository, avoid logging it, and use non-sensitive structures or libraries unless the service terms support the intended data. <br>


## Reference(s): <br>
- [SciMiner tool API files](https://sciminer.tech/tool_api_files/) <br>
- [SciMiner API key utility](https://sciminer.tech/utility) <br>
- [Virtual Screening on ClawHub](https://clawhub.ai/sciminer/skills/virtual-screening) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with invocation steps, JSON result summaries, and share URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SciMiner API documentation for payload construction and returns task identifiers and share URLs for successful runs.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
