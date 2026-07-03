## Description: <br>
Converts Markdown into WeChat Official Account HTML and helps agents inspect metadata, themes, images, styles, AI-trace handling, and draft or image-post readiness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerryxn](https://clawhub.ai/user/jerryxn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to prepare Markdown articles for WeChat Official Account workflows, including HTML conversion, preview and readiness inspection, cover or infographic generation, draft creation, and image-post routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WeChat draft credentials and account-bound upload actions can expose or modify a WeChat Official Account workflow. <br>
Mitigation: Validate configuration before draft or image-post actions, keep WECHAT_APPID and WECHAT_SECRET private, and run upload or draft creation only after an explicit user request. <br>
Risk: AI-trace removal, creator-style writing, and aggressive humanizing can obscure authorship or make content-transparency claims misleading. <br>
Mitigation: Review generated or humanized text for truthful authorship and attribution, and do not use these features to misrepresent who wrote the content. <br>
Risk: Remote image downloads, external image generation, and media uploads can send content to third-party services or WeChat. <br>
Mitigation: Use inspect and local preview first, confirm image sources and service configuration, and avoid remote generation or upload unless requested. <br>
Risk: Draft shortcuts and smoke-test flows may not provide the formal title, author, digest, cover, and content checks needed before release. <br>
Mitigation: Use the inspect, preview, upload_image, create_draft, and draft verification flow before relying on a WeChat draft for publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jerryxn/skills/zm-md2wechat-conversion-tool) <br>
- [Go module install source](https://github.com/geekjourneyx/zm-md2wechat-conversion-tool-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with CLI command examples, JSON configuration references, and workflow status labels.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local HTML previews, draft JSON inputs, uploaded WeChat draft or image-post actions, generated images, and PASS/NEEDS_REVISION/BLOCKED status when the CLI workflow is executed.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
