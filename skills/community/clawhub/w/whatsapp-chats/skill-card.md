## Description: <br>
List, search, and analyze WhatsApp conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MarcosRippel](https://clawhub.ai/user/MarcosRippel) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agents and users use this skill to browse, search, and summarize locally stored WhatsApp chat metadata from a Baileys session cache. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local WhatsApp chat/session data that may include names, phone numbers, group identifiers, and message content. <br>
Mitigation: Use it only in a trusted workspace and review outputs before sharing, storing, or pasting them elsewhere. <br>
Risk: Broad or casual searches can expose private conversation metadata beyond the user's immediate intent. <br>
Mitigation: Use narrow search terms and limit result counts when inspecting sensitive local data. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Analysis] <br>
**Output Format:** [JSON printed to stdout, with optional text summaries by the calling agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local WhatsApp credential/session cache paths and can return contacts, groups, and chat statistics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
