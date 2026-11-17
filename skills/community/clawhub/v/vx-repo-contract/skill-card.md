## Description:

Guides agents applying the shared repository layout contract to vx-managed repositories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loonghao](https://clawhub.ai/user/loonghao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and repository-maintaining agents use this skill to check and align vx-managed repository layouts, task entry points, and agent instructions with the shared contract.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloning and running external repository-checking tooling can execute code from outside the target repository.

Mitigation: Inspect the tooling and confirm its pinned revision before running the checker.

Risk: Repository layout changes or a public issue status comment may have unintended effects or expose sensitive details.

Mitigation: Review proposed changes and the issue target; omit private paths and identifiers from public comments.

## Reference(s):

- [Shared repository contract](https://github.com/dcc-mcp/.github/blob/main/contract/repo_contract.json)
- [vx-repo-contract on ClawHub](https://clawhub.ai/loonghao/skills/vx-repo-contract)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with command and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance for baseline and strict repository checks.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
