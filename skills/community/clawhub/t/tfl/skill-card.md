## Description:

London TfL transit - real-time Tube arrivals, bus predictions, line status, service disruptions, journey planning, and route info for the London Underground, DLR, Overground, Elizabeth line, and buses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brianleach](https://clawhub.ai/user/brianleach)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to answer London public transport questions with live TfL status, arrivals, disruptions, route, stop, and journey-planning data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: London transit searches, journey origins and destinations, precise coordinates, and the optional TfL API key may be sent to TfL's official API.

Mitigation: Use a dedicated TfL API key, avoid placing unrelated secrets in the skill's .env file, and avoid entering precise coordinates unless needed.

Risk: The TfL API key is passed in URL query parameters and may appear in request logs.

Mitigation: Treat the key as potentially visible in URL logs and rotate it if exposed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/brianleach/skills/tfl)
- [TfL Unified API](https://api.tfl.gov.uk/)
- [TfL API Portal](https://api-portal.tfl.gov.uk/)
- [Declared Skill Homepage](https://github.com/brianleach/tfl-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with concise transit summaries and inline shell commands when invoking the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live JSON responses from TfL's API and may include line status, arrival predictions, disruptions, journey steps, fares when available, or route and stop information.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
