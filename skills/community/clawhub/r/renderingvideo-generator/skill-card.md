## Description: <br>
RenderingVideo preview assistant that helps agents draft or edit RenderingVideo schema JSON, validate it through the public preview flow without an API key, and return the preview URL and temporary identifier. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gljhint](https://clawhub.ai/user/gljhint) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create or edit RenderingVideo JSON schemas, submit them to the public preview endpoint, and report temporary preview links and validation feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: RenderingVideo schema JSON is uploaded to video.renderingvideo.com and may result in a temporary shareable preview link. <br>
Mitigation: Use only content intended for external processing; avoid secrets, tokens, customer data, private media, proprietary scripts, and internal URLs. <br>


## Reference(s): <br>
- [RenderingVideo API and Usage](https://renderingvideo.com/docs/api-and-usage.md) <br>
- [RenderingVideo JSON Spec](https://renderingvideo.com/docs/json-spec.md) <br>
- [RenderingVideo Clips](https://renderingvideo.com/docs/clips.md) <br>
- [RenderingVideo Elements](https://renderingvideo.com/docs/elements.md) <br>
- [RenderingVideo Base Clip](https://renderingvideo.com/docs/elements/base-clip.md) <br>
- [RenderingVideo Animation and Timing](https://renderingvideo.com/docs/animation-and-timing.md) <br>
- [ClawHub Release Page](https://clawhub.ai/gljhint/renderingvideo-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with JSON schema content, shell commands, preview URLs, temporary identifiers, and validation details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns tempId, viewerUrl, url, and expiresIn when present; generated preview links are temporary and expire after 7 days.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
