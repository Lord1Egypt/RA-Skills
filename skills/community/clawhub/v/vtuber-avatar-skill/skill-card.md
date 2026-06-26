## Description: <br>
Generate vtuber avatar creator ai images with AI via the Neta AI image generation API (free trial at neta.art/open). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate VTuber avatar images from text prompts, with optional size selection and reference-image style inheritance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional reference image UUIDs, and the Neta/TalesofAI API token are sent to api.talesofai.com. <br>
Mitigation: Use a token scoped to this service, avoid sensitive prompt content, and review whether the external API is acceptable for the intended use. <br>
Risk: Passing API tokens directly in command lines can expose them in shared terminals or shell history. <br>
Mitigation: Prefer safer secret handling and avoid pasting long-lived tokens into shared command lines. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/blammectrappora/vtuber-avatar-skill) <br>
- [Neta AI API Token Page](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text URL printed to stdout, with Markdown documentation and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a direct generated image URL after polling the remote image API.] <br>

## Skill Version(s): <br>
2.0.1 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
