## Description: <br>
One-command release pipeline. Bumps version, updates changelog + SKILL.md, publishes to npm + GitHub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and release engineers use this skill to automate package releases from a repository, including version bumps, changelog and SKILL.md updates, tagging, npm and GitHub publishing, and ClawHub publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish packages, create GitHub releases, deploy public mirrors, merge or delete branches, close issues, and use local npm, GitHub, 1Password, and ClawHub credentials. <br>
Mitigation: Install and run it only in trusted repositories with scoped credentials; use --dry-run first and use --no-publish or --no-deploy-public when publishing or public sync is not intended. <br>
Risk: A configured websiteRepo or deploy.sh target can cause website publication during the release flow. <br>
Mitigation: Review .publish-skill.json, WIP_WEBSITE_REPO, and deploy.sh before release execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/parkertoddbrooks/wip-release) <br>
- [Publisher profile](https://clawhub.ai/user/parkertoddbrooks) <br>
- [npm package](https://www.npmjs.com/package/@wipcomputer/wip-release) <br>
- [Project homepage](https://github.com/wipcomputer/wip-release) <br>
- [Universal Interface Spec](https://github.com/wipcomputer/wip-universal-installer/blob/main/SPEC.md) <br>
- [README](artifact/README.md) <br>
- [Reference](artifact/REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with CLI commands, module API examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute release automation that mutates repository state and publishes packages when invoked with credentials.] <br>

## Skill Version(s): <br>
1.9.72 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
