## Description: <br>
AI vaporwave art generator that creates synthwave, retrowave, and vaporwave images with neon grids, 80s retro colors, palm trees, and lo-fi aesthetics through the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omactiengartelle](https://clawhub.ai/user/omactiengartelle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate vaporwave, synthwave, and retrowave image URLs from text prompts for wallpapers, album art, social media visuals, and related aesthetic content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, reference image IDs, and the Neta token are sent to a third-party image-generation API. <br>
Mitigation: Use only non-sensitive prompts and reference IDs, and avoid exposing raw tokens in shell history or shared logs. <br>
Risk: Generated image URLs depend on the external service's availability, moderation, and content policies. <br>
Mitigation: Review generated outputs before use and handle API errors, moderation states, and timeouts before relying on the URL. <br>


## Reference(s): <br>
- [Neta Open API Access](https://www.neta.art/open/) <br>
- [ClawHub Skill Page](https://clawhub.ai/omactiengartelle/vaporwave-art-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text image URL printed to stdout, with progress and errors on stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token; accepts optional size and reference image UUID parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
