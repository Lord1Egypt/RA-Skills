## Description: <br>
License rug-pull detection that scans dependencies and forks for license changes, gates upstream merges, maintains a license ledger, and generates a public compliance dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to detect dependency or upstream fork license drift before changes enter a repository. It supports CLI, git-hook, and MCP workflows for license ledgers, merge gates, reports, and dashboards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Online scans can execute package-manager and git commands against the target repository. <br>
Mitigation: Install only for trusted workflows, sandbox scans for untrusted repositories or pull requests, and prefer offline mode where practical. <br>
Risk: Installing the optional git hooks changes repository workflow by blocking or warning on license drift. <br>
Mitigation: Treat hook installation as a deliberate workflow change and review the generated hook behavior before enabling it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/parkertoddbrooks/wip-license-hook) <br>
- [Publisher profile](https://clawhub.ai/user/parkertoddbrooks) <br>
- [Project homepage](https://github.com/wipcomputer/wip-ai-devops-toolbox) <br>
- [NPM package](https://www.npmjs.com/package/@wipcomputer/wip-license-hook) <br>
- [Universal Interface Spec](https://github.com/wipcomputer/wip-ai-devops-toolbox/blob/main/tools/wip-universal-installer/SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [CLI and MCP text responses, Markdown reports, JSON ledger files, git-hook shell scripts, and static HTML dashboard files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update LICENSE-LEDGER.json, ledger snapshots, installed git hooks, and dashboard output in the target repository.] <br>

## Skill Version(s): <br>
1.9.72 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
