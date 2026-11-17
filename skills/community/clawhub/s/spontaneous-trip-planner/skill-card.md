## Description:

Helps an agent collect travel preferences and generate three seasonal trip plans with destination, route, budget, transportation, attraction, hotel, and booking-link recommendations using Feizhu/flyai travel tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenshinan](https://clawhub.ai/user/chenshinan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to turn departure city, travel scenario, group size, budget/time/quality preferences, and season into concise itinerary recommendations. It is especially suited to Chinese-language leisure travel planning that needs Feizhu/flyai searches for points of interest, flights, hotels, and booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may open a popup and collect trip details such as departure city, travel scenario, group size, and travel preferences.

Mitigation: Confirm the user wants itinerary help before invoking the skill, especially when travel is mentioned casually.

Risk: Destination and preference queries may be sent to flyai travel tools.

Mitigation: Avoid entering sensitive personal details beyond what is needed for travel planning and review returned booking links before use.

Risk: The skill is best suited for Chinese-language travel planning and may be less effective for other travel contexts.

Mitigation: Set user expectations about language and regional coverage before relying on the itinerary.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown itinerary recommendations with travel-search command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces three recommended plans and may include booking links returned by travel tools.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
