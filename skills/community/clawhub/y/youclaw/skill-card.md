## Description:

Youmi Cloud marketing analysis assistant powered by YouShu AI that breaks down ad creatives, uncovers brand advertising strategies, and supports strategy exploration, creative stress testing, and creative polishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youcloud](https://clawhub.ai/user/youcloud)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, brand strategists, and advertising operators use this skill to analyze ad creatives, explore competitor and brand advertising strategies, and refine campaign ideas through YouCloud's YouShu AI service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Marketing prompts and related context are sent to YouCloud's YouShu AI service using the user's API key.

Mitigation: Install and invoke the skill only when this remote processing is intended, and avoid sending content that should not be shared with that service.

Risk: Broad marketing keywords can trigger the skill unintentionally.

Mitigation: Use explicit slash commands for deliberate activation when accidental keyword triggers are a concern.

Risk: Persisting YOUCLOUD_API_KEY in shell profile files can expose the credential to other local processes or future sessions.

Mitigation: Store and scope the API key deliberately, rotate it if exposed, and avoid persistent shell configuration when temporary access is sufficient.

## Reference(s):

- [Usage Example](references/example.md)
- [YouCloud Homepage](https://www.youcloud.com)
- [ClawHub Skill Page](https://clawhub.ai/youcloud/skills/youclaw)
- [YouCloud Publisher Profile](https://clawhub.ai/user/youcloud)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown marketing analysis, creative critique, follow-up prompts, and setup or error guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires YOUCLOUD_API_KEY and may preserve session_id for follow-up questions handled by the remote service.]

## Skill Version(s):

1.2.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
