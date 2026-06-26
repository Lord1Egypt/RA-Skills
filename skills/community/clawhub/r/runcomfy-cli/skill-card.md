## Description: <br>
Guides agents and developers through installing, authenticating, and using the RunComfy CLI to run RunComfy model endpoints, inspect schemas, poll jobs, script JSON output, and handle errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kalvinrv](https://clawhub.ai/user/kalvinrv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate RunComfy from a terminal or script, including setup, authentication, model invocation, job polling, downloads, JSON output, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RunComfy token and local CLI configuration. <br>
Mitigation: Protect the token, avoid logging or committing it, use the RUNCOMFY_TOKEN environment variable where appropriate, and rotate credentials when needed. <br>
Risk: The workflow depends on installing and running an external CLI. <br>
Mitigation: Install only the verified RunComfy CLI package or inspect installer scripts before use. <br>
Risk: Model outputs may be downloaded to local disk. <br>
Mitigation: Choose output directories deliberately and review generated files before relying on or sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kalvinrv/runcomfy-cli) <br>
- [RunComfy](https://www.runcomfy.com) <br>
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=runcomfy-cli) <br>
- [RunComfy CLI install guide](https://docs.runcomfy.com/cli/install?utm_source=clawhub&utm_medium=skill&utm_campaign=runcomfy-cli) <br>
- [RunComfy CLI authentication](https://docs.runcomfy.com/cli/auth?utm_source=clawhub&utm_medium=skill&utm_campaign=runcomfy-cli) <br>
- [RunComfy model catalog](https://www.runcomfy.com/models?utm_source=clawhub&utm_medium=skill&utm_campaign=runcomfy-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce RunComfy CLI commands, environment variable setup, request JSON, polling commands, and download guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
