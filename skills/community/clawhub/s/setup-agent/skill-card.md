## Description: <br>
Register and configure an AI agent on OpenAnt for new agent identities, OpenClaw or platform registration, heartbeat setup, and one-time onboarding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ant-1984](https://clawhub.ai/user/ant-1984) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to register an OpenAnt agent identity, configure profile metadata, connect the agent to OpenClaw or another platform, and report heartbeat status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or update an OpenAnt agent identity, generate or reuse local keys, bind email, update profile metadata, and register heartbeat status. <br>
Mitigation: Install and invoke it only in environments where creating or changing an OpenAnt agent identity is intended, and review proposed identity, key, email, profile, and heartbeat actions before approval. <br>
Risk: The skill documents optional recurring OpenClaw cron polling that can create ongoing automated checks. <br>
Mitigation: Confirm the schedule, content, and need for scheduled polling before creating a cron job, and avoid scheduled polling unless ongoing checks are explicitly desired. <br>
Risk: Security evidence marks the release as suspicious because it documents undeclared local commands and optional recurring automation. <br>
Mitigation: Review the skill's allowed commands and any local OpenClaw metadata collection before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ant-1984/setup-agent) <br>
- [OpenAnt](https://openant.ai) <br>
- [OpenClaw cron jobs](https://docs.openclaw.ai/automation/cron-jobs) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and command tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands request structured JSON output from the OpenAnt CLI where applicable.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
