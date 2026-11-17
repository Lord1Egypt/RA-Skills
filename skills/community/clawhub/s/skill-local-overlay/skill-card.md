## Description:

Guides agents in preserving local edits to marketplace, connector, and built-in skills with snapshots, a patch ledger, and replay after upgrades.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to preserve local changes to marketplace, connector, and built-in skills across upgrades. It guides them to snapshot files, record each change in a patch ledger, and replay patches after upgrades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security analysis was partial because a local path-like reference could not be resolved.

Mitigation: Check whether the unresolved reference is relevant before installing, and review patches before replaying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haiyangchenbj/skills/skill-local-overlay)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Files]

**Output Format:** [Step-by-step instructions and Markdown patch ledger entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill directs snapshotting, patching, and replaying local skill files.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
