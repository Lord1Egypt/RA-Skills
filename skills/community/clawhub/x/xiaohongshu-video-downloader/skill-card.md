## Description:

Parses Xiaohongshu (RED) video links that include xsec_token and returns watermark-free video and cover download links through redfox.hk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as creators, editors, collectors, and operators use this skill to validate Xiaohongshu links they are authorized to process and receive direct video download links for saving, editing, backup, or analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Token-bearing Xiaohongshu links are sent to the third-party redfox.hk API.

Mitigation: Use only Xiaohongshu links you are authorized to process, avoid private or sensitive links, and review redfox.hk handling terms before use.

Risk: The API key can be stored on disk when the save-key option is used.

Mitigation: Prefer environment-variable or one-time CLI key configuration unless persistent local storage is acceptable, and rotate or revoke the key if exposure is suspected.

Risk: The security evidence reports limited privacy and authorization guardrails.

Mitigation: Review the skill before installation and require users to confirm they have permission to download or analyze the submitted content.

## Reference(s):

- [Core Workflow](references/core_workflow.md)
- [RedFox API Key Settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [ClawHub Skill Page](https://clawhub.ai/redfox-data/skills/xiaohongshu-video-downloader)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown-style terminal text with video download links, cover links, descriptions, batch summaries, and optional JSON response data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned video download links are time-limited; batch mode summarizes success and failure counts.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
