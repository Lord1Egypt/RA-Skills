## Description:

Provides TikHub-powered workflows for retrieving multi-platform video data, comments, creator information, download links, and Douyin transcription outputs across Douyin, TikTok, Bilibili, YouTube, Xiaohongshu, Weibo, and Kuaishou.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kk-kingkong](https://clawhub.ai/user/kk-kingkong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content workflow operators use this skill to call TikHub MCP or SDK flows for collecting social-video metadata, comments, subtitles, download URLs, and transcripts. It is intended for workflows that require explicit TikHub credentials and attention to provider costs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use local TikHub credentials automatically.

Mitigation: Configure credentials explicitly in a dedicated environment and avoid relying on local .env scraping.

Risk: Media downloads and arbitrary video URLs cross the TikHub provider trust boundary.

Mitigation: Review the TikHub provider before use, validate or constrain input URLs, and restrict outputs to a chosen download directory.

Risk: TikHub API calls may incur provider costs.

Mitigation: Monitor account balance, reuse cached results when available, and set request limits for batch workflows.

Risk: The CPU background Whisper path has unsafe shell and nohup handling in the scanned evidence.

Mitigation: Do not use the CPU background transcription path until command handling is fixed; prefer reviewed synchronous execution or the GPU path in a controlled environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kk-kingkong/skills/tikhub-api-skill-kk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands, Python snippets, JSON data, and local media or transcript files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call TikHub APIs, download media files, create JSON result files, and write transcript text files.]

## Skill Version(s):

1.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
