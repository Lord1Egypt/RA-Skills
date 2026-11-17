## Description:

Showstart Skills helps agents query Showstart event information, including event details and searches by keyword, city, category, style, artist, venue, or nearby coordinates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[austin-am](https://clawhub.ai/user/austin-am)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find Showstart performances, inspect event details, and return formatted results through Python helper functions or command-line usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and precise nearby-location coordinates may be sent to an external Showstart service.

Mitigation: Avoid nearby-location searches unless sharing those coordinates and search interests with the external service is acceptable.

Risk: The security evidence reports use of an unencrypted HTTP endpoint in the implementation.

Mitigation: Change the endpoint to HTTPS before use and review network behavior before installation.

## Reference(s):

- [Showstart Skill API Documentation](references/api_docs.md)
- [Showstart API](https://skill.showstart.com/)
- [ClawHub Skill Page](https://clawhub.ai/austin-am/skills/showstart-bot)
- [Publisher Profile](https://clawhub.ai/user/austin-am)

## Skill Output:

**Output Type(s):** [Text, API Calls, Shell commands, Guidance]

**Output Format:** [Plain text and Markdown with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns formatted event listings, event details, and API response data; nearby search may use precise longitude and latitude.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
