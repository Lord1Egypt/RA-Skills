## Description: <br>
Helps company teams plan group outing destinations by collecting member preferences, analyzing activity, budget, timing, and accessibility needs, and querying flyai for destination details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shiguan1](https://clawhub.ai/user/shiguan1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and team coordinators use this skill to collect group outing requirements, compare destination options, and produce a shareable recommendation report for company team-building activities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Team outing preferences may include personal names, accessibility needs, travel constraints, or other sensitive information. <br>
Mitigation: Use summarized or anonymized preferences where possible and avoid storing names or sensitive needs unless necessary. <br>
Risk: Travel queries are sent to the flyai CLI/provider. <br>
Mitigation: Confirm the installer trusts the flyai provider and is comfortable with sending travel queries to that service before use. <br>
Risk: The generated HTML report may contain sensitive team preferences or planning details. <br>
Mitigation: Review the HTML before sharing it and delete ~/team-outing-recommendation.html when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shiguan1/team-outing-planner) <br>
- [README](README.md) <br>
- [Preference collection template](preferences-template.md) <br>
- [HTML report template](html-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown recommendations plus a local HTML report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May query travel data through flyai and generate ~/team-outing-recommendation.html.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
