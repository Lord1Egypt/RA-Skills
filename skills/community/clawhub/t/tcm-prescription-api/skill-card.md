## Description:

TCM Prescription API helps agents query a Traditional Chinese Medicine prescription REST API for formula search, details, categories, and symptom-based recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[slamw](https://clawhub.ai/user/slamw)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve Traditional Chinese Medicine formula data, browse categories, and generate informational symptom-based formula recommendations through the documented API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Health-related search terms and symptom descriptions are sent to an external API.

Mitigation: Avoid sharing identifying medical details and treat returned recommendations as informational, not medical advice.

Risk: The documentation includes an API-key-in-URL pattern that can expose credentials through logs, browser history, or shared links.

Mitigation: Use the TCM_API_KEY environment variable and the X-API-Key request header; do not place real API keys in URL query parameters.

## Reference(s):

- [TCM Prescription API reference](artifact/references/api-reference.md)
- [ClawHub skill page](https://clawhub.ai/slamw/skills/tcm-prescription-api)
- [Publisher profile](https://clawhub.ai/user/slamw)
- [TCM prescription API service](https://119.91.226.122)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON summaries and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API response summaries, command examples, and environment-variable setup guidance.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
