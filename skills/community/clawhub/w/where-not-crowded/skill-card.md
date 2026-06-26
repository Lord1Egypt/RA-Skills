## Description: <br>
去哪不挤 helps users decide whether a default holiday travel choice is worth it and recommends less crowded, higher-value alternatives with a direct decision report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keyikoi](https://clawhub.ai/user/keyikoi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users invoke this skill before Chinese holiday travel to compare a likely default destination against better alternatives by crowd risk, cost, travel window, and overall value. It produces an actionable decision report rather than a detailed itinerary or booking workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes Markdown and HTML reports into the working directory, including a fixed latest-report HTML filename. <br>
Mitigation: Run it in a workspace where generated travel report files are expected, and rename or archive prior latest-report output before rerunning if it must be preserved. <br>
Risk: The skill uses bundled frames rather than live pricing, live crowd data, or external APIs. <br>
Mitigation: Treat crowd and cost estimates as decision guidance and verify current prices, availability, entry rules, and booking details before travel. <br>


## Reference(s): <br>
- [Report Template](references/report_template.md) <br>
- [Example Report](references/example_report.md) <br>
- [Widget Data Spec](references/widget_data_spec.md) <br>
- [Destination Frames](assets/destination_frames.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/keyikoi/where-not-crowded) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown report plus local Markdown and HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Also writes a fixed latest HTML alias; uses bundled destination frames and does not use live pricing, live crowd data, credentials, or external APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
