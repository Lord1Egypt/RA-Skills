## Description: <br>
Generate AI selfie art portraits from text descriptions - cinematic portraits, anime illustrations, oil painting style, and artistic profile pictures via the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[barbaraledbettergq](https://clawhub.ai/user/barbaraledbettergq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate stylized selfie portraits and profile-picture art from a text prompt, with optional size, style, and reference-image controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional reference image UUIDs, and the Neta token are sent to the external Neta/TalesOfAI service. <br>
Mitigation: Use a dedicated or low-privilege token, avoid sensitive personal or confidential prompt content, and rotate the token if it appears in logs, shell history, or shared output. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/barbaraledbettergq/selfie-art-generator) <br>
- [Neta token setup](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Plain text image URL on stdout, with Markdown usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token; accepts a prompt, size, style, and optional reference image UUID.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
