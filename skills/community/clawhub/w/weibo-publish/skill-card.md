## Description:

Publish text and image posts to Weibo (m.weibo.cn) using browser automation, including text-only posts, image posts, and automated publishing workflows that use an existing browser login session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noah-1106](https://clawhub.ai/user/noah-1106)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to publish text and image content to a logged-in Weibo account through browser automation while verifying the published post afterward.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can post publicly through the currently logged-in Weibo browser session.

Mitigation: Use it only for the intended Weibo account and require explicit approval before the agent clicks send.

Risk: The skill includes cleanup commands that may be unsafe if run with wildcard or placeholder paths.

Mitigation: Delete only verified temporary upload files with exact paths, and avoid broad cleanup commands.

Risk: The compose page may remain open after publishing and can create accidental duplicate-post risk.

Mitigation: Verify the latest post on the personal page after publishing, then close the compose tab.

## Reference(s):

- [Workflow Examples](references/workflow-examples.md)
- [ClawHub Skill Page](https://clawhub.ai/noah-1106/skills/weibo-publish)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code]

**Output Format:** [Markdown instructions with browser automation examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an existing Weibo browser login session, manual verification after posting, and known temporary upload file paths for cleanup.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
