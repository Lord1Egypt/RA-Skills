## Description: <br>
Query and organize China travel information for flights and trains, including schedules, prices, duration, stops, and summary tables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LiuBroth](https://clawhub.ai/user/LiuBroth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and travel planners use this skill to query China domestic flight and train options, normalize visible schedules and prices, and summarize the best choices with caveats about source quality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel result pages may expose itinerary details or other personal travel context selected by the user. <br>
Mitigation: Only connect filtered travel result pages intended for summarization, and avoid exposing passenger or payment details unnecessarily. <br>
Risk: Prices, inventory, and availability can change or depend on booking site state, region, login status, seat class, or cabin. <br>
Mitigation: Verify final fares and availability on the booking site before acting. <br>


## Reference(s): <br>
- [Traffic Query Sources](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summaries with compact option lists and caveats] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries may include schedules, prices, duration, stops, seat or cabin details, source notes, and partial-result labels.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata and README) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
