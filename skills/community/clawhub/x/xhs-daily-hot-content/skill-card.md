## Description:

Generates Xiaohongshu marketing drafts by searching current public trends, focusing on AI education and parenting topics, and prepending new entries to a local YAML content library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangcongwangcong](https://clawhub.ai/user/wangcongwangcong)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators, creators, and marketing teams use this skill to turn current public trends into Xiaohongshu-style draft posts for AI education and parenting audiences. It can update a local `templates/posts.yaml` content library and optionally guide cover-card generation when a project generator is present.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill searches current public trends, so generated marketing drafts may reflect incomplete, outdated, or low-quality search results.

Mitigation: Review the selected topics, cited trend basis, and final copy before publication.

Risk: The skill can write to `templates/posts.yaml`, which may change a local content library.

Mitigation: Confirm whether the run should only draft text or also write files, and review the file diff before using the updated library.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangcongwangcong/skills/xhs-daily-hot-content)
- [ClawHub publisher profile](https://clawhub.ai/user/wangcongwangcong)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown report with YAML content entries and optional inline code guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write or update `templates/posts.yaml`; optional cover generation depends on local project files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
