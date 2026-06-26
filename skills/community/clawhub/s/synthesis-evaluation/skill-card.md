## Description: <br>
Synthesis evaluation workflows combining SynFormer-ED, Retrosynthesis Planner, and SAScore through SciMiner. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sciminer](https://clawhub.ai/user/sciminer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and scientific teams use this skill to generate synthesizable analogs, recommend retrosynthetic routes, and score synthetic accessibility for molecule candidates through SciMiner. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a user-provided SciMiner API key stored at the documented local path. <br>
Mitigation: Confirm the credential file is present, keep the key out of prompts, logs, and repository files, and do not print or persist it. <br>
Risk: Molecule inputs or uploaded files are sent to SciMiner for synthesis evaluation. <br>
Mitigation: Use the skill only when SciMiner's terms and sharing behavior are appropriate for the data, especially for confidential chemical information. <br>


## Reference(s): <br>
- [SciMiner API Key Utility](https://sciminer.tech/utility) <br>
- [SciMiner Tool API Files](https://sciminer.tech/tool_api_files/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration, API calls, markdown] <br>
**Output Format:** [Markdown guidance with code or shell snippets and SciMiner share_url links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SciMiner task results and returns share_url links for successful tasks.] <br>

## Skill Version(s): <br>
1.0.4 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
