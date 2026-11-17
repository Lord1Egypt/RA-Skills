## Description:

Archives Weibo posts from t.cn or weibo.com links by expanding links, capturing post text and images, saving Obsidian Markdown, and optionally syncing to Feishu, Notion, or a generated Sprout note.

This skill is ready for commercial/non-commercial use.

## Publisher:

[violin86318](https://clawhub.ai/user/violin86318)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal knowledge-management users use this skill to archive Weibo posts and images into an organized Obsidian folder, with optional Feishu, Notion, and Sprout-note workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses browser automation to read Weibo pages and persist copied content and images locally.

Mitigation: Run it only on validated Weibo post URLs and save archives to an intended local Obsidian directory.

Risk: Configured Feishu or Notion credentials can transmit archived content, images, and author metadata to third-party services.

Mitigation: Leave external sync credentials unset for local-only use and enable them only for destinations where the content is intended to be uploaded.

Risk: Using an existing browser profile may expose sensitive authenticated sessions during page capture.

Mitigation: Use a separate browser profile with only the sessions needed for Weibo archiving.

Risk: The skill explicitly works around image-fetching network blocks.

Mitigation: Review image capture behavior before use in restricted environments and stop execution when page or image sources are unexpected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/violin86318/skills/weibo-save)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files with YAML frontmatter, local image files, optional Feishu or Notion records, optional Sprout-note Markdown, and a concise status response.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided local paths and optional Feishu, Notion, and browser-profile configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
