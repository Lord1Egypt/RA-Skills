## Description: <br>
Manage YouTube videos through yutu CLI commands to list, upload, update, delete, rate, get ratings, and report videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OpenWaygate](https://clawhub.ai/user/OpenWaygate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and channel operators use this skill to have an agent prepare yutu CLI commands for listing, uploading, updating, rating, reporting, or deleting YouTube videos after OAuth credentials are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload, modify, rate, report, or delete videos when used with YouTube credentials. <br>
Mitigation: Require explicit confirmation before uploads, public or privacy changes, subscriber notifications, ratings, abuse reports, or deletions. <br>
Risk: OAuth client secrets and cached tokens can grant access to a YouTube account. <br>
Mitigation: Keep client_secret.json and youtube.token.json private, avoid committing them, and restrict local file access. <br>
Risk: The skill depends on the third-party yutu CLI to operate on a YouTube account. <br>
Mitigation: Install and use it only when the publisher and yutu CLI are trusted for the intended account. <br>


## Reference(s): <br>
- [Yutu project homepage](https://github.com/eat-pray-ai/yutu) <br>
- [Yutu README](https://github.com/eat-pray-ai/yutu#readme) <br>
- [Yutu releases](https://github.com/eat-pray-ai/yutu/releases/latest) <br>
- [YouTube Data API v3](https://console.cloud.google.com/apis/api/youtube.googleapis.com/overview) <br>
- [Yutu Setup Guide](references/setup.md) <br>
- [Video Delete](references/video-delete.md) <br>
- [Video GetRating](references/video-getRating.md) <br>
- [Video Insert](references/video-insert.md) <br>
- [Video List](references/video-list.md) <br>
- [Video Rate](references/video-rate.md) <br>
- [Video ReportAbuse](references/video-reportAbuse.md) <br>
- [Video Update](references/video-update.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and command flag tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference JSON, YAML, table, or silent yutu command outputs depending on selected flags.] <br>

## Skill Version(s): <br>
0.10.7-dev (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
