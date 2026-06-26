## Description: <br>
Deploys code from the current directory to Railway using `railway up`, including detached deploys and CI log-streaming mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dbanys](https://clawhub.ai/user/dbanys) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to deploy local code changes to linked or explicitly selected Railway projects, services, and environments. It helps choose detached or CI mode, attach commit messages, and interpret common deployment errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad Railway CLI authority and can deploy from the current repository to live Railway resources. <br>
Mitigation: Before each use, confirm the logged-in Railway account, project, service, environment, and working directory. <br>
Risk: Administrative examples in the artifact can create, modify, or delete Railway resources beyond routine deploys. <br>
Mitigation: Only allow environment edits, service creation, Docker image changes, or deletions after an explicit request for that exact administrative action. <br>


## Reference(s): <br>
- [Railway Deploy ClawHub Page](https://clawhub.ai/dbanys/railway-deploy) <br>
- [Environment Config Reference](references/environment-config.md) <br>
- [Monorepo Reference](references/monorepo.md) <br>
- [Railpack Reference](references/railpack.md) <br>
- [Variables Reference](references/variables.md) <br>
- [Railpack Documentation](https://railpack.com/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute Railway CLI deploy commands against the current repository when the agent is permitted to run shell commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
