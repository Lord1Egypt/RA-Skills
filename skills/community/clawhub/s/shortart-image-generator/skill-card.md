## Description: <br>
Generates images through ShortArt AI in three modes: text or image prompted artwork, e-commerce product image sets, and template-based marketing or social media images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yige666s](https://clawhub.ai/user/yige666s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to route image generation requests to ShortArt for general artwork, product listing imagery, and template-driven visual assets. It helps agents collect parameters, submit generation jobs, poll status, and optionally download completed images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected images are sent to ShortArt for generation. <br>
Mitigation: Use the skill only when ShortArt's terms fit the intended data, and avoid submitting sensitive images or confidential prompts. <br>
Risk: API-key handling and download behavior were flagged for review by the authoritative security evidence. <br>
Mitigation: Do not echo the API key in shared terminals or logs, keep SHORTART_API_KEY scoped to trusted environments, and treat downloaded results cautiously until trusted hosts and paths are confirmed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yige666s/shortart-image-generator) <br>
- [ShortArt](https://shortart.ai) <br>
- [ShortArt API Key Page](https://shortart.ai/key) <br>
- [Text-to-Image Generation](references/text-to-image.md) <br>
- [E-commerce Suit Image Generation](references/suit-image.md) <br>
- [Template-based Image Generation](references/template-image.md) <br>
- [Image Prompt Writing Guide](references/prompt-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON task results, and local image file paths when downloads are requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SHORTART_API_KEY, Python 3.7 or later, and the requests package; generation jobs may require polling before images are available.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
