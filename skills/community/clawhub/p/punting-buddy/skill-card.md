## Description:

Punting Buddy provides conversational horse racing racecard analysis, runner comparisons, upcoming-race and results checks, and read-only punting decision support using The Racing API free plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anupa-perera](https://clawhub.ai/user/anupa-perera)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to get concise, conversational horse-racing racecard breakdowns, runner comparisons, shortlists, and results checks. Agent builders can also use it to guide setup for live The Racing API data while keeping betting-related output read-only by default.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Betting-related analysis can be mistaken for guaranteed advice or automated wagering.

Mitigation: Treat output as read-only decision support, avoid guaranteed claims, and require explicit user intent before discussing paper bets or approval-prep workflows.

Risk: Live race data requires third-party The Racing API credentials.

Mitigation: Use the skill without credentials for setup or workflow explanation, and clearly stop with setup guidance when credentials are missing for live fetches.

Risk: Free-plan racecard data may not support deep historical analysis, advanced metrics, or robust probability modelling.

Mitigation: Frame outputs as conversational card reads, disclose uncertainty, and avoid fake precision such as exact win percentages unless richer evidence is available.

## Reference(s):

- [Punting Buddy ClawHub Skill Page](https://clawhub.ai/anupa-perera/skills/punting-buddy)
- [The Racing API OpenAPI Specification](https://api.theracingapi.com/openapi.json)
- [The Racing API](https://api.theracingapi.com)
- [Analysis Rubric](references/analysis-rubric.md)
- [Chat Output Patterns](references/chat-output-patterns.md)
- [Safety and Modes](references/safety-and-modes.md)
- [Setup](references/setup.md)
- [Workflow](references/workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Conversational text or Markdown with inline setup commands and configuration guidance when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Short, read-only responses by default; expands only when the user asks for deeper analysis.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
