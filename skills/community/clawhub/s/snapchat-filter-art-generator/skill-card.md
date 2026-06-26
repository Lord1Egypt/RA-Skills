## Description: <br>
Generates nostalgic selfie images with Snapchat-style filters such as puppy ears, flower crowns, dog tongues, sparkles, and bunny noses through the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omactiengartelle](https://clawhub.ai/user/omactiengartelle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to generate 2010s-style social media selfie art from text prompts, with optional size selection and reference-image UUIDs for style inheritance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, selected image settings, API token, and reference image UUIDs are sent to the Neta/TalesOfAI service. <br>
Mitigation: Avoid confidential prompts or sensitive personal references, and use the skill only when sharing this data with Neta/TalesOfAI is acceptable. <br>
Risk: Command-line API tokens may appear in shell history or process listings. <br>
Mitigation: Treat the Neta token as a secret and prefer execution environments that limit shell history and process-list exposure. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/omactiengartelle/snapchat-filter-art-generator) <br>
- [Neta Open](https://www.neta.art/open/) <br>
- [Neta/TalesOfAI Image Task API](https://api.talesofai.com/v3/make_image) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown guidance and shell commands that return a direct image URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token and may use an optional reference image UUID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
