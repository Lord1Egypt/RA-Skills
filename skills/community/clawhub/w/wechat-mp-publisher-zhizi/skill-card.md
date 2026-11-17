## Description:

Enables agents to upload media, manage drafts, publish articles, and query publishing status for WeChat Official Accounts through the WeChat MP API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryan32382](https://clawhub.ai/user/ryan32382)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent prepare WeChat Official Account articles, upload cover or article media, save drafts, submit publications, and check draft or publication status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, publish, or delete WeChat Official Account content.

Mitigation: Use it only with an account where the agent is authorized for those actions, prefer draft mode before publishing, and verify media_id targets before deletion.

Risk: Local file uploads can expose unintended media files.

Mitigation: Restrict uploads to a dedicated media folder and review file paths before invoking upload tools.

Risk: WeChat AppID, AppSecret, and access-token cache files are sensitive credentials.

Mitigation: Protect configuration and token cache files with owner-only permissions and avoid placing secrets in shared locations.

Risk: Dependencies may need updates before production use.

Mitigation: Run dependency review and update vulnerable packages before using the skill in production.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryan32382/skills/wechat-mp-publisher-zhizi)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)
- [Technical specification](artifact/TECH_SPEC.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Configuration]

**Output Format:** [JSON-style tool responses with success flags, status messages, media IDs, publish IDs, draft metadata, and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May upload local media files and create, publish, query, or delete WeChat Official Account content when invoked with valid credentials.]

## Skill Version(s):

2.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
