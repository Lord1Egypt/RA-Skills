## Description:

Publishes text posts to Weibo (Sina Weibo) with emoji, hashtags, and mentions through browser automation using a managed browser profile.

This skill is ready for commercial/non-commercial use.

## Publisher:

[azfliao](https://clawhub.ai/user/azfliao)

### License/Terms of Use:


## Use Case:

External users and developers use this skill when they want an agent to draft and publish text content to a logged-in Weibo account through browser automation. It is intended for posts that may include Chinese text, emoji, hashtags, mentions, and line breaks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish to a real Weibo account, creating reputational, policy, or account-impacting consequences.

Mitigation: Require explicit user confirmation before every send action and verify the intended account, content, and timing before publishing.

Risk: Saved browser snapshots and weibo-state.json can contain account details or post content.

Mitigation: Treat local state and snapshots as sensitive, minimize stored content, and restrict access to the workspace where they are stored.

Risk: Unattended or scheduled posting can publish content without adequate review.

Mitigation: Avoid unattended or hourly posting workflows unless a human approval step is enforced for each post.

Risk: The optional Python script defines a posting workflow and updates state, but it does not prove that Weibo accepted or displayed the post.

Mitigation: Verify publication in the browser or profile timeline before reporting success or updating posting history.

Risk: Changing page element references and JSON quoting issues can cause failed or unintended browser actions.

Mitigation: Take fresh browser snapshots before each action and use the documented Unicode escaping approach for Chinese content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/azfliao/skills/weibo-publisher)
- [Weibo Publishing Quick Reference](QUICK_REFERENCE.md)
- [Weibo Publishing Examples](references/EXAMPLES.md)
- [Weibo Publisher Troubleshooting](references/TROUBLESHOOTING.md)
- [Unicode Escape Guide for Weibo Publishing](references/UNICODE_ESCAPE.md)
- [Weibo Homepage](https://weibo.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline browser actions, Python snippets, JSON state examples, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include content-preparation steps, browser action sequences, verification guidance, and local state-tracking instructions.]

## Skill Version(s):

2.0.0 (source: ClawHub release metadata and CHANGELOG.md, released 2026-03-02)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
