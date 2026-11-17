## Description:

Unified gateway skill for async execute/poll, portal user closure, and telemetry feedback workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinasilva](https://clawhub.ai/user/chinasilva)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to run BinaryWorks gateway capabilities, poll asynchronous results, perform portal account actions, normalize attachments, and submit feedback from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles credentials and portal account actions.

Mitigation: Install only from a trusted publisher, restrict invocation to the intended gateway domains, and require explicit confirmation for voucher redemption or recharge creation.

Risk: Telemetry is enabled by default and can use a configurable telemetry base URL.

Mitigation: Disable or constrain telemetry with runtime environment controls, and do not pass untrusted SKILL_TELEMETRY_BASE_URL values.

Risk: Local file_path inputs can upload files from the agent runtime.

Mitigation: Avoid raw file_path inputs for sensitive files; prefer pre-uploaded attachment URLs or explicitly approved files.

Risk: Face and person recognition capabilities may involve sensitive image analysis.

Mitigation: Limit use to appropriate datasets and user-approved workflows, and treat recognition results as sensitive.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chinasilva/skills/skill-hub-gateway)
- [Gateway Homepage](https://gateway.binaryworks.app)
- [Capability Reference](references/capabilities.json)
- [OpenAPI Reference](references/openapi.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON API responses, and command-line script output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include run identifiers, status payloads, uploaded file URLs, presentation assets, and telemetry or feedback results.]

## Skill Version(s):

2.4.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
