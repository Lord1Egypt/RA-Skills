## Description:

Generate AI-powered presentations, documents, and social posts using SkillBoss API Hub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate presentations, documents, and social media carousels from prompts or markdown content through SkillBoss API Hub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill sends the API key and user content to a different hostname than the documentation discloses.

Mitigation: Review the SkillBoss service and the api.heybossai.com destination before installing; avoid confidential, personal, or regulated data unless the publisher explains the domain relationship and data handling.

Risk: The skill requires an API key for an external service.

Mitigation: Use a narrowly scoped, revocable SKILLBOSS_API_KEY and rotate or revoke it if misuse is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/skills/toby-gamma)
- [Documented SkillBoss API endpoint](https://api.skillbossai.com/v1/pilot)
- [Runtime API endpoint used by script](https://api.heybossai.com/v1/pilot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with bash commands; script output is plain text containing a generated Gamma URL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends user-provided content to an external API service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
