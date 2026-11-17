## Description:

Executes AI workflow orchestration flows using the AetherLang \u03a9 DSL for multi-step AI pipelines such as recipes, business strategy, market analysis, and molecular gastronomy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[contrario](https://clawhub.ai/user/contrario)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to submit AetherLang flow code and a user query to an external API that runs orchestrated AI workflows and returns structured results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends AetherLang flow code and user query text to api.neurodoc.app for processing.

Mitigation: Notify the user before the first API call and install only when the user is comfortable with that external data transfer.

Risk: Requests could expose sensitive information if a user includes secrets, credentials, personal account details, confidential business data, uploaded files, or hidden context.

Mitigation: Send only the explicit flow code and query text, strip sensitive data before requests, and avoid including files, credentials, or hidden context.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/contrario/skills/skills-2)
- [Publisher homepage and privacy policy](https://masterswarm.net)
- [AetherLang execution API endpoint](https://api.neurodoc.app/aetherlang/execute)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, JSON, Guidance]

**Output Format:** [Markdown guidance with JSON API request and response structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sends only AetherLang flow code and user query text to the disclosed external API.]

## Skill Version(s):

2.0.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
