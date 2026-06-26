## Description: <br>
Create high-converting YouTube thumbnail concepts, overlay text, image prompts, and optional AI-generated cover images from raw titles, hooks, scripts, or marketing copy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LUO-2Q](https://clawhub.ai/user/LUO-2Q) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Creators, marketers, and agent users use this skill to turn YouTube titles, hooks, scripts, or campaign copy into thumbnail angles, short overlay text, Nano Banana image prompts, and optional generated PNG assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Thumbnail titles, scripts, hooks, or marketing copy may be sent to Gemini during planning or image generation. <br>
Mitigation: Avoid including secrets, credentials, or highly confidential unpublished material in prompts. <br>
Risk: Generated PNG and sidecar metadata files may contain shareable prompt or campaign details. <br>
Mitigation: Write outputs to a dedicated directory and review generated files before sharing or committing them. <br>
Risk: Image generation may not render exact overlay text or requested visual details. <br>
Mitigation: Review generated thumbnails and metadata before publication, and revise prompts or overlays when accuracy matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LUO-2Q/youtube-cover-nano-banana) <br>
- [Publishing Contract](artifact/references/publishing-contract.md) <br>
- [YouTube Thumbnail Patterns](artifact/references/youtube-thumbnail-patterns.md) <br>
- [Gemini Generative Language API endpoint](https://generativelanguage.googleapis.com/v1beta/models/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Image files, Guidance] <br>
**Output Format:** [Markdown blocks and structured JSON, with optional PNG image output and sidecar metadata JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The command contract returns angle, overlay_text, prompt, generation_notes, artifact paths, and readable error details.] <br>

## Skill Version(s): <br>
0.1.1 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
