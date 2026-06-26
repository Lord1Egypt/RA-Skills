## Description: <br>
Generates stained-glass-style images and illustrations from text prompts through the Neta/TalesOfAI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate stained-glass-style portraits, animals, landscapes, decorative panels, and mosaic-inspired artwork from text prompts, with optional image-size and reference-image controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional reference image UUIDs, and the API token are sent to Neta/TalesOfAI. <br>
Mitigation: Use the skill only when the service is trusted for the prompt content, avoid sensitive or regulated prompts, and prefer limited or revocable API tokens. <br>
Risk: Image generation depends on an external API and may fail, time out, or return moderated results. <br>
Mitigation: Plan for retries or fallback handling and review generated outputs before using them in production or customer-facing workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blammectrappora/stained-glass-art-generator) <br>
- [Neta API token signup](https://www.neta.art/open/) <br>
- [Neta/TalesOfAI image generation endpoint](https://api.talesofai.com/v3/make_image) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [Plain text image URL with command-line status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token passed with --token; supports portrait, landscape, square, and tall sizes plus an optional reference image UUID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
