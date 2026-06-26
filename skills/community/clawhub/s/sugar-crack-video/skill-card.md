## Description: <br>
Generates vertical sugar-shell crack and pour dessert videos through WeryAI from text prompts or public image URLs, with prompt expansion and confirmation before paid generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agent users use this skill to generate short food-ASMR dessert videos with sugar-shell cracking, lava pour, jelly wobble, or shell-snap effects. It supports text-to-video and image-to-video workflows through WeryAI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid WeryAI generation requires WERYAI_API_KEY and can consume credits. <br>
Mitigation: Keep the API key secret, review the bundled script before use, and require user confirmation of the full prompt and parameters before each generation. <br>
Risk: Image-to-video requests may upload local image files if a local path is intentionally used. <br>
Mitigation: Prefer public HTTPS image URLs; use local paths only after explicit user consent and review of the upload behavior. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zoucdr/sugar-crack-video) <br>
- [WeryAI video CLI and JSON reference](resources/WERYAI_VIDEO_API.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON command payloads and video URL summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses WERYAI_API_KEY, Node.js 18+, network access, paid WeryAI generation, and public HTTPS image URLs for normal image-to-video use.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
