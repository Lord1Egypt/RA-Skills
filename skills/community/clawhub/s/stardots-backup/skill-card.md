## Description:

Automatically backs up image attachments to stardots.io cloud storage using configurable Stardots credentials and MD5 request signing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keepchen](https://clawhub.ai/user/keepchen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to upload image attachments from an agent session to Stardots cloud storage when triggered by backup or upload requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports unsafe shell execution and weak attachment-path controls that could expose local files or run unintended commands.

Mitigation: Review before installing; use only with non-sensitive images from trusted attachment sources, validate attachment handles and file contents, and prefer a version that uses a native upload client instead of shell-based curl.

Risk: Credentials may be exposed because the implementation passes authentication material through command-line curl headers.

Mitigation: Avoid shared hosts or verbose process monitoring, rotate Stardots credentials regularly, and prefer a version that keeps secrets out of command-line arguments.

Risk: Image uploads occur when trigger phrases match, which may send files to Stardots without sufficient user confirmation.

Mitigation: Require explicit confirmation before upload and limit use to intended images and trusted conversations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/keepchen/skills/stardots-backup)
- [Stardots.io](https://stardots.io)
- [Stardots OpenAPI documentation](https://stardots.io/en/documentation/openapi)

## Skill Output:

**Output Type(s):** [text, API calls, shell commands, configuration]

**Output Format:** [Text status message with upload URLs or error details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Stardots API key, API secret, and storage space configuration.]

## Skill Version(s):

1.0.0 (source: evidence release metadata, skill.yaml, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
