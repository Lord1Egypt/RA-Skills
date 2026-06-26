## Description: <br>
Interact with Snipe-IT asset management via REST API for assets, users, licenses, accessories, consumables, components, locations, departments, models, manufacturers, status labels, categories, suppliers, maintenances, and reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bivex](https://clawhub.ai/user/bivex) <br>

### License/Terms of Use: <br>


## Use Case: <br>
IT administrators, asset managers, and developers use this skill to prepare Snipe-IT REST API calls for inventory, user, license, accessory, consumable, component, location, department, maintenance, and reporting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify or delete Snipe-IT inventory and user records when used with a powerful token. <br>
Mitigation: Use a dedicated least-privilege API token and manually confirm delete, checkout/checkin, restore, backup download, user-management, and other write or sensitive actions before execution. <br>
Risk: API tokens and server URLs may be exposed if copied into logs or chat. <br>
Mitigation: Store SNIPEIT_API_TOKEN securely, avoid printing it, and use only approved Snipe-IT servers through SNIPEIT_URL. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bivex/snipeit-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash snippets and REST API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, SNIPEIT_URL, and SNIPEIT_API_TOKEN; write and sensitive examples should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
