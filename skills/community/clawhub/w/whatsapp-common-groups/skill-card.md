## Description: <br>
Find groups shared between contacts and check group membership. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MarcosRippel](https://clawhub.ai/user/MarcosRippel) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to query local WhatsApp state for groups associated with a phone number, verify whether a phone number belongs to a specific group, or list known group members when they have a legitimate need to inspect that data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local WhatsApp credential and state files and its outputs can reveal private phone numbers, group IDs, group names, and relationship metadata. <br>
Mitigation: Install and run it only when you intentionally want an agent to inspect that local WhatsApp state, and keep resulting transcripts and logs access-controlled. <br>
Risk: The all-members command can broadly enumerate known members across groups. <br>
Mitigation: Prefer narrow find or check commands for specific questions, and use all-members only when broad enumeration is necessary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MarcosRippel/whatsapp-common-groups) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands] <br>
**Output Format:** [JSON text emitted by a Node.js command-line script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include phone numbers, WhatsApp group IDs, group names, membership status, counts, and error messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
