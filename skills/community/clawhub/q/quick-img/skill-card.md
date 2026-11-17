## Description:

Generate images using curl and the SkillBoss API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Quick Img V2 to generate image URLs from text prompts through the SkillBoss/HeyBoss API using curl. The skill requires SKILLBOSS_API_KEY and includes a separate IP-check command.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image-generation prompts and SKILLBOSS_API_KEY are sent to the external SkillBoss/HeyBoss API.

Mitigation: Avoid sensitive prompts or secrets unless that external data flow is acceptable for the deployment.

Risk: The Check IP command contacts httpbin.org and exposes the runtime environment's public IP address.

Mitigation: Remove or avoid the Check IP workflow unless the deployment explicitly needs that network check.

## Reference(s):

- [Quick Img V2 on ClawHub](https://clawhub.ai/marjoriebroad/skills/quick-img)
- [SkillBoss API endpoint](https://api.heybossai.com/v1/run)
- [SkillBoss API key service](https://www.skillboss.co)
- [httpbin IP check endpoint](https://httpbin.org/get)

## Skill Output:

**Output Type(s):** [shell commands, API calls, guidance]

**Output Format:** [Markdown with bash commands; runtime output is an image URL or JSON response.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for image generation.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
