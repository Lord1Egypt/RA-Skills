## Description: <br>
Generate ai sticker pack generator images from text descriptions via the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate sticker-pack style images from text prompts, with optional size and reference-image parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends sticker prompts, optional reference IDs, and a Neta API token to api.talesofai.com. <br>
Mitigation: Use a limited-purpose token where possible and avoid sensitive prompts or reusable tokens in shared terminals, logs, or shell history. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/blammectrappora/sticker-pack-skill) <br>
- [Neta API token setup](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Direct image URL printed as text, with CLI status messages on stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token and sends the prompt, optional reference ID, and token to api.talesofai.com.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
