## Description: <br>
Generate and vectorize SVG graphics via the QuiverAI API (Arrow model). Use when the user asks to create logos, icons, or illustrations as SVG, convert raster images (PNG/JPEG/WebP) to SVG, or generate vector graphics from text prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charmmm718](https://clawhub.ai/user/charmmm718) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and designers use this skill to ask an agent for SVG generation or raster-to-SVG vectorization through QuiverAI. It provides setup guidance, API examples, request parameters, and response handling details for text-to-SVG and image-to-SVG workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts, reference images, or raster images to QuiverAI and requires access to a QuiverAI API key. <br>
Mitigation: Use a dedicated API key where possible, avoid confidential or regulated material unless approved by your organization, and rotate or revoke the key if exposure is suspected. <br>
Risk: API requests consume QuiverAI credits and may fail when credits, authorization, or rate limits are exhausted. <br>
Mitigation: Review generated requests before execution, monitor credit usage, and handle 401, 402, and 429 responses as described by the skill. <br>


## Reference(s): <br>
- [QuiverAI Skill Page](https://clawhub.ai/charmmm718/quiverai) <br>
- [QuiverAI Site](https://quiver.ai) <br>
- [QuiverAI Documentation](https://docs.quiver.ai) <br>
- [QuiverAI API Base](https://api.quiver.ai/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, TypeScript, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include QuiverAI API request parameters and SVG response handling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
