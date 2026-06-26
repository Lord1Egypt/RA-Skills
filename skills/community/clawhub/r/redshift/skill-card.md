## Description: <br>
Manage application secrets with the Redshift CLI, a decentralized encrypted secret-management tool built on Nostr. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[accolver](https://clawhub.ai/user/accolver) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to manage Redshift projects, environments, authentication, secret CRUD operations, secret import/export, and command execution with injected secrets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands can reveal, delete, export, or inject application secrets. <br>
Mitigation: Confirm the project, environment, secret names, delete operations, raw secret display, secret file exports, and any redshift run command before execution. <br>
Risk: The skill depends on a locally installed redshift binary. <br>
Mitigation: Install the redshift binary only from a trusted source before allowing an agent to assist with Redshift commands. <br>
Risk: Passing secret values directly on command lines may expose them through shell history, logs, or process inspection. <br>
Mitigation: Prefer interactive input, stdin, or CI secret-management environment variables such as REDSHIFT_NSEC and REDSHIFT_BUNKER for sensitive values. <br>


## Reference(s): <br>
- [Redshift project homepage](https://redshiftapp.com) <br>
- [Redshift install and build source](https://github.com/accolver/redshift) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that expose or manipulate secrets; sensitive actions should be confirmed before execution.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
