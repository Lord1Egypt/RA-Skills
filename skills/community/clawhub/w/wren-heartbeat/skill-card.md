## Description:

Unified heartbeat system for OpenClaw agents that runs parallel health checks, data collectors, and state monitors and returns one actionable summary optimized for LLM consumption.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wrentheai](https://clawhub.ai/user/wrentheai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure and run repeatable heartbeat checks that collect workspace, service, and state signals in parallel and summarize whether action is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace configuration can execute broad shell commands and network calls.

Mitigation: Review every heartbeat.yaml command and endpoint before running, and execute the skill with a restricted runtime account and minimal environment variables.

Risk: Configured output and cache paths can write files in the workspace.

Mitigation: Keep output and cache paths inside a generated-artifacts or similarly scoped directory, and avoid paths that overwrite source or sensitive files.

Risk: Scheduled heartbeat runs can cause agents to act on summaries automatically.

Mitigation: Require user confirmation before cron-triggered summaries cause follow-up actions, especially when a check returns action-needed status.

Risk: Configuration examples may include API keys or secrets in commands.

Mitigation: Use environment variables or secret stores for credentials and avoid hardcoded API keys in heartbeat.yaml.

## Reference(s):

- [Config Reference](references/config.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, JSON status output, brief text status lines, YAML configuration examples, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit codes indicate all clear, runtime error, or action needed; summaries may be written to a configured workspace output path.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
