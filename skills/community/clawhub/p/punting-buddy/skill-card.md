## Description: <br>
Conversational horse racing analysis for racecard breakdowns, runner comparisons, results checks, odds or value discussion, and punting-style decision support using The Racing API as the default live data source. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anupa-perera](https://clawhub.ai/user/anupa-perera) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to get conversational horse-racing race discovery, racecard analysis, runner comparisons, shortlist discussion, and results checks. It is read-only by default and guides The Racing API credential setup when live data access is requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Racing API credentials could be exposed if a user pastes them into chat. <br>
Mitigation: Store THE_RACING_API_USERNAME and THE_RACING_API_PASSWORD as environment secrets and guide setup without asking the user to reveal credentials in conversation. <br>
Risk: Horse-racing analysis could be mistaken for guaranteed betting advice or automated betting. <br>
Mitigation: Keep the skill read-only by default, frame suggestions as informal analysis, avoid autonomous live betting, and state uncertainty when the evidence is thin. <br>
Risk: Free-plan racecard data may be too limited for strong quantitative claims. <br>
Mitigation: Use The Racing API card as the backbone, avoid fake precision or implied edge claims, and disclose when analysis is only a lightweight card read. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/anupa-perera/punting-buddy) <br>
- [Analysis rubric](references/analysis-rubric.md) <br>
- [Chat output patterns](references/chat-output-patterns.md) <br>
- [Domain model](references/domain-model.md) <br>
- [Safety and modes](references/safety-and-modes.md) <br>
- [Setup](references/setup.md) <br>
- [The Racing API](references/the-racing-api.md) <br>
- [The Racing API OpenAPI spec](https://api.theracingapi.com/openapi.json) <br>
- [Workflow](references/workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Configuration guidance] <br>
**Output Format:** [Conversational Markdown or plain text with concise paragraphs and optional bullets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only horse-racing analysis; live racecards and results require The Racing API credentials supplied through environment variables.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
