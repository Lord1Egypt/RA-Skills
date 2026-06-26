## Description: <br>
Call Vibbit OpenAPI to generate B-roll images, parse Douyin/Xiaohongshu/Bilibili links, break down viral videos, list available avatars, and initialize avatar voiceover workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zgissing](https://clawhub.ai/user/zgissing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to route eligible media-generation, video-analysis, avatar-listing, and avatar voiceover tasks through Vibbit's OpenAPI-backed CLI instead of hand-writing API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation rules may cause matching media-generation or video-analysis requests to use Vibbit by default. <br>
Mitigation: Install only when Vibbit should handle these tasks, and confirm ambiguous user intent before invoking the skill. <br>
Risk: Prompts, media URLs, signed URLs, private media, localhost links, or intranet URLs may be sent to or fetched by Vibbit services. <br>
Mitigation: Avoid confidential inputs and private network URLs unless the user is comfortable sharing or exposing them to Vibbit. <br>
Risk: A custom VIBBIT_BASE_URL can redirect requests and credentials to a nonstandard endpoint. <br>
Mitigation: Keep VIBBIT_BASE_URL pointed at a trusted endpoint and use a scoped Vibbit API key when available. <br>


## Reference(s): <br>
- [Vibbit SKILL on ClawHub](https://clawhub.ai/zgissing/vibbit-skills) <br>
- [Vibbit API Key Management](https://app.vibbit.ai/api-keys) <br>
- [Vibbit OpenAPI Base URL](https://openapi.vibbit.cn) <br>
- [Vibbit File Info API](https://tools.vibbit.ai/api/file-info) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VIBBIT_API_KEY and Node.js 18+; returns media URLs, parsed metadata, avatar lists, or avatar voiceover workflow links through Vibbit APIs.] <br>

## Skill Version(s): <br>
1.0.9 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
