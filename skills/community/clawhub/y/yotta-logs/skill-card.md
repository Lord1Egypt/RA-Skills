## Description:

元史 searches local agent conversation and memory logs across common formats to retrieve past discussions, session context, and source details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yottameta](https://clawhub.ai/user/yottameta)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users can use the skill to find earlier decisions, statements, and discussion context in their local session or memory files, then inspect the matching excerpts and source details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A search intended to cover conversations only can also include private memories.

Mitigation: Constrain searches with an explicit --dir or --source, or use --kind session; do not rely on default_scope to exclude sources. Treat retrieved excerpts as sensitive because redaction may not remove every secret.

## Reference(s):

- [Security and privacy guidance](references/security.md)
- [CLI reference](references/cli.md)
- [Supported agent log formats](references/agent-formats.md)
- [GitHub project](https://github.com/YottaMeta/yotta-logs)
- [npm package](https://www.npmjs.com/package/@yottameta/yotta-logs)
- [ClawHub skill page](https://clawhub.ai/yottameta/skills/yotta-logs)

## Skill Output:

**Output Type(s):** [Text, JSON, Analysis]

**Output Format:** [Search excerpts, session timelines, source details, and usage statistics in readable text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retrieved excerpts may contain private conversation or memory content; output is redacted by default, but redaction may not remove every secret.]

## Skill Version(s):

0.3.5 (source: frontmatter, CHANGELOG, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
