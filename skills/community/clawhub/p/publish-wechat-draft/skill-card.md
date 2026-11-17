## Description:

Publishes articles to a WeChat Official Account draft box using the weixingongzhonghao-publisher CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lixinran2015](https://clawhub.ai/user/lixinran2015)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to prepare article input, check the required publisher project and dependencies, guide WeChat login when needed, and create WeChat Official Account drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may run mutable third-party npm code that can access the local environment and WeChat publishing session.

Mitigation: Use only a trusted, pinned copy of the referenced project and dependencies, run it in a restricted workspace or container, and require confirmation before installation, login, file writes, or draft creation.

Risk: The workflow uses WeChat account session cookies with limited scoping safeguards.

Mitigation: Do not read or expose cookie contents, keep cookie files out of git, require user-controlled login, and stop if the user declines authentication.

## Reference(s):

- [weixingongzhonghao GitHub project](https://github.com/lixinran2015/weixingongzhonghao)
- [ClawHub skill page](https://clawhub.ai/lixinran2015/skills/publish-wechat-draft)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional generated article files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create temporary HTML article files and report publish results, draft links, errors, and suggested next steps.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
