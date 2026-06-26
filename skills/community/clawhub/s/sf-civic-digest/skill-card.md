## Description: <br>
Track San Francisco city government activity across public meetings, hearings, planning notices, permits, local journalism, and civic data sources, filtered by district, neighborhood, street, or topic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sgillen](https://clawhub.ai/user/sgillen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and civic researchers use this skill to collect public San Francisco government, housing, transportation, education, journalism, and community event signals, then synthesize daily or weekly civic digests with actionable next steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores local JSON archives and state for sensitive public records and political activity. <br>
Mitigation: Review USER.md before use, avoid tracking private individuals, and periodically delete local archive and state files if historical retention is not desired. <br>
Risk: The security verdict is suspicious because the tool monitors many civic, media, protest, eviction, lobbying, and 311 sources with limited user controls. <br>
Mitigation: Run only in trusted workspaces, inspect generated reports before sharing, and keep the scope limited to public-interest civic monitoring. <br>


## Reference(s): <br>
- [SF Civic Digest on ClawHub](https://clawhub.ai/sgillen/sf-civic-digest) <br>
- [SF Districts Reference](references/sf-districts.md) <br>
- [SF Build Timelines Reference](references/sf-build-timelines.md) <br>
- [SF Legistar RSS Feed](https://sfgov.legistar.com/Feed.ashx?M=C&ID=17442&GUID=EEE85B7C-1A1C-4A56-873E-355A0A0DE5C3&Mode=All&Format=rss) <br>
- [SF Open Data Socrata API](https://data.sfgov.org/resource/{id}.json?$where=supervisor_district=) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown narrative reports, inline shell commands, and JSON data from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are synthesized by the agent from script output and user profile context.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
