## Description:

Query UK National Rail live departure boards, arrivals, delays, and train services for GB stations via Darwin/Huxley2 API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jabbslad](https://clawhub.ai/user/jabbslad)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to look up live UK rail departures, arrivals, delays, platforms, service details, and station codes for chat or command-line workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper shell script can send the National Rail token to an endpoint selected through HUXLEY_URL.

Mitigation: Use the Python command path or only run scripts/trains.sh with a trusted HTTPS HUXLEY_URL; rotate the token if it may have been sent to an untrusted endpoint.

## Reference(s):

- [UK Trains ClawHub Skill Page](https://clawhub.ai/jabbslad/skills/uk-trains)
- [National Rail OpenLDBWS Registration](https://realtime.nationalrail.co.uk/OpenLDBWSRegistration/)
- [National Rail OpenLDBWS Endpoint](https://lite.realtime.nationalrail.co.uk/OpenLDBWS/ldb12.asmx)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [JSON API responses and concise Markdown chat summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a NATIONAL_RAIL_TOKEN; live results depend on National Rail Darwin or Huxley2 API availability.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
