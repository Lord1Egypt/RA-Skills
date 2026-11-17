## Description:

Generates structured Chinese Xiaohongshu draft posts from pdf, md, txt, or json inputs, with v1 focused on paper-interpretation posts and local Markdown and JSON outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chen-li-17](https://clawhub.ai/user/chen-li-17)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, and researchers use this skill to turn source documents into Xiaohongshu-ready Chinese draft posts while preserving source-grounded evidence notes. It is especially suited to paper interpretation drafts that need titles, body sections, hashtags, and structured JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes xhs-post.md and xhs-post.json next to the input file, which may place generated drafts in sensitive or synced folders.

Mitigation: Run it in an intended working directory and review or move generated draft files before sharing or syncing.

Risk: Generated Xiaohongshu copy may still need editorial review before public posting.

Mitigation: Review titles, claims, hashtags, and evidence notes against the source document before publishing.

Risk: When source material lacks enough detail, the draft can contain explicit information-gap notes.

Mitigation: Provide complete source documents or keep the skill's required missing-information disclosures in the final draft.

## Reference(s):

- [Xhs Post Factory ClawHub Page](https://clawhub.ai/chen-li-17/skills/xhs-post-factory)
- [paper-interpretation template](templates/paper-interpretation.md)
- [XHS Writing Style Guide](references/style-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown draft plus structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes xhs-post.md and xhs-post.json next to the input source; v1 defaults to paper-interpretation with configurable length and emoji density.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
