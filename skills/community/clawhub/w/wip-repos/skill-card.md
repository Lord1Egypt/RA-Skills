## Description:

Repo manifest reconciler. Makes repos-manifest.json the single source of truth for repo organization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to check repository layout drift against repos-manifest.json, plan or apply local repo moves, edit manifest entries, and generate manifest-based repository trees.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sync and compliance workflows can move folders or write files beyond what a user expects.

Mitigation: Run check and sync --dry-run before applying changes, review planned moves and diffs, and operate only on trusted manifests and repositories.

Risk: Path containment and CLAUDE.md metadata handling are not fully resolved for third-party or mixed-ownership repo sets.

Mitigation: Avoid compliance --fix and claude workflows on those repo sets until the boundary and metadata handling issues are fixed and reviewed.

Risk: The security scan verdict is suspicious despite the skill's coherent repo-organization purpose.

Mitigation: Treat installation as trust-sensitive, review the artifact before deployment, and restrict use to repository sets the operator controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/parkertoddbrooks/skills/wip-repos)
- [Publisher profile](https://clawhub.ai/user/parkertoddbrooks)
- [Project homepage](https://github.com/wipcomputer/wip-ai-devops-toolbox)
- [npm package](https://www.npmjs.com/package/@wipcomputer/wip-repos)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Plain text, JSON, and Markdown tree output; CLI and MCP calls may also update manifest and repository files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and git. Commands that change files should be previewed with dry-run or planning modes first.]

## Skill Version(s):

1.9.72 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
