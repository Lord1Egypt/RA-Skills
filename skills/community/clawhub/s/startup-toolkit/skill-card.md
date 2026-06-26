## Description: <br>
Startup Toolkit helps agents scaffold a basic local startup project folder and provide launch-oriented guidance for a SaaS MVP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sunshine-del-ux](https://clawhub.ai/user/Sunshine-del-ux) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and startup builders use this skill to create a simple project directory structure for an MVP and get next-step launch guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact presents authentication, payments, analytics, Docker, and CI/CD as included capabilities, but the security summary says it is only a basic scaffold. <br>
Mitigation: Treat generated output as a starting folder structure and independently implement and review production auth, payments, analytics, Docker, and CI/CD before use. <br>
Risk: The launch script creates project directories in the current working directory. <br>
Mitigation: Run it only from a workspace where creating a new project folder is intended, and review generated files before integrating them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Sunshine-del-ux/startup-toolkit) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/Sunshine-del-ux) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown guidance with bash commands and generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates frontend, backend, database, and docker directories under the requested project name.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
