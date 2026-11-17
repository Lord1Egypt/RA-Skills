## Description:

Provides quality rules that guide agents to analyze complex tasks before acting, state uncertainty, and self-check results; it does not execute code or take over tool permissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yottameta](https://clawhub.ai/user/yottameta)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users can apply the skill to complex analysis, troubleshooting, writing, and implementation tasks that benefit from careful reasoning. It guides the agent to explain uncertainty and review its work while leaving execution and human review to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reinstalling the skill can replace local skill files, and a global install can affect multiple agent directories.

Mitigation: Review the files or use an exact package version, preview with --dry-run, install to one selected agent or directory, and back up local edits before reinstalling.

## Reference(s):

- [FAQ](references/faq.md)
- [Complex-task walkthroughs](references/walkthroughs.md)
- [Project homepage](https://github.com/YottaMeta/yotta-anti-shallow)
- [ClawHub release](https://clawhub.ai/yottameta/skills/yotta-anti-shallow)
- [npm package](https://www.npmjs.com/package/@yottameta/yotta-anti-shallow)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Text, Markdown]

**Output Format:** [Text and Markdown responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance for reasoning and self-checking; no code execution or external tool calls, and not a replacement for tests or human review.]

## Skill Version(s):

1.4.4 (source: frontmatter, package.json, CHANGELOG; released 2026-11-05)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
