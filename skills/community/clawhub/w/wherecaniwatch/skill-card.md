## Description: <br>
Find where to stream movies and TV shows in the US using the WhereCanIWatch.tv API, with optional filtering by the user's subscriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samthewise2855](https://clawhub.ai/user/samthewise2855) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users ask an agent where a specific movie or TV show is available in the US. The skill guides the agent to search WhereCanIWatch.tv, compare services and prices, and present the best viewing options. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: Movie or TV title searches and subscription preferences may be sent to WhereCanIWatch.tv during lookup. <br>
Mitigation: Avoid including sensitive personal details in lookup requests and only provide subscription preferences needed for filtering. <br>
Risk: The skill can return provider and WhereCanIWatch links for the user to open. <br>
Mitigation: Review links before opening them and use normal browser caution when following third-party provider pages. <br>
Risk: Availability data is scoped to the US and refreshed daily, so results may not apply to other regions or reflect very recent catalog changes. <br>
Mitigation: Tell users when results are US-specific and verify time-sensitive availability on the linked provider page. <br>


## Reference(s): <br>
- [WhereCanIWatch Search API](https://www.wherecaniwatch.tv/api/search?q={title}) <br>
- [WhereCanIWatch Watch API](https://www.wherecaniwatch.tv/api/watch/{slug}.json) <br>
- [WhereCanIWatch Watch Page](https://www.wherecaniwatch.tv/watch/{slug}) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown response with streaming options and links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a best option, one or two alternatives, prices, quality notes, provider deep links, and a WhereCanIWatch page link.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
