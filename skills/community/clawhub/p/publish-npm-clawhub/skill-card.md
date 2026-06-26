## Description: <br>
Publish OpenClaw skills or plugins to npm and ClawHub with a guarded workflow for release checks, sanitized publish directories, scanner review, and explicit publishing steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[humanlike2026](https://clawhub.ai/user/humanlike2026) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and release maintainers use this skill to prepare and verify npm and ClawHub releases for OpenClaw skills or plugins. It helps check local release configuration, prepare a sanitized release directory, run release-guard checks, publish intentionally, and confirm ClawHub scanner status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports real npm and ClawHub publishing workflows that can change public package or registry state. <br>
Mitigation: Run npm publish and clawhub publish only with explicit user intent, confirm accounts with whoami commands, and review the generated release directory before publishing. <br>
Risk: Publishing from a repository root can unintentionally include local files such as credentials, environment files, or package archives. <br>
Mitigation: Use a disposable sanitized output path such as /tmp/publish-release and inspect the copied files before release. <br>
Risk: The workflow depends on sensitive local publishing account configuration. <br>
Mitigation: Keep config/publish.accounts.local.json gitignored, ensure it is not tracked, and avoid uploading local account configuration. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/humanlike2026/publish-npm-clawhub) <br>
- [Release Workflow](references/workflow.md) <br>
- [Scanner Review Playbook](references/scanner-playbook.md) <br>
- [Publisher Profile](https://clawhub.ai/user/humanlike2026) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and release status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include release-guard findings, npm and ClawHub verification commands, scanner status interpretation, and concrete remediation steps.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata, skill.json, and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
