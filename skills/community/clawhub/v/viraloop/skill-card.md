## Description: <br>
Viraloop is an OpenClaw agent skill that analyzes a website, generates TikTok and Instagram carousel slides, publishes them through Upload-Post, and uses analytics feedback to improve future posts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mutonby](https://clawhub.ai/user/mutonby) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, and developers use this skill to turn a public product website into a daily TikTok and Instagram carousel workflow with generated slides, publishing, analytics collection, and iterative content recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish public TikTok and Instagram posts without human review. <br>
Mitigation: Add a human approval step before publishing or use test accounts until content and account controls are reviewed. <br>
Risk: The skill is designed to continue optimizing future automated runs. <br>
Mitigation: Disable or tightly control cron and self-scheduling behavior so posting cadence remains operator-approved. <br>
Risk: Upload-Post credentials can enable publishing and analytics access for connected social accounts. <br>
Mitigation: Scope, rotate, and store the Upload-Post token only in the execution environment. <br>
Risk: Website analysis and generated analytics artifacts may include business or campaign information. <br>
Mitigation: Analyze only public, non-sensitive websites and store generated content and analytics in a private directory with deletion rules. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mutonby/viraloop) <br>
- [Google AI Studio API Keys](https://aistudio.google.com/app/apikey) <br>
- [Upload-Post](https://upload-post.com) <br>
- [Upload-Post Upload Photo API](https://docs.upload-post.com/api/upload-photo) <br>
- [Upload-Post Analytics API](https://docs.upload-post.com/api/get-analytics) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands plus generated JSON, JPG, caption, analytics, and learning files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a six-slide vertical carousel, caption text, local analysis and learning files, and post metadata for TikTok and Instagram publishing.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
