## Description:

Find where to stream any movie or TV show in the US using the WhereCanIWatch.tv API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samthewise2855](https://clawhub.ai/user/samthewise2855)

### License/Terms of Use:


## Use Case:

External users ask an agent where a movie or TV show is available to watch in the US, compare free, subscription, rental, and purchase options, and filter results by their streaming subscriptions when provided.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Search titles and any subscription names provided by the user are sent to WhereCanIWatch.tv.

Mitigation: Avoid entering sensitive viewing preferences or subscription details unless sharing them with the service is acceptable.

Risk: Availability is documented as US-only, so answers may be inaccurate for users in other regions.

Mitigation: State the US-region limitation when presenting results and avoid applying the results to other countries.

## Reference(s):

- [WhereCanIWatch skill page](https://clawhub.ai/samthewise2855/skills/wherecaniwatch)
- [WhereCanIWatch.tv](https://www.wherecaniwatch.tv/)
- [WhereCanIWatch search API](https://www.wherecaniwatch.tv/api/search?q={title})
- [WhereCanIWatch watch API](https://www.wherecaniwatch.tv/api/watch/{slug}.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown answer with watch links and concise availability details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should lead with the best option, include one or two alternatives, and link to the full WhereCanIWatch page.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
