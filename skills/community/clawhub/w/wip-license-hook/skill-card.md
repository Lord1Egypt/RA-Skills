## Description:

License rug-pull detection. Scans dependencies and forks for license changes, gates upstream merges, maintains a license ledger, and generates a public compliance dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to monitor dependency and fork license changes, gate upstream merges, maintain a license ledger, and generate compliance reports or dashboards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Git-hook installation can persist behavior in a repository and may overwrite existing hooks.

Mitigation: Review the hook scripts first, back up .git/hooks, and avoid running the installer until overwrite behavior is confirmed acceptable.

Risk: Scanning untrusted repositories or package manifests may expose local command and path-handling risks.

Mitigation: Use trusted repositories, prefer offline mode for untrusted code, and review scan results before acting on them.

Risk: An unpinned npx fallback can fetch code that changes between installations.

Mitigation: Install a reviewed, pinned package version or avoid the fallback path until it is fixed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/parkertoddbrooks/skills/wip-license-hook)
- [npm package @wipcomputer/wip-license-hook](https://www.npmjs.com/package/@wipcomputer/wip-license-hook)
- [Project Homepage](https://github.com/wipcomputer/wip-ai-devops-toolbox)
- [Skill Definition](https://github.com/wipcomputer/wip-ai-devops-toolbox/blob/main/tools/wip-license-hook/SKILL.md)
- [MCP Server](https://github.com/wipcomputer/wip-ai-devops-toolbox/blob/main/tools/wip-license-hook/mcp-server.mjs)
- [Universal Interface Spec](https://github.com/wipcomputer/wip-ai-devops-toolbox/blob/main/tools/wip-universal-installer/SPEC.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to generate or update LICENSE-LEDGER.json, license reports, alerts, and static dashboard files when the underlying CLI is run.]

## Skill Version(s):

1.9.72 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
