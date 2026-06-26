## Description: <br>
Provides London TfL transit lookups for real-time Tube arrivals, bus predictions, line status, disruptions, journey planning, and route information across London public transport. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brianleach](https://clawhub.ai/user/brianleach) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent operators use this skill to answer London public transport questions, including arrivals, service status, disruptions, route details, and journey planning for TfL modes. <br>

### Deployment Geography for Use: <br>
Global, for London TfL transit data. <br>

## Known Risks and Mitigations: <br>
Risk: Journey searches, station names, coordinates, and the optional TFL_API_KEY may be sent to TfL. <br>
Mitigation: Use a TfL-specific API key, query only necessary travel details, and avoid placing unrelated secrets in the skill-local .env file. <br>
Risk: Live TfL lookups depend on TfL API availability and rate limits. <br>
Mitigation: Configure TFL_API_KEY for higher TfL API limits and verify critical travel decisions against an official TfL source when availability matters. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/brianleach/tfl) <br>
- [Publisher Profile](https://clawhub.ai/user/brianleach) <br>
- [TfL Unified API](https://api.tfl.gov.uk/) <br>
- [TfL API Portal](https://api-portal.tfl.gov.uk/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with optional shell commands and TfL result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live TfL API results, route or stop identifiers, service status, arrival times, disruptions, journey steps, and fare estimates when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
