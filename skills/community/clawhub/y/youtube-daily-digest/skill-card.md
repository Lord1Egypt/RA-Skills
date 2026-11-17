## Description:

YouTube Daily Digest fetches recent videos from selected AI, product, and technology YouTube channels, summarizes available transcripts in Chinese through OpenClaw Gateway, and posts a Feishu card digest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jadeyang7458-byte](https://clawhub.ai/user/jadeyang7458-byte)

### License/Terms of Use:

MIT-0

## Use Case:

External users or teams who follow AI, product, and technology podcasts use this skill to receive a Chinese-language Feishu digest of newly published YouTube videos. It is intended for scheduled or manual runs in an OpenClaw environment with Feishu messaging configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports apparent plaintext Feishu and OpenClaw credentials in the package.

Mitigation: Remove and rotate exposed credentials before installing, publishing, or running the skill.

Risk: Transcript text is sent through the configured OpenClaw Gateway/Claude service and the resulting digest is posted to Feishu.

Mitigation: Confirm the configured model gateway and Feishu workspace are approved for the transcript content being processed.

Risk: The security guidance notes weak local-secret scoping and recipient configuration concerns.

Mitigation: Use a virtual environment with pinned dependencies and provide the Feishu recipient explicitly at runtime.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jadeyang7458-byte/skills/youtube-daily-digest)
- [Publisher Profile](https://clawhub.ai/user/jadeyang7458-byte)
- [Setup Guide](references/setup.md)
- [Google Takeout](https://takeout.google.com)
- [YouTube Atom Feed Pattern](https://www.youtube.com/feeds/videos.xml?channel_id=UC频道ID)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Feishu interactive card content with Chinese text summaries and Markdown-style links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries are generated from available YouTube transcript text and posted to a configured Feishu recipient.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
