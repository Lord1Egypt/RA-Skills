## Description:

RunComfy CLI on RunComfy teaches agents how to install and authenticate the `runcomfy` CLI, discover model schemas, invoke RunComfy model endpoints, poll or submit asynchronous jobs, download outputs, emit JSON for scripts, and handle common exit codes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[permew](https://clawhub.ai/user/permew)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to operate RunComfy models from a terminal or script, including install, login, request submission, status checks, result download, and automation patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to install and run an unpinned third-party npm package.

Mitigation: Use a pinned, reviewed `@runcomfy/cli` version from a trusted package source and avoid unattended `npx -y` execution.

Risk: RunComfy authentication tokens can be exposed through logs, prompts, shell history, or committed configuration.

Mitigation: Keep `RUNCOMFY_TOKEN` out of prompts and logs, store local token files with owner-only permissions, and prefer scoped environment handling in CI.

Risk: Generated media downloads can consume unexpected disk space or land in an unintended working directory.

Mitigation: Set an explicit output directory and review large-download behavior before running automated batches.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/permew/skills/runcomfy-cli)
- [RunComfy](https://www.runcomfy.com)
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=runcomfy-cli)
- [RunComfy CLI install guide](https://docs.runcomfy.com/cli/install?utm_source=clawhub&utm_medium=skill&utm_campaign=runcomfy-cli)
- [RunComfy CLI authentication](https://docs.runcomfy.com/cli/auth?utm_source=clawhub&utm_medium=skill&utm_campaign=runcomfy-cli)
- [RunComfy CLI quickstart](https://docs.runcomfy.com/cli/quickstart?utm_source=clawhub&utm_medium=skill&utm_campaign=runcomfy-cli)
- [RunComfy CLI command reference](https://docs.runcomfy.com/cli/commands?utm_source=clawhub&utm_medium=skill&utm_campaign=runcomfy-cli)
- [RunComfy CLI troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=runcomfy-cli)
- [RunComfy model catalog](https://www.runcomfy.com/models?utm_source=clawhub&utm_medium=skill&utm_campaign=runcomfy-cli)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, configuration notes, and troubleshooting tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe CLI commands that submit remote jobs, poll status, download generated files, or emit machine-readable JSON.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
