## Description:

Relay GitCode CLI guides agents to use the local `gd` command line client for GitCode API v5 workflows, including authentication, repositories, pull requests, issues, search, SSH keys, labels, releases, pipelines, raw API calls, JSON automation, version checks, and shell completion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevetdp](https://clawhub.ai/user/stevetdp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when an agent needs to inspect or change GitCode resources through `gd` commands instead of GitHub-only tooling. It supports repository, pull request, issue, release, label, SSH key, pipeline, workflow YAML, and raw API automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles GitCode credentials and private API responses.

Mitigation: Use narrow, revocable tokens through environment variables or keyring-backed login, and do not print, commit, or persist tokens or private API responses.

Risk: The documented CLI behavior disables TLS certificate verification by default.

Mitigation: Enable verification with `GD_SSL_VERIFY`, `GITCODE_SSL_VERIFY`, or `SSL_VERIFY` set to `true`, and avoid setting `GIT_SSL_NO_VERIFY`.

Risk: The skill can guide powerful repository and API changes, including moves, delete/recreate syncs, SSH-key deletion, label deletion, pipeline cancellation, and raw API mutations.

Mitigation: Require explicit user confirmation before high-impact operations, prefer disposable repositories for tests, and use dry-run or skip modes where available.

Risk: Online installation fallbacks may fetch unpinned binaries or packages.

Mitigation: Prefer bundled or already installed released `gd` binaries, verify the selected version before use, and avoid online installs unless no usable local binary exists.

## Reference(s):

- [Relay GitCode CLI ClawHub page](https://clawhub.ai/stevetdp/skills/relay-gitcode-cli)
- [Relay GitCode CLI homepage](https://github.com/coolplayagent/relay-gitcode-cli)
- [Relay GitCode CLI Workflows](references/cli-workflows.md)
- [GitCode Workflow YAML Examples](references/gitcode-workflow-yml.md)
- [GitCode Pipeline documentation](https://docs.gitcode.com/en/docs/help/home/org_project/pipeline/pipeline-intro1/)
- [GitCode Pipeline documentation (Chinese)](https://docs.gitcode.com/docs/help/home/org_project/pipeline/pipeline-intro1/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, JSON-oriented command patterns, and GitCode workflow YAML snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefers explicit repositories, bounded result sizes, and `--json` output for agent-readable automation.]

## Skill Version(s):

0.1.5 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
