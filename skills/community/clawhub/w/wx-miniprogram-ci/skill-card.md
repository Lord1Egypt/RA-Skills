## Description:

Helps developers preview, upload, build npm, upload cloud functions, and upload cloud storage for WeChat Mini Program projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[super9du](https://clawhub.ai/user/super9du)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers maintaining WeChat Mini Program projects use this skill to configure and run miniprogram-ci operations, including preview, upload, npm build, cloud function and cloud storage upload, and source map retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload code and cloud assets to WeChat services.

Mitigation: Review generated commands before execution and use least-privilege WeChat CI credentials in a dedicated project environment.

Risk: The skill uses WeChat CI private key paths and may persist configuration in the user's home directory.

Mitigation: Store private keys securely, avoid sharing config files, and prefer project-specific configuration paths when appropriate.

Risk: The init flow may install global tooling with npm install -g miniprogram-ci.

Mitigation: Preinstall and pin an approved miniprogram-ci version before using the skill in controlled environments.

## Reference(s):

- [miniprogram-ci package](https://www.npmjs.com/package/miniprogram-ci)
- [WeChat Mini Program CI documentation](https://developers.weixin.qq.com/miniprogram/dev/devtools/ci.html#%E6%A6%82%E8%BF%B0)
- [Wx Miniprogram Ci on ClawHub](https://clawhub.ai/super9du/skills/wx-miniprogram-ci)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JavaScript configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may create local output files and may persist WeChat Mini Program CI configuration when executed.]

## Skill Version(s):

1.2.1 (source: release evidence and script constant)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
