## Description:

Quickly generate static websites using VitePress. Supports installing dependencies, initializing projects, local preview, building, and deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to scaffold, configure, preview, build, and deploy VitePress-based documentation sites, blogs, and static websites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup commands and the initialization script create project files, install npm dependencies, and modify package.json in the selected directory.

Mitigation: Run the setup only in the intended project directory and review generated files before committing or deploying them.

Risk: Deployment examples include dependency, GitHub Actions, Docker, and repository write-credential choices that may be unsuitable for production without review.

Mitigation: Pin package versions, GitHub Actions, and Docker images for production or CI, and review any workflow that receives repository write credentials.

## Reference(s):

- [VitePress Documentation](https://vitepress.dev)
- [VitePress Configuration Guide](references/config-guide.md)
- [VitePress Theme Customization](references/theme-customization.md)
- [VitePress Deployment Guide](references/deployment.md)
- [ClawHub Skill Page](https://clawhub.ai/openlark/skills/vitepress-generator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, code snippets, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include npm, VitePress, GitHub Actions, Docker, and static hosting commands that users should review before running.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
