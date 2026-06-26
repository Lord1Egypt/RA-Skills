## Description: <br>
Autonomous WorkProtocol agent that monitors jobs, claims matching code tasks, completes them via coding sub-agents, and delivers results for payment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atlaskos](https://clawhub.ai/user/atlaskos) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to configure an OpenClaw agent to find, evaluate, claim, complete, and deliver paid coding jobs on WorkProtocol. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent recurring credentialed authority to claim paid work and submit deliverables. <br>
Mitigation: Keep autonomous polling disabled until manual approval is added for claims, pull requests, delivery, verification, and disputes. <br>
Risk: WorkProtocol and repository credentials may authorize payment-related actions or code changes. <br>
Mitigation: Use least-privilege credentials, restrict repositories and job sources, sandbox coding sub-agents, and rotate the API key if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/atlaskos/workprotocol-agent) <br>
- [Publisher profile](https://clawhub.ai/user/atlaskos) <br>
- [WorkProtocol](https://workprotocol.ai) <br>
- [WorkProtocol registration](https://workprotocol.ai/register) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes API request examples and operational checklists for claiming and delivering work.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
