## Description:

Post or schedule video content to TikTok using the Publora API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergebulaev](https://clawhub.ai/user/sergebulaev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and social media operators use this skill to prepare API calls and guidance for uploading, drafting, or scheduling TikTok videos through Publora.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publora API keys could be exposed or misused if handled as ordinary text.

Mitigation: Treat the Publora API key as sensitive and avoid placing real keys in shared prompts, code examples, logs, or public files.

Risk: A post could be uploaded to the wrong TikTok account or scheduled for the wrong time.

Mitigation: Confirm the target TikTok platform ID and scheduled time before running examples against a real account.

Risk: Captions or videos that exceed TikTok API limits may fail or trigger posting errors.

Mitigation: Review captions and videos before upload, including caption length, video duration, daily posting volume, and rate limits.

Risk: Unaudited TikTok apps may publish posts as private by default.

Mitigation: Confirm TikTok app audit status and expected visibility before relying on a scheduled post for public distribution.

## Reference(s):

- [Publora API base URL](https://api.publora.com/api/v1)
- [Create post endpoint](https://api.publora.com/api/v1/create-post)
- [Upload URL endpoint](https://api.publora.com/api/v1/get-upload-url)

## Skill Output:

**Output Type(s):** [markdown, code, configuration, guidance]

**Output Format:** [Markdown with JavaScript and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Publora API endpoints, TikTok platform limits, required platform ID format, and upload workflow notes.]

## Skill Version(s):

2.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
