## Description:

Automatically uploads local image files to Stardots.io cloud storage, lists uploaded files, and returns access links using configured Stardots API credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keepchen](https://clawhub.ai/user/keepchen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users can use this skill to back up selected local images to a configured Stardots.io space and inspect recently uploaded files from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runtime HTTP dependencies have confirmed credential-handling and upload-related vulnerabilities.

Mitigation: Review the skill before installation and update vulnerable runtime dependencies before relying on it in sensitive workflows.

Risk: The skill uploads selected local image files to Stardots.io using the configured account and space.

Mitigation: Confirm the local file path and destination space before upload, and avoid sensitive images unless the Stardots.io account and data handling are approved for that content.

Risk: Uploads depend on API credentials stored in the agent configuration.

Mitigation: Use scoped Stardots API credentials, rotate them if exposed, and restrict skill access to users allowed to upload to the configured space.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/keepchen/skills/stardots-backup-skill)
- [Stardots.io](https://stardots.io)
- [Stardots OpenAPI documentation](https://stardots.io/en/documentation/openapi)

## Skill Output:

**Output Type(s):** [text, configuration, API calls]

**Output Format:** [Plain text status messages with file metadata, URLs, and error guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns upload success or failure details, uploaded file URLs, file lists, and suggested retry actions.]

## Skill Version(s):

1.0.1 (source: server release metadata, skill.yaml, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
