## Description: <br>
Generates hyperrealistic texture and material images from text prompts using the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, designers, and developers use this skill to generate macro texture images for social content, thumbnails, product backgrounds, and visual experiments from a prompt and optional reference image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional reference IDs, and the Neta API token are sent to the remote Neta image API. <br>
Mitigation: Use a limited token where possible and avoid sending secrets, private data, or confidential concepts in prompts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blammectrappora/texture-art-generator) <br>
- [Neta API token and trial](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text image URL on stdout, with progress messages on stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token; accepts a prompt, size option, and optional reference image UUID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
