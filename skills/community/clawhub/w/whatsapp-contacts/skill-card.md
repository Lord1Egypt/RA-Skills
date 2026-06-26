## Description: <br>
List, search, and lookup WhatsApp contacts from the Baileys session cache. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MarcosRippel](https://clawhub.ai/user/MarcosRippel) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to list, search, or look up contacts from a local Baileys WhatsApp session cache without opening a live WhatsApp connection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can print names, phone numbers, status, image URLs, and group identifiers from the local WhatsApp/Baileys contact cache. <br>
Mitigation: Install only when the agent should access that local contact cache; prefer targeted searches or small list limits, and avoid sharing the JSON output outside the context where the contact details are needed. <br>
Risk: Results may be incomplete because only contacts already present in the local Baileys session cache are available. <br>
Mitigation: Treat missing contacts as cache absence rather than proof that a WhatsApp contact does not exist. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text] <br>
**Output Format:** [JSON printed by a Node.js command-line script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports list, search, and get commands; list accepts an optional result limit.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
