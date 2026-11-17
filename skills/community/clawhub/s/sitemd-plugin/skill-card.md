## Description:

Build and manage websites from Markdown with MCP tools for page creation, content generation, settings, and deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tyler-berggren](https://clawhub.ai/user/tyler-berggren)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site maintainers use this skill to create, edit, validate, build, and deploy Markdown-based websites through an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install flow and release security summary identify native-code download during installation as a review point.

Mitigation: Install only when the publisher is trusted, test in a non-production project first, avoid administrator execution, and review the downloaded release path before broader use.

Risk: Deployment, activation, login, API key, and configuration tools can affect live sites and credentials.

Mitigation: Verify deployment targets before deploy or activate, require explicit owner confirmation for production changes, and treat login URLs, API keys, and SITEMD_TOKEN as credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tyler-berggren/skills/sitemd-plugin)
- [Publisher profile](https://clawhub.ai/user/tyler-berggren)
- [sitemd homepage](https://sitemd.cc)
- [sitemd documentation](https://sitemd.cc/docs)
- [sitemd repository](https://github.com/sitemd-cc/sitemd)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain-text guidance with tool calls, shell commands, and file or configuration updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update website content, settings, generated site files, authentication state, and deployment targets.]

## Skill Version(s):

0.1.3 (source: server release evidence and artifact/openclaw.plugin.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
