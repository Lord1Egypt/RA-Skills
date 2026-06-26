## Description: <br>
Extract and analyze TikTok content using yt-dlp, including video metadata, captions, sound and music details, user profile data, and engagement stats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuya227939](https://clawhub.ai/user/xuya227939) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, social media analysts, content strategists, and researchers use this skill to extract structured TikTok metadata, captions, comments, profile feeds, hashtag data, and sound usage for content research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser-cookie fallback can expose active browser session data to local tooling. <br>
Mitigation: Do not enable browser-cookie fallback unless the user understands and accepts the session-data exposure risk. <br>
Risk: The skill references an external download service for video download requests. <br>
Mitigation: Use the skill for content extraction and analysis, avoid third-party downloader sites, and only access content the user is allowed to access. <br>
Risk: Security evidence marks the release as suspicious and notes a mismatch between the apparent YouTube transcript focus and the TikTok artifact. <br>
Mitigation: Review the skill before installing and verify that the documented behavior matches the intended TikTok research use case. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xuya227939/tiktok-research-kit) <br>
- [Publisher profile](https://clawhub.ai/user/xuya227939) <br>
- [SnapVee homepage](https://snapvee.com) <br>
- [Support issue tracker](https://github.com/xuya227939/tiktok-research-kit/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with yt-dlp shell commands, JSON field mappings, and formatted analysis tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include parsed TikTok metadata, profile summaries, comments, hashtag results, sound information, error guidance, and prerequisite installation commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md, and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
