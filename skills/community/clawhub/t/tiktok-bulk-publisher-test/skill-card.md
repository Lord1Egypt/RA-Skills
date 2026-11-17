## Description:

Automate bulk uploading and publishing of TikTok videos with customizable titles, privacy, comment, duet, stitch, and upload status controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fly3094](https://clawhub.ai/user/fly3094)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to automate TikTok video publishing through the TikTok Content Posting API, including video metadata, privacy settings, engagement controls, OAuth setup, and publish status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles TikTok account publishing credentials and access tokens.

Mitigation: Review before installing with a real TikTok account, use a test account first, avoid passing tokens or client secrets on the command line, and prefer tightly scoped secret storage.

Risk: The skill can publish content publicly if privacy is not set deliberately.

Mitigation: Set privacy explicitly for each publishing workflow instead of relying on the public default.

Risk: The requested OAuth scopes may exceed what some workflows need.

Mitigation: Consider reducing OAuth scope to only the permissions required for the intended workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fly3094/skills/tiktok-bulk-publisher-test)
- [Publisher profile](https://clawhub.ai/user/fly3094)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include TikTok OAuth credentials, access tokens, privacy settings, upload parameters, and publishing status checks.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
