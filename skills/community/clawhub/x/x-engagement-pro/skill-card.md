## Description: <br>
Automates authentic engagement on X by monitoring AI image generation conversations, responding, amplifying content, and tracking metrics for brand growth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawbuilder](https://clawhub.ai/user/clawbuilder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Social media operators and AI image generation brands use this skill to monitor X conversations, prioritize mentions and keyword matches, and draft or perform replies and likes through an X account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform scheduled replies and likes without a clear per-action approval workflow when automation modes are enabled. <br>
Mitigation: Keep engagementMode set to manual unless automated account actions are explicitly intended, and monitor scheduled runs closely. <br>
Risk: The skill requires X account write access. <br>
Mitigation: Use a dedicated least-privileged X API credential and rotate it if the runtime or command source is not trusted. <br>
Risk: The agent invokes an external xapi command for searches, mentions, replies, and likes. <br>
Mitigation: Verify the xapi command source and behavior before enabling the skill in an OpenClaw gateway. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clawbuilder/x-engagement-pro) <br>
- [Publisher profile](https://clawhub.ai/user/clawbuilder) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Text and JSON-like agent run results with configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires X API credentials and may execute X account actions depending on engagement mode.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
