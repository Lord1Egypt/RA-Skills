## Description:

Provides real-time sports updates through TheSportsDB and API-Football.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jakah2551](https://clawhub.ai/user/jakah2551)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve live scores, today's fixtures, upcoming matches, recent team results, and team or player search results across supported sports. Football-specific live and daily fixture lookups can use API-Football when the user provides an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API-Football commands accept an API key as a command-line argument, which can expose that key in local process metadata or command logs.

Mitigation: Use the TheSportsDB-only commands when possible; for API-Football, prefer a version that reads the key from a safer secret mechanism and avoid echoing or persisting the key.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jakah2551/skills/sports-live)
- [TheSportsDB API endpoint](https://www.thesportsdb.com/api/v1/json/1/)
- [API-Football registration](https://dashboard.api-football.com/register)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text with sports results and brief command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; optional API-Football commands require a user-provided API key.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
