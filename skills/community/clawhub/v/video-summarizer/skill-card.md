## Description: <br>
Converts Bilibili, YouTube, Xiaohongshu, and Douyin videos into structured Notion-ready summaries with configurable AI analysis, screenshots, and OSS uploads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajayhao](https://clawhub.ai/user/ajayhao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content teams use this skill to turn supported video URLs into structured Markdown summaries, key concepts, timestamps, screenshots, and optional Notion database records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can send video transcripts and metadata to the configured LLM provider and can upload screenshots or cover images to Aliyun OSS. <br>
Mitigation: Use dedicated low-privilege API keys, restrict OSS bucket permissions, and avoid processing confidential videos. <br>
Risk: Server security evidence reports that summaries may be pushed to Notion whenever Notion credentials are present, even without the documented push option. <br>
Mitigation: Remove Notion credentials unless automatic archiving is intended, or patch the workflow so Notion upload only runs when an explicit push option is supplied. <br>
Risk: Bilibili subtitle access can use session cookies stored on the local machine. <br>
Mitigation: Use Bilibili cookies only on controlled devices, keep file permissions restrictive, and delete the cookies when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ajayhao/video-summarizer) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Release changelog](artifact/CHANGELOG.md) <br>
- [Quick start README](artifact/README.md) <br>
- [Summary template documentation](artifact/templates/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration] <br>
**Output Format:** [Markdown summaries with JSON analysis files, transcript text, screenshot URL lists, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can upload screenshots to Aliyun OSS and can write summaries to Notion when credentials are configured.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release metadata, changelog, and artifact documentation; released 2026-05-10) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
