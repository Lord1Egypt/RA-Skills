## Description: <br>
Post content to social media via the Publer API, including media upload, post creation, scheduling, and job polling for Publer-supported platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imamark](https://clawhub.ai/user/imamark) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and social media operators use this skill to list Publer accounts, upload media, publish immediately, schedule posts, and check publishing jobs from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent using this skill can publish or schedule social posts through the configured Publer workspace. <br>
Mitigation: Review account IDs, media IDs, captions, privacy, and schedule before running live post commands; use the dry-run option for important or ambiguous posts. <br>
Risk: The skill uses a Publer API key and workspace ID that grant access to connected social accounts. <br>
Mitigation: Install only when Publer access is intended, store credentials outside the artifact, and use the least-privileged workspace or account setup available. <br>
Risk: Local media files selected for upload are sent to Publer. <br>
Mitigation: Confirm file paths and media contents before upload and avoid including private or unintended assets. <br>


## Reference(s): <br>
- [Publer API Reference](references/api.md) <br>
- [Publer API endpoint](https://app.publer.com/api/v1) <br>
- [ClawHub Publer release](https://clawhub.ai/imamark/publer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, the requests package, PUBLER_API_KEY, and PUBLER_WORKSPACE_ID; supports dry-run payload preview before live post commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
