## Description: <br>
Give OpenClaw the ability to access social media content by searching TikTok, Instagram, and YouTube videos, retrieving metadata and creator profiles, and extracting insights from video content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[veedcrawl](https://clawhub.ai/user/veedcrawl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover public social video content, inspect creator profiles and video metadata, request transcripts, and produce structured research notes or analysis from supported platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Social-media search terms, usernames, video URLs, transcripts, prompts, and extraction results may be sent to the Veedcrawl external service. <br>
Mitigation: Use the skill only when third-party processing is acceptable, and avoid confidential investigations or private content. <br>
Risk: The skill requires a sensitive Veedcrawl API key. <br>
Mitigation: Provide the key through the VEEDCRAWL_API_KEY environment variable and avoid exposing it in prompts, logs, examples, or committed files. <br>


## Reference(s): <br>
- [Veedcrawl Documentation](https://docs.veedcrawl.com) <br>
- [Veedcrawl OpenAPI Specification](https://veedcrawl.com/openapi.json) <br>
- [Veed Crawl on ClawHub](https://clawhub.ai/veedcrawl/veedcrawl) <br>
- [Veedcrawl Publisher Profile](https://clawhub.ai/user/veedcrawl) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks, structured tables, or JSON summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should preserve video URLs, platform, creator identity, timestamps, and whether findings came from metadata, transcript, or extraction evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
