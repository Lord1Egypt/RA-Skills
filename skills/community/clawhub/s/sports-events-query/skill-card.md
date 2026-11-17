## Description:

Retrieve sports events, results, team information, and league details across multiple sports using TheSportsDB free API without requiring an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mingo-318](https://clawhub.ai/user/mingo-318)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to answer sports schedule, result, live score, league, and team information requests by running a local Python wrapper for TheSportsDB.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound HTTPS requests to TheSportsDB and depends on the Python requests package.

Mitigation: Install dependencies in a virtual environment and pin versions when reproducibility matters.

Risk: Sports schedules, live scores, and results can be incomplete, delayed, or unavailable if the upstream API changes or is unreachable.

Mitigation: Treat returned sports data as live third-party information and verify important results against an authoritative source.

Risk: Command output may include Chinese labels even when invoked from an English workflow.

Mitigation: Review or translate output before presenting it in an English-only user experience.

## Reference(s):

- [TheSportsDB API](https://www.thesportsdb.com/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text or Markdown summaries with command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Makes outbound HTTPS requests to TheSportsDB; responses depend on upstream API availability and data freshness.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
