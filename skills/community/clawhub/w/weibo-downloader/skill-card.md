## Description:

Downloads Weibo images and videos from standard, mobile, and fx share links using Python requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[belingud](https://clawhub.ai/user/belingud)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to download media from individual Weibo posts or batches of Weibo links into local image and video files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Weibo and creates visitor session cookies that may persist locally for about a year.

Mitigation: Use the skill only in an environment where Weibo access and local cookie persistence are acceptable; keep the skill directory private.

Risk: Stored cookies are auto-loaded from an unsafe serialized format.

Mitigation: Do not use cookie files from other users or untrusted sources; prefer a reviewed version that stores cookies as JSON with restrictive file permissions.

Risk: Batch mode can process untrusted URL lists and fx share links.

Mitigation: Review batch input before running the skill and validate fx links before downloading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/belingud/skills/weibo-downloader)
- [ClawHub publisher profile](https://clawhub.ai/user/belingud)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands; executed scripts write local image and video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads are organized by Weibo author and status ID when the script is run.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
