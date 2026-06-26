## Description: <br>
Vercel CLI skill for deploying and managing Vercel projects from the terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to get guidance for deploying, inspecting, rolling back, and managing Vercel projects, domains, teams, usage, and environment variables with the Vercel CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide account-level Vercel actions such as deletes, production promotions, rollbacks, billing-related usage checks, and domain purchases. <br>
Mitigation: Require manual confirmation before purchase, delete, production promotion, rollback, domain, billing, or team-management commands are executed. <br>
Risk: The skill requires a Vercel token and may involve environment variables or pulled env files. <br>
Mitigation: Use the least-privileged available Vercel token, prefer the VERCEL_TOKEN environment variable, and treat pulled env files as secrets that must not be committed or indexed. <br>
Risk: API write/delete calls and protection-bypass curl requests can change live resources or bypass expected protections. <br>
Mitigation: Review the target endpoint, method, project, team, and environment before allowing API write/delete calls or protection-bypass curl commands. <br>


## Reference(s): <br>
- [Vercel CLI Command Reference](references/commands.md) <br>
- [Vercel Access Tokens](https://vercel.com/account/tokens) <br>
- [ClawHub Skill Page](https://clawhub.ai/openlark/vercel-cli) <br>
- [OpenLark Publisher Profile](https://clawhub.ai/user/openlark) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may reference authenticated Vercel account operations and should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
