## Description: <br>
Use gd, the relay-gitcode-cli GitCode command line client, for GitCode API v5 workflows including authentication, repositories, pull requests, issues, search, SSH keys, labels, releases, GitCode Pipeline operations, raw API calls, JSON automation, version checks, and shell completion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevetdp](https://clawhub.ai/user/stevetdp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to manage GitCode repositories, issues, pull requests, releases, raw API calls, and pipeline workflows through the local gd CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make authenticated changes to GitCode repositories, pull requests, releases, and pipelines. <br>
Mitigation: Use least-privilege tokens, start with read-only commands, and require explicit approval before write operations. <br>
Risk: Repository moves, recreate syncs, raw API writes, release publishing, and pipeline changes can have broad or difficult-to-reverse effects. <br>
Mitigation: Require explicit user approval for these operations and prefer disposable repositories for end-to-end checks. <br>
Risk: The workflow handles sensitive credentials such as GitCode, OpenLibing, and GitHub tokens. <br>
Mitigation: Keep tokens in environment variables or keyring-backed login, avoid printing or committing credentials, and avoid storing private API responses in files. <br>
Risk: TLS verification is disabled by default for GitCode API calls in the documented gd behavior. <br>
Mitigation: Enable TLS verification with GD_SSL_VERIFY, GITCODE_SSL_VERIFY, or SSL_VERIFY when the environment supports it. <br>


## Reference(s): <br>
- [Relay GitCode CLI Workflows](references/cli-workflows.md) <br>
- [GitCode Workflow YAML Examples](references/gitcode-workflow-yml.md) <br>
- [Project homepage](https://github.com/coolplayagent/relay-gitcode-cli) <br>
- [GitCode Pipeline documentation](https://docs.gitcode.com/en/docs/help/home/org_project/pipeline/pipeline-intro1/) <br>
- [ClawHub skill page](https://clawhub.ai/stevetdp/relay-gitcode-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON-oriented CLI examples, and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Skill guidance favors explicit repositories, bounded JSON output, and least-privilege credential use.] <br>

## Skill Version(s): <br>
0.1.5 (source: evidence release and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
