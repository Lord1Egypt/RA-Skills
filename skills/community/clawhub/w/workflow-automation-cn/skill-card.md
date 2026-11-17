## Description:

Generates OpenClaw heartbeat automation scripts from natural-language workflow requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to turn natural-language automation ideas into scheduled scripts, heartbeat configuration, test commands, and operational guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated scheduled automations can call external services, change files, or publish content without sufficiently narrow scope.

Mitigation: Review the full script, schedule, file paths, external endpoints, message contents, and credentials handling before adding anything to HEARTBEAT.md.

Risk: Automation examples may encourage hardcoded tokens or shared temporary state files.

Mitigation: Use environment variables or a secret store for credentials, and use private per-workflow state directories instead of hardcoded tokens or shared /tmp files.

Risk: A recurring automation can repeat mistakes after activation.

Mitigation: Test generated scripts manually, add error handling and logging, and activate heartbeat schedules only after review.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated scripts, HEARTBEAT.md snippets, file paths, schedules, API endpoints, and logging instructions.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
