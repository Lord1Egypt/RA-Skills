## Description: <br>
List and search WhatsApp Business labels/tags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MarcosRippel](https://clawhub.ai/user/MarcosRippel) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to inspect local WhatsApp Business label metadata, list available labels, and find contacts or chats associated with a selected label. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the local OpenClaw WhatsApp Business session cache. <br>
Mitigation: Run it only in environments where the agent is allowed to inspect that local session cache. <br>
Risk: Output may include contact IDs, contact names, and label metadata. <br>
Mitigation: Treat results as business/contact metadata and share them only with the intended task audience. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MarcosRippel/whatsapp-labels) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON objects printed to stdout, with command examples in Markdown documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results may include WhatsApp Business label IDs, label names, colors, contact IDs, contact names, and matched labels.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
