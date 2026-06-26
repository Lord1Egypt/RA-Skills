## Description: <br>
Create, produce, and publish UGC-style short-form video reels at scale using DanSUGC for UGC clips, analytics, and posting; Gemini for video analysis; and ffmpeg for video assembly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielhangan](https://clawhub.ai/user/danielhangan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and growth teams use this skill to guide an agent through short-form UGC reel production, including finding reaction hooks, analyzing demo videos, assembling vertical clips, scoring virality, publishing to connected TikTok and Instagram accounts, and reviewing analytics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can spend DanSUGC credits when purchasing clips or using analytics. <br>
Mitigation: Use limited-balance or test accounts where possible and require manual confirmation before purchase or paid analytics actions. <br>
Risk: The workflow can upload unpublished demos or final videos to third-party services for Gemini processing and temporary public hosting. <br>
Mitigation: Avoid sensitive recordings, review media before upload, and remove temporary hosted files when they are no longer needed. <br>
Risk: The workflow can publish or manage real TikTok and Instagram posts through connected accounts. <br>
Mitigation: Use limited or staging social accounts where possible and manually confirm each upload, schedule, publish, or delete action. <br>
Risk: The preflight behavior includes package installation commands that may request elevated privileges. <br>
Mitigation: Do not run sudo or package-install preflight steps automatically; review and execute dependency installation separately. <br>


## Reference(s): <br>
- [ReelClaw homepage](https://github.com/dansugc/reelclaw) <br>
- [DanSUGC API docs](https://dansugc.com/llms.txt) <br>
- [DanSUGC interactive docs](https://dansugc.com/docs) <br>
- [DanSUGC dashboard](https://dansugc.com/dashboard) <br>
- [Gemini API key setup](https://aistudio.google.com/apikey) <br>
- [Tool setup reference](artifact/tools-setup.md) <br>
- [FFmpeg patterns reference](artifact/ffmpeg-patterns.md) <br>
- [Green zone reference](artifact/green-zone.md) <br>
- [Virality scoring reference](artifact/virality-scoring.md) <br>
- [Virality reference](artifact/virality.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands, API calls, JSON examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce video-editing command plans, publishing instructions, virality analysis, and social caption guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
