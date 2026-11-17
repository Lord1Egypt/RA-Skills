## Description:

Automates a local stock prediction workflow from image-based stock-code extraction through service health checks, model switching, batch prediction, and returning result text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guanhang89](https://clawhub.ai/user/guanhang89)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run a Windows-based local Kronos stock prediction workflow when a prompt includes stock-code images and prediction parameters. It checks the local backend, switches to the expected model, executes batch prediction, and returns generated prediction results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can start a local backend and switch models as part of the prediction workflow.

Mitigation: Use it only in a trusted local Kronos environment and require operator confirmation before starting services or switching models.

Risk: The prediction script builds a PowerShell command string from runtime inputs.

Mitigation: Validate dates and numeric sample counts before execution, and update the script to call the prediction command with an argument list instead of a shell string.

Risk: The workflow reads and returns local prediction result files.

Mitigation: Run under a low-privilege account and review output paths so only expected prediction files are accessed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guanhang89/skills/stock-prediction)
- [ClawHub publisher profile](https://clawhub.ai/user/guanhang89)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration]

**Output Format:** [Markdown and plain text with shell command and script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns prediction status and result text from local files after running the configured workflow.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
