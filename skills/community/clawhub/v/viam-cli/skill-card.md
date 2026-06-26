## Description: <br>
Guides an agent in installing, authenticating, troubleshooting, and using the Viam CLI to manage robotics fleets, modules, machine data, datasets, and data pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hexbabe](https://clawhub.ai/user/hexbabe) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and robotics operators use this skill to help an agent work with Viam CLI commands for fleet administration, module development, data management, and local troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables broad administration of Viam machines, deployments, data, and credentials. <br>
Mitigation: Use a least-privilege Viam account, authenticate outside chat, and verify the active account with `viam whoami` before sensitive work. <br>
Risk: Remote shell access, file copy, module deploys, registry uploads, data exports or deletes, pipeline changes, API-key creation, and database-user changes can have high impact. <br>
Mitigation: Require explicit user approval before those actions and list or describe resources before mutating them. <br>
Risk: CLI command syntax may drift as the Viam platform changes. <br>
Mitigation: Check the installed CLI help for failing commands and ask permission before upgrading the CLI. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hexbabe/viam-cli) <br>
- [Publisher profile](https://clawhub.ai/user/hexbabe) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Markdown] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Viam CLI commands that affect remote machines, registry assets, data, credentials, and pipelines.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
