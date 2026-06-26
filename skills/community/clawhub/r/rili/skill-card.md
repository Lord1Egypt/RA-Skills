## Description: <br>
rili provides local Gregorian and Chinese lunar calendar lookups, including weekdays, month views, traditional lunar festivals, zodiac information, and Gregorian-to-lunar conversion through a bundled Node script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jvy](https://clawhub.ai/user/jvy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use rili to answer Chinese-language date questions, inspect monthly calendars, find traditional lunar festival dates, and convert between Gregorian and lunar dates. It is intended for date lookup and explanation, not calendar event management or shared calendar integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a bundled local Node script, and server-resolved GitHub provenance is unavailable for this version. <br>
Mitigation: Review the bundled script and file hashes before installing in environments that require strong publisher provenance. <br>
Risk: Lunar calendar conversion depends on Node Intl Chinese calendar support and is documented for common question-answering rather than astronomical precision or region-specific folk dates. <br>
Mitigation: Verify high-stakes or specialized calendar results against an authoritative calendar source, and avoid using this skill for event creation, reminders, or shared calendar workflows. <br>


## Reference(s): <br>
- [ClawHub rili skill page](https://clawhub.ai/jvy/rili) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Chinese-language text or JSON from local Node CLI commands, usually summarized by the agent in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with Node; evidence reports no accounts, secrets, network access, or persistence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
