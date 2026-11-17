## Description:

Vienna public transport (Wiener Linien) real-time data. Use when asking about departures, schedules, disruptions, elevator status, or directions in Vienna's public transport (U-Bahn, tram, bus, night bus). Queries stops, lines, and traffic info.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hjanuschka](https://clawhub.ai/user/hjanuschka)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to query Vienna public transport stops, departures, disruptions, and elevator outage information from Wiener Linien public real-time data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stop-name searches may treat user input as grep options or regular expressions.

Mitigation: Harden search-stop.sh by using literal matching, for example grep -iF -- "$QUERY", and use normal stop names, line names, and stop IDs as inputs.

## Reference(s):

- [Wiener Linien OGD Realtime API](https://www.wienerlinien.at/ogd_realtime)
- [Wiener Linien Stop Reference CSV](https://www.wienerlinien.at/ogd_realtime/doku/ogd/wienerlinien-ogd-haltepunkte.csv)
- [ClawHub Skill Page](https://clawhub.ai/hjanuschka/skills/wienerlinien)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public Wiener Linien API responses; scripts require curl and jq.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
