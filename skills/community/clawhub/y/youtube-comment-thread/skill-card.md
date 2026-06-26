## Description: <br>
Manage YouTube comment threads by helping agents list existing threads or insert new top-level comments through the yutu CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OpenWaygate](https://clawhub.ai/user/OpenWaygate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage YouTube comment thread workflows from an agent, including setup, listing threads, and posting top-level comments with OAuth-backed yutu credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish YouTube comments using the user's OAuth account and does not clearly require final confirmation before posting. <br>
Mitigation: Before any insert command, require explicit approval after showing the video ID, channel ID, author channel, and full comment text. <br>
Risk: OAuth client secrets and cached tokens can grant access to the user's YouTube account if exposed. <br>
Mitigation: Keep client_secret.json and youtube.token.json private and out of version control, and revoke the OAuth token if exposure is suspected or the skill is no longer used. <br>


## Reference(s): <br>
- [Yutu Setup Guide](references/setup.md) <br>
- [Comment Thread Insert](references/commentThread-insert.md) <br>
- [Comment Thread List](references/commentThread-list.md) <br>
- [yutu project homepage](https://github.com/eat-pray-ai/yutu) <br>
- [yutu README](https://github.com/eat-pray-ai/yutu#readme) <br>
- [YouTube Data API v3](https://console.cloud.google.com/apis/api/youtube.googleapis.com/overview) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and command reference tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The yutu CLI can return table, JSON, YAML, or silent output depending on command flags.] <br>

## Skill Version(s): <br>
0.10.7-dev (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
