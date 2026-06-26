## Description: <br>
Extract and analyze Xiaohongshu (Little Red Book) content using yt-dlp and gallery-dl, including note metadata, image and video extraction, user profile analysis, and content research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuya227939](https://clawhub.ai/user/xuya227939) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, researchers, and content analysts use this skill to inspect Xiaohongshu notes, profiles, and topic pages with local yt-dlp and gallery-dl commands, then summarize extracted metadata and engagement data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to use browser login cookies for Xiaohongshu content access. <br>
Mitigation: Review before installing, approve any command that reads browser cookies, and prefer a dedicated browser profile or site-limited cookie file. <br>
Risk: The skill relies on local yt-dlp and gallery-dl tooling to access user-selected Xiaohongshu URLs. <br>
Mitigation: Install yt-dlp and gallery-dl only from trusted sources and review generated shell commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xuya227939/xiaohongshu-research-kit) <br>
- [Publisher profile](https://clawhub.ai/user/xuya227939) <br>
- [Support issues](https://github.com/xuya227939/xiaohongshu-research-kit/issues) <br>
- [SnapVee](https://snapvee.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured result tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include parsed metadata fields, engagement statistics, image or video URLs, and short follow-up analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
