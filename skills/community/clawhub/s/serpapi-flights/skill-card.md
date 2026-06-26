## Description: <br>
Query Google Flights via SerpApi for flight schedules, prices, and cabin class info. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirorab](https://clawhub.ai/user/kirorab) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to look up flight schedules, prices, cabin classes, aircraft types, and route comparisons through SerpApi-backed Google Flights queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Flight lookup requests send route, date, passenger, cabin, and currency query details to SerpApi. <br>
Mitigation: Use a SerpApi key intended for this purpose and avoid submitting sensitive travel details unless this data sharing is acceptable. <br>
Risk: Searches may consume SerpApi quota. <br>
Mitigation: Monitor usage and use account limits appropriate for the deployment. <br>
Risk: Prices and availability returned from Google Flights through SerpApi may differ from airline-direct prices or omit seat availability. <br>
Mitigation: Treat returned fares as lookup guidance and verify final booking details with the airline or booking provider. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kirorab/serpapi-flights) <br>
- [Publisher profile](https://clawhub.ai/user/kirorab) <br>
- [SerpApi](https://serpapi.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Markdown flight tables or raw JSON from a Node.js command-line query.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and a SERPAPI_KEY environment variable; route, date, passenger, cabin, and currency query details are sent to SerpApi.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
