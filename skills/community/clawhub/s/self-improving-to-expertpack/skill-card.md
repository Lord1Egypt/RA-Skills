## Description:

Converts Self-Improving Agent learning logs and promoted workspace guidance into an Obsidian-compatible ExpertPack with a manifest, overview, categorized Markdown files, indexes, glossary, and relationship metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brianhearn](https://clawhub.ai/user/brianhearn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to migrate accumulated Self-Improving Agent learnings, errors, feature requests, and promoted guidance into a portable ExpertPack for review, reuse, and publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated packs may include private or organization-specific workspace instruction content, especially promoted guidance copied into mind/promoted-rules.md.

Mitigation: Run the converter only on workspaces intended for export, review generated content carefully before committing or publishing, and pay particular attention to promoted-rules.md.

Risk: The release evidence says the skill overstates its secret-stripping protections before encouraging publication.

Mitigation: Do not rely on built-in redaction as the only control; run an independent secret scan and manually inspect generated Markdown and YAML before sharing the pack.

## Reference(s):

- [ExpertPack](https://expertpack.ai)
- [ClawHub skill page](https://clawhub.ai/brianhearn/skills/self-improving-to-expertpack)
- [ClawHub ExpertPack skill](https://clawhub.com/skills/expertpack)

## Skill Output:

**Output Type(s):** [markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown and YAML files in an ExpertPack directory, plus terminal status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; reads .learnings files and selected workspace instruction files; generated packs should be reviewed before publishing.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
