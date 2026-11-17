## Description:

AI-driven event forecasting skill. Collects multi-source data, cross-validates facts, maps future scenarios with probabilities, and delivers actionable recommendations for investors, managers, and policymakers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onecore-me](https://clawhub.ai/user/onecore-me)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts, investors, managers, and policymakers use this skill to turn an uncertain event into multiple scenario paths with fact-confidence ratings, probability estimates, trigger milestones, and role-specific action guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Forecasts can be mistaken for financial, policy, or operational advice.

Mitigation: Treat outputs as structured decision support; verify current sources and consult qualified judgment before acting.

Risk: The README install command uses an unpinned npx invocation.

Mitigation: Prefer a pinned and verified ClawHub installer version before installing or distributing the skill.

## Reference(s):

- [Scenario Forecaster ClawHub release](https://clawhub.ai/onecore-me/skills/scenario-forecaster)
- [API reference](docs/api_reference.md)
- [Customization guide](docs/customization_guide.md)
- [Prompt template](skill/prompt.md)
- [Fed rate forecast example](examples/output_fed_rate.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown forecast report with tables, scenario paths, probability estimates, trigger milestones, and role-specific recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces 3-5 scenario paths and may describe an API-style JSON response shape for integrations.]

## Skill Version(s):

1.3.0 (source: server release evidence and target metadata; artifact YAML lists 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
