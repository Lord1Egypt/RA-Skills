## Description: <br>
Remove image backgrounds using the remove.bg API with API-key auth and transparent PNG output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rolandkakonyi](https://clawhub.ai/user/rolandkakonyi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to remove backgrounds from workspace images when high-quality cutouts are needed and cloud processing through remove.bg is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images are sent to remove.bg for processing. <br>
Mitigation: Use the skill only for images that are acceptable to process through remove.bg under the applicable terms. <br>
Risk: API usage may consume remove.bg account credits or paid quota. <br>
Mitigation: Confirm account quota and intended size setting before running the background-removal command. <br>
Risk: The skill requires REMOVE_BG_API_KEY. <br>
Mitigation: Store REMOVE_BG_API_KEY in OpenClaw-managed secret configuration rather than embedding it in prompts, files, or shell history. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rolandkakonyi/removebg-api) <br>
- [remove.bg API endpoint](https://api.remove.bg/v1.0/removebg) <br>
- [remove.bg API key dashboard](https://www.remove.bg/dashboard#api-key) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files] <br>
**Output Format:** [Transparent image file plus console text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes the processed image under outputs/removebg-api/ and prints a MEDIA line for chat workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
