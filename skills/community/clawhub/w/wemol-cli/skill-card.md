## Description: <br>
wemol-cli helps agents operate the Wemol CLI to discover modules and flows, inspect schemas, submit jobs, track progress, and retrieve outputs for biology, chemistry, and AI workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nanomolar](https://clawhub.ai/user/nanomolar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and domain scientists use this skill to operate Wemol CLI for drug-discovery workflows, including module discovery, flow inspection, job submission, status tracking, and output recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installer and upgrade commands can change the user's local CLI environment. <br>
Mitigation: Install or upgrade only after explicitly trusting Wemol, and prefer a verified or signed installer when available. <br>
Risk: Credentials or session IDs could be exposed if passed in command arguments or logs. <br>
Mitigation: Avoid putting passwords or session IDs in command arguments, and review logs or shared command history before disclosure. <br>
Risk: Wemol jobs may upload local input files to the platform. <br>
Mitigation: Confirm the active Wemol account and host, then review which local files will be uploaded before submitting jobs. <br>


## Reference(s): <br>
- [Wemol platform](https://wemol.wecomput.com) <br>
- [ClawHub release page](https://clawhub.ai/nanomolar/wemol-cli) <br>
- [Flow Workflow](references/flow-workflow.md) <br>
- [Install](references/install.md) <br>
- [Job Workflow](references/job-workflow.md) <br>
- [Module Workflow](references/module-workflow.md) <br>
- [Output And Agent Notes](references/output-and-agent-notes.md) <br>
- [Session And Host](references/session-and-host.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include job IDs, module or flow IDs, command sequences, JSON parameters, and local file paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
