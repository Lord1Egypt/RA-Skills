## Description:

Uses pippit-tool-cli to submit, monitor, and retrieve short-drama creation tasks, including script generation, continuation, rewriting, plot expansion, character setup, episode drafts, worldbuilding, session files, and downloaded results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ydtincle](https://clawhub.ai/user/ydtincle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to route short-drama creation requests through the Xiao Yunque/Pippit CLI, track task progress, answer required service prompts, and retrieve generated assets. It is intended for workflows where the user already plans to use the Xiao Yunque/Pippit short-drama service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected .doc, .docx, or .txt reference files are sent to the Xiao Yunque/Pippit short-drama service.

Mitigation: Review user content before submission and use the skill only when the user intentionally wants to use that external service.

Risk: The CLI may store credentials and open service links as part of the workflow.

Mitigation: Use an account intended for this service, review CLI login behavior, and avoid running it in shared or untrusted environments.

Risk: Service-directed downloads can write generated assets to local output paths.

Mitigation: Run the skill in a contained workspace and avoid output locations where downloaded assets could overwrite important files.

Risk: The security review verdict is suspicious because the external CLI and service downloads have broad authority over submitted content and local files.

Mitigation: Review the skill before installation, pin the CLI version where possible, and monitor downloaded files before reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ydtincle/skills/xyq-short-drama-skill)
- [Publisher profile](https://clawhub.ai/user/ydtincle)
- [Xiao Yunque Web UI](https://xyq.jianying.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with CLI commands, text and JSON result summaries, and locally downloaded generated files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pippit-tool-cli and a Xiao Yunque/Pippit account; generated assets may be downloaded into the local workspace.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
