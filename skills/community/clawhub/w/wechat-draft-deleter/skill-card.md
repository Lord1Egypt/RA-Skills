## Description:

Deletes WeChat Official Account drafts by Media ID, including single-item, comma-separated batch, and file-based batch deletion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bigkingcn](https://clawhub.ai/user/bigkingcn)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and WeChat Official Account operators use this skill to clean test drafts, remove old draft versions, and automate bulk draft cleanup through the WeChat draft deletion API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs destructive WeChat draft deletion that may be irreversible.

Mitigation: Run only against Media IDs that are backed up or confirmed for removal, and test the workflow before using it on important drafts.

Risk: Evidence security guidance reports real-looking credentials in examples.

Mitigation: Replace example credentials with placeholders and rotate any credentials that may have been exposed.

Risk: Evidence security guidance flags installer and dependency behavior that needs review.

Mitigation: Avoid elevated privileges during installation and prefer a virtual environment with pinned Python dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bigkingcn/skills/wechat-draft-deleter)
- [WeChat draft delete API endpoint](https://api.weixin.qq.com/cgi-bin/draft/delete)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and CLI arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes credential setup guidance, Media ID input options, confirmation behavior, and deletion result summaries.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
