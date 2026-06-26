## Description: <br>
Deploy to Vercel for site editing, production deployment, aliasing, and live verification tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ranlywood](https://clawhub.ai/user/ranlywood) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site maintainers use this skill to edit HTML, deploy projects to Vercel, assign aliases, and verify the live site. It also guides Vercel authentication and project configuration workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide production deploys, alias changes, and project creation that may publish unintended content. <br>
Mitigation: Require explicit confirmation before production deploys, aliases, or new project creation, and verify the deployed URL before treating the task as complete. <br>
Risk: Broad Vercel tokens or stored credentials can expose account-level deployment authority. <br>
Mitigation: Prefer normal Vercel CLI authentication or scoped session tokens, and do not write tokens to shell profiles or repository files. <br>
Risk: Commands that change SSO, password protection, or trusted IP settings can weaken site access controls. <br>
Mitigation: Confirm the exact security-setting change with the user and limit it to the intended Vercel project. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command blocks, file-editing instructions, and a final public URL after successful deployment] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Vercel CLI authentication or a session-scoped Vercel token; production actions should be confirmed before execution.] <br>

## Skill Version(s): <br>
1.4.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
