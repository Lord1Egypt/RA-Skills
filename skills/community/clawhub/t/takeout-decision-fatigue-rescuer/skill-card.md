## Description:

Helps Chinese-language users choose takeout by collecting budget, dietary restrictions, and hunger level, then narrowing options to a Top 3 set of restaurant and dish recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangyang7-star-jpg](https://clawhub.ai/user/yangyang7-star-jpg)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill when they are stuck choosing a takeout meal. The agent asks for budget, dietary restrictions, and hunger level, then returns concise Top 3 recommendations with prices and reasons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad Chinese-language phrases about not knowing what to eat.

Mitigation: Use it when the user is asking for meal or takeout decision help, and confirm intent if the phrase could refer to a different decision.

Risk: The skill does not itself provide direct access to current delivery app inventory, prices, ratings, or availability.

Mitigation: Use live platform data when the agent has access to it; otherwise disclose that recommendations are based on common takeout categories and ask the user to verify details in the delivery app.

Risk: Generated recommendations can be misleading if they ignore dietary restrictions or user-provided constraints.

Mitigation: Collect budget, dietary restrictions, and hunger level before ranking options, and tie each recommendation reason directly to those inputs.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/Yangyang7-star-jpg/skills/tree/main/takeout-decision-fatigue-rescuer)
- [ClawHub skill page](https://clawhub.ai/yangyang7-star-jpg/skills/takeout-decision-fatigue-rescuer)
- [ClawHub publisher profile](https://clawhub.ai/user/yangyang7-star-jpg)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with a structured Top 3 recommendation list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations should be grounded in the user's budget, dietary restrictions, and hunger level; if live delivery data is unavailable, the agent should disclose that recommendations are based on common takeout categories.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
