## Description:

微信小程序云开发完整指南。包含项目结构、云函数开发、miniprogram-ci 部署命令、常见问题处理。适用于需要开发、部署微信小程序的场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasondu](https://clawhub.ai/user/jasondu)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to create, configure, preview, upload, and troubleshoot WeChat mini-program cloud development projects. It provides project structure guidance, cloud function examples, miniprogram-ci commands, and common operational fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes deployment commands that dynamically run an unpinned miniprogram-ci package with access to a private-key path.

Mitigation: Review the skill before installing or running scripts, keep private keys outside the repository where possible, and use a pinned or lockfile-controlled miniprogram-ci dependency.

Risk: The artifact includes project-specific operational identifiers and paths that may not match the user's environment.

Mitigation: Replace AppID, cloud environment ID, project paths, and private-key paths with the user's own values or placeholders before use.

## Reference(s):

- [WeChat Mini-Program Development Environment Information](references/config.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON, JavaScript, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes deployment command examples that should be adapted to the user's own AppID, cloud environment ID, and private-key path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
