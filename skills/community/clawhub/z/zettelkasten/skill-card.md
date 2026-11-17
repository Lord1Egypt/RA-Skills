## Description:

Zettelkasten captures ideas as structured note cards and provides tags, AI-style insights, extension suggestions, connection prompts, and daily review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rainy-cogmet](https://clawhub.ai/user/rainy-cogmet)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to capture personal ideas as Zettelkasten cards, generate related tags and suggestions, find connections among stored notes, and review prior cards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists notes in local JSON files with weak file scoping.

Mitigation: Store note databases in a dedicated protected directory and sanitize or hash user IDs before broader deployment.

Risk: The included publishing helper can package the current directory broadly and reads a local credential file for upload.

Mitigation: Do not run publish.sh from directories containing private files; publish from an explicit allowlist package and avoid raw credentials in upload scripts.

Risk: Runtime commands are primarily Chinese, which can cause mistaken use for English-only operators.

Mitigation: Confirm the supported commands, including "记录灵感：", "每日回顾", and "统计", before using the skill in an agent workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rainy-cogmet/skills/zettelkasten)
- [README.en.md](artifact/README.en.md)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown note cards with plain-text prompts and summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local JSON note records and returns generated card content, related-card prompts, daily review text, or note counts.]

## Skill Version(s):

1.0.0 (source: server release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
