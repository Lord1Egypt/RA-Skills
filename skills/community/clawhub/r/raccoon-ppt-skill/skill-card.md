## Description:

Raccoon PPT Skill creates full presentation decks from a natural-language topic through the PPT OpenAPI, and supports continuing or checking existing generation tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raccoon-office](https://clawhub.ai/user/raccoon-office)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to create a new full PPT deck from a topic, collect the minimum presentation parameters, continue a service-side follow-up question, and return the final download link when generation succeeds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send the API token and presentation content to a configurable remote PPT service.

Mitigation: Use only a trusted RACCOON_API_HOST, prefer the default service, keep the token in environment variables, and avoid submitting confidential business, customer, personal, or financial material unless remote processing is acceptable.

Risk: Job details, topics, and download links can be stored locally in plaintext state files.

Mitigation: Periodically clear the skill output/jobs state and registry files when they may contain sensitive topics or download links.

## Reference(s):

- [Raccoon PPT Skill on ClawHub](https://clawhub.ai/raccoon-office/skills/raccoon-ppt-skill)
- [Publisher profile](https://clawhub.ai/user/raccoon-office)
- [Raccoon PPT service homepage](https://xiaohuanxiong.com)
- [PPT OpenAPI Skill Reference](references/API_REFERENCE.md)
- [PPT OpenAPI Cheatsheet](references/CHEATSHEET.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, user-facing status messages, and final PPT download links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and RACCOON_API_TOKEN; RACCOON_API_HOST is optional and defaults to the service homepage.]

## Skill Version(s):

1.0.1 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
