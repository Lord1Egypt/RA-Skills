## Description: <br>
Generate waifu generator ai image generator images with AI via the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomcarranzaem](https://clawhub.ai/user/tomcarranzaem) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate anime-style character images from text prompts, with optional size selection and reference image UUIDs. The skill returns a direct image URL from the Neta AI image generation service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional reference image UUIDs, and the Neta/TalesOfAI API token are sent to api.talesofai.com. <br>
Mitigation: Use the skill only for prompts and reference images that are appropriate to share with the external service, and avoid sensitive or regulated content. <br>
Risk: Passing the API token with --token can expose it in shared terminal history or logs. <br>
Mitigation: Use the skill on trusted machines and avoid running commands where shell history, logs, or shared sessions may disclose the token. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tomcarranzaem/waifu-generator-skill) <br>
- [Neta AI access page](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [Plain text URL printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token passed with --token; supports portrait, landscape, square, and tall image sizes plus an optional reference image UUID.] <br>

## Skill Version(s): <br>
3.0.0 (source: server evidence release.version and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
