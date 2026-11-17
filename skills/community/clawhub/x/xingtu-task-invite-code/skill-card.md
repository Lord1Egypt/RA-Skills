## Description:

This skill helps an agent batch download QR code invitation images from XingTu recruitment tasks by authenticating with cookies, fetching paginated task lists, opening each task detail page, and saving downloaded QR code images by task ID.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juanjuan2538](https://clawhub.ai/user/juanjuan2538)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to automate downloading invitation QR code images for active XingTu recruitment tasks. It is intended for authenticated XingTu workflows where the user has access to the relevant task data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and reuses a XingTu session cookie in plaintext, which can create account-access risk if the file or chat transcript is exposed.

Mitigation: Use the skill only in a trusted local environment, avoid sharing cookies in prompts or logs, delete the plaintext cookie file when finished, and rotate or log out the XingTu session if exposure is possible.

Risk: The skill performs live authenticated browser and API actions against XingTu and downloads task QR code images to local storage.

Mitigation: Review the authenticated account, task filters, and output directory before execution, then monitor the first run and stop on unexpected task data or download behavior.

## Reference(s):

- [XingTu API Reference](references/api_spec.md)
- [ClawHub Skill Page](https://clawhub.ai/juanjuan2538/skills/xingtu-task-invite-code)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline PowerShell, Python, shell commands, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions for live browser automation, API calls, progress tracking, and QR image downloads to local files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
