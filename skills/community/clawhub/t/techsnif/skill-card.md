## Description:

Query TechSnif tech news intelligence through a bundled CLI for current articles across AI, Startups, Venture, and Robotics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coffeefuelbump](https://clawhub.ai/user/coffeefuelbump)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to query current TechSnif technology news, retrieve full articles, and synthesize briefings about AI, startups, venture capital, robotics, companies, or topics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled CLI makes live network requests for tech-news queries.

Mitigation: Use the skill only where sending query terms to TechSnif is acceptable and review returned sources before relying on summaries.

Risk: The CLI endpoint can be redirected with --api-url or TECHSNIF_API_URL, allowing an alternate endpoint to receive query terms and supply content for summarization.

Mitigation: Do not use endpoint overrides unless the alternate endpoint is intentionally trusted.

## Reference(s):

- [TechSnif homepage](https://techsnif.com/)
- [TechSnif CLI npm package](https://www.npmjs.com/package/@techsnif/cli)
- [TechSnif categories reference](references/categories.md)
- [ClawHub skill page](https://clawhub.ai/coffeefuelbump/skills/techsnif)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or text summaries based on JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Use --json for structured CLI output and check the ok field before reading data. Listing commands omit article content; retrieve full content with the article command.]

## Skill Version(s):

1.0.4 (source: server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
