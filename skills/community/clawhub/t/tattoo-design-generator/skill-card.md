## Description: <br>
Generates tattoo concept art, ink illustrations, and reference sheets from text prompts using the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omactiengartelle](https://clawhub.ai/user/omactiengartelle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Tattoo artists, studios, and individuals use this skill to turn tattoo ideas into generated concept art, flash designs, sleeve concepts, and reference images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends tattoo prompts, optional reference UUIDs, and the Neta API token to the external Neta/TalesOfAI service. <br>
Mitigation: Use a trusted token source such as an environment variable and avoid submitting sensitive client or personal reference material unless the provider's data handling is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/omactiengartelle/tattoo-design-generator) <br>
- [Publisher profile](https://clawhub.ai/user/omactiengartelle) <br>
- [Neta API access](https://www.neta.art/open/) <br>
- [TalesOfAI image generation endpoint](https://api.talesofai.com/v3/make_image) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [Plain text image URL returned by a Node CLI command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a tattoo prompt, a Neta API token, and optional size or reference-image UUID arguments.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
