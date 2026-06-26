## Description: <br>
Control the IMA (ima.copilot) desktop application for AI search and private knowledge retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hyddd](https://clawhub.ai/user/hyddd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to launch Tencent IMA, run public AI searches, and query configured private knowledge bases from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls a local Tencent IMA desktop session through remote debugging. <br>
Mitigation: Install only when this level of local application control is acceptable, and confirm the debug port is restricted to the local session and closed when use is complete. <br>
Risk: Private knowledge-base queries require storing or supplying a knowledge ID. <br>
Mitigation: Store the knowledge ID only in approved local configuration or environment variables, and review who can read that configuration before enabling private-knowledge mode. <br>
Risk: The skill rewrites IMA requests to enable private knowledge-base mode. <br>
Mitigation: Use private-knowledge mode only for explicit user-requested queries and review the request-rewriting behavior before deployment. <br>
Risk: The skill extracts rendered page text from the IMA session. <br>
Mitigation: Review whether the extracted page content may include sensitive private-knowledge results before sharing logs or agent output. <br>


## Reference(s): <br>
- [Tencent IMA Skill on ClawHub](https://clawhub.ai/hyddd/tencent-ima-skill) <br>
- [hyddd publisher profile](https://clawhub.ai/user/hyddd) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text search results with setup and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script prints extracted IMA page text and truncates result output to the first 3000 characters.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
