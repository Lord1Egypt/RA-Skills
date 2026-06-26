## Description: <br>
Generate waifu generator AI images from text descriptions via the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omactiengartelle](https://clawhub.ai/user/omactiengartelle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to generate anime-style character images from text prompts and optionally apply style inheritance from a reference image UUID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional reference UUIDs, and the Neta API token are sent to a third-party image generation service. <br>
Mitigation: Avoid sensitive prompts, review third-party service terms before use, and prefer passing the token through an environment variable or secret store instead of shell history. <br>


## Reference(s): <br>
- [Neta API token and trial page](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Direct image URL with CLI status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token, a text prompt, and optional size or reference UUID arguments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
