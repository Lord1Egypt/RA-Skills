## Description: <br>
Deploy applications and manage projects with complete CLI reference, including commands for deployments, projects, domains, environment variables, and live documentation access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheSethRose](https://clawhub.ai/user/TheSethRose) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to operate Vercel projects through the Vercel CLI, including deployments, local development, domains, environment variables, logs, and status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some referenced Vercel commands can alter production deployments, projects, domains, aliases, or environment data. <br>
Mitigation: Review the exact command, target project, environment, and active Vercel account or team before execution. <br>
Risk: Commands using tokens, logs, or environment-variable operations may expose sensitive data. <br>
Mitigation: Avoid sharing secrets in prompts or output, and approve token, log, and environment-variable commands only when their scope is clear. <br>
Risk: Commands with --yes can skip confirmation prompts for impactful operations. <br>
Mitigation: Require explicit user approval before running commands that use --yes or otherwise bypass interactive confirmation. <br>


## Reference(s): <br>
- [Vercel Documentation](https://vercel.com/docs) <br>
- [Vercel Documentation Sitemap](https://vercel.com/docs/sitemap.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/TheSethRose/vercel) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and command reference tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the vercel and curl command-line tools when executing referenced commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
