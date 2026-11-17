## Description:

Publish reports to the ZeeLin reports website ("智灵报告网站") by copying report assets, inserting a new top entry into public/reports_config.json for any category, running build checks, and preparing PR-ready branches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thu-nmrc](https://clawhub.ai/user/thu-nmrc)

### License/Terms of Use:


## Use Case:

Developers and report-site maintainers use this skill to publish PDF or presentation reports to the ZeeLin reports website through a branch, build, push, and pull-request workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish to GitHub and change persistent local or account state while preparing report releases.

Mitigation: Confirm the target repository, branch, remotes, and intended PR workflow before allowing push or pull-request creation.

Risk: The bootstrap flow can configure Git identity, GitHub authentication, and SSH keys on the local machine.

Mitigation: Run bootstrap only when account setup is intended; prefer --skip-ssh and --skip-gh-login when authentication or key management is already configured.

Risk: The security summary reports a path-boundary issue that can write outside the target repository.

Mitigation: Use dry-run behavior first where available, review path-related options carefully, and verify the destination paths before permitting file writes.

## Reference(s):

- [Report Metadata Contract](references/report-metadata.md)
- [ClawHub skill page](https://clawhub.ai/thu-nmrc/skills/zeelin-report-publisher)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured publishing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prepare repository file changes, copied report assets, commits, pushes, and pull-request links when executed by an agent with the required local tools and permissions.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
