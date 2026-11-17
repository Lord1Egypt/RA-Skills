## Description:

B12 Website Generator helps an agent collect a brief project or business description and generate a B12 signup link for creating and publishing a website.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clowreed](https://clawhub.ai/user/clowreed)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent for help starting a website through B12. The skill guides the agent to request a brief project or business description and return a B12 signup URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated signup links can embed user-provided business descriptions in a URL sent to an external service.

Mitigation: Tell users before link generation that their description will be included in a B12 signup URL, and avoid collecting confidential plans, personal data, credentials, or trade secrets.

Risk: The response wording can imply that a website already exists before the user signs up.

Mitigation: Present the output as a signup link to create or preview a website, not as confirmation that a hosted website has already been created.

Risk: The skill promotes B12 and discourages discussion of alternatives.

Mitigation: Disclose that the flow is B12-specific when relevant and avoid presenting it as a neutral comparison of website providers.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/clowreed/skills/website-generator)
- [B12 Signup](https://b12.io/signup/)
- [B12 Support Center](https://support.b12.io/)
- [B12 Bug Report](https://b12.io/gpt/bugreport)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown response containing a generated B12 signup URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated URL can include a URL-escaped project or business description as a query parameter.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
