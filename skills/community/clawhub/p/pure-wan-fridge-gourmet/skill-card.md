## Description: <br>
Generates dish concept images or videos and recipe guidance from fridge photos using Alibaba DashScope Wan models and a bundled recipe database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laojun509](https://clawhub.ai/user/laojun509) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn refrigerator photos into cuisine-specific meal ideas, generated food media, and practical recipe steps. It supports command-line and Python usage for selecting cuisine, difficulty, cooking time, model, and optional custom requirements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fridge photos and prompts may contain private items or location clues and are sent to Alibaba DashScope or the configured WAN_API_URL for processing. <br>
Mitigation: Crop or redact private items, medications, labels, faces, and location clues before use. <br>
Risk: The skill requires an API key for the external image or video generation service. <br>
Mitigation: Use a limited API key, keep it in environment variables, and run the skill in a virtual environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/laojun509/pure-wan-fridge-gourmet) <br>
- [Publisher profile](https://clawhub.ai/user/laojun509) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Usage examples](artifact/scripts/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text, optional JSON result files, and Python dictionary results containing media URLs and recipe details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a WAN_API_KEY and may use WAN_API_URL for the configured DashScope-compatible endpoint.] <br>

## Skill Version(s): <br>
3.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
