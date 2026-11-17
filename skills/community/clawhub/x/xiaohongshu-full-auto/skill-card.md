## Description:

Automates Xiaohongshu content workflows from hot-topic discovery through topic matching, copy and cover generation, publishing, and publication logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guanlansss](https://clawhub.ai/user/guanlansss)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, bloggers, and content studios use this skill to generate and optionally publish batches of Xiaohongshu posts based on hot topics and configured content niches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks for a Xiaohongshu cookie that may allow account access and posting.

Mitigation: Use draft or semi-automatic mode, limit credential scope where possible, and provide real cookies only after reviewing the workflow and account impact.

Risk: The workflow can publish generated content automatically.

Mitigation: Require human review before publication and verify generated titles, body text, tags, cover images, and target account settings.

Risk: The hot-topic source is a third-party endpoint whose reliability and data handling are not clearly bounded.

Mitigation: Approve or replace the hot-topic source before production use and pin or review dependencies before installation.

Risk: Publication logs are written locally without a clearly documented project-owned output directory.

Mitigation: Move logs to an approved project output path and avoid recording secrets or sensitive account details.

## Reference(s):

- [Configuration example](references/config-example.yaml)
- [Xiaohongshu Open Platform](https://www.xiaohongshu.com/developer)
- [xiaohongshu-mcp](https://github.com/openclaw/skills/tree/main/skills/pxfeng/xiaohongshu-mcp)
- [ClawHub release page](https://clawhub.ai/guanlansss/skills/xiaohongshu-full-auto)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline commands, generated social-media copy, image paths, publication status, and JSONL publication logs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call external topic, image-generation, and publishing services when configured.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
