## Description: <br>
Multi-date flight price comparison assistant that uses flyai search-flight to discover candidate flights, compare up to seven dates, apply persona-based travel constraints, and explain recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangxchao](https://clawhub.ai/user/zhangxchao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-planning agents use this skill to compare one-way flight prices across nearby dates, filter results for family, business, student, senior, or honeymoon trips, and choose explainable booking candidates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores local route preferences and travel-selection history, which can reveal travel patterns. <br>
Mitigation: Review and periodically clear assets/history.json and assets/preferences.json if long-term travel-pattern retention is not desired. <br>
Risk: The skill may run flyai CLI commands using user-provided route, date, and flight-number values and may require an API key. <br>
Mitigation: Keep the documented input validation in place, reject unsafe shell characters before execution, and verify flyai-cli/API-key setup before use. <br>
Risk: Recommendations and booking links can influence real travel purchases. <br>
Mitigation: Confirm price, itinerary, transfer, visa, baggage, and refund details with the booking provider before purchasing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangxchao/super-flight) <br>
- [flyai search-flight reference](references/search-flight.md) <br>
- [FlyAI Open Platform](https://flyai.open.fliggy.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown recommendations with tables, CLI command invocations, filter notices, price matrices, and booking links when returned by flyai.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses flyai search-flight responses as the source for prices, times, durations, and booking links; compares at most 7 dates and up to 2 locked flights per matrix.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
