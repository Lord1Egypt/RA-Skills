## Description: <br>
TOKEN SOP caches successful OpenClaw browser workflows locally and can match or contribute reusable workflows through a configured cloud endpoint to reduce repeated token use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ainclaw](https://clawhub.ai/user/ainclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use TOKEN SOP to intercept repeated browser automation intents, replay validated local or cloud-matched Lobster workflows, and save successful sessions for later reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Session-derived workflow data may be automatically contributed to the configured cloud service. <br>
Mitigation: Review before installing, disable auto_contribute in sensitive environments, and avoid use on accounts or pages where traces may contain sensitive or consequential actions. <br>
Risk: Cloud-provided workflows may be executed with weak user control. <br>
Mitigation: Consider disabling cloud matching, restrict the cloud_endpoint to a trusted service, and review workflow behavior before using the skill on high-impact browser tasks. <br>
Risk: Replayed clicks or form submissions could change important data. <br>
Mitigation: Use the skill only where replayed browser actions are acceptable, and bypass cached workflow execution for account, payment, administrative, or irreversible workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ainclaw/tokensop) <br>
- [Publisher Profile](https://clawhub.ai/user/ainclaw) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Manifest](artifact/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, code] <br>
**Output Format:** [OpenClaw hook responses, Lobster workflow execution results, local workflow files, and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May replay cached workflows, persist workflow traces locally, and send match, contribution, or failure-report payloads to the configured cloud endpoint.] <br>

## Skill Version(s): <br>
5.6.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
