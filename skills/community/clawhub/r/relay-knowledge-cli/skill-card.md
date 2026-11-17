## Description:

Guides agents in using the local relay-knowledge CLI to index repositories, maintain CodeSpec and Knowledge maps, query code and business relationships, and assess changes after commits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevetdp](https://clawhub.ai/user/stevetdp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use the skill to build and query local repository knowledge maps, inspect code and business context at a pinned revision, and update maps and impact analysis after commits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository indexing and map updates may access or change local project data.

Mitigation: Restrict use to repositories you authorize and review map changes.

Risk: Installing an unverified CLI could execute untrusted software.

Mitigation: Prefer verified published installs and check the executable before use.

Risk: Feedback auto-submit or persistent local service operation may have unintended effects.

Mitigation: Enable publication or persistence only when intentionally authorized.

## Reference(s):

- [ClawHub release](https://clawhub.ai/stevetdp/skills/relay-knowledge-cli)
- [Project homepage (listed in release metadata)](https://github.com/coolplayagent/relay-knowledge)
- [CLI workflows](artifact/references/cli-workflows.md)
- [Knowledge map workflows](artifact/references/knowledge-map-workflows.md)
- [Feedback workflows](artifact/references/feedback-workflows.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with CLI examples; CLI responses can be JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Repository results depend on the indexed snapshot and selected revision.]

## Skill Version(s):

1.1.22 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
