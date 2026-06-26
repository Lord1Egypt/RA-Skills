## Description: <br>
StylePilot is a local-first personal wardrobe assistant that helps agents manage clothing records, generate outfit suggestions, and prepare travel packing recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mars2003](https://clawhub.ai/user/mars2003) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and personal agents use StylePilot to build a local wardrobe, add clothing metadata and photos, and generate outfit or travel packing recommendations based on scene, weather, trip length, and explicit feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wardrobe photos, metadata, outfit history, and feedback can reveal personal appearance, preferences, or private context if retained casually. <br>
Mitigation: Use StylePilot only on trusted machines, avoid storing sensitive photos or location-revealing images, and review or delete the local data directory when it is no longer needed. <br>
Risk: Outfit recommendations can be poorly matched when scene, weather, season, or dress-code constraints are missing or inaccurate. <br>
Mitigation: Ask for the minimum missing context before recommending, pass known weather and trip length into the CLI arguments, and label incomplete recommendations when key wardrobe categories are missing. <br>


## Reference(s): <br>
- [StylePilot on ClawHub](https://clawhub.ai/mars2003/stylepilot) <br>
- [README](artifact/README.md) <br>
- [Security Considerations](artifact/SECURITY.md) <br>
- [Skill Instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON responses from CLI-backed wardrobe commands, with optional shell commands for local execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may reference local wardrobe records, copied image paths, missing clothing categories, selected items, and explicit feedback reasons.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
