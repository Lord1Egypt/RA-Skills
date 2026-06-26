## Description: <br>
Gives agents real-time and archival access to front-page headlines across 20 countries for breaking news, current events, and comparative media analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sfkislev](https://clawhub.ai/user/sfkislev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to inspect current and historical front-page news snapshots across countries, compare media framing, and ground answers about breaking or recent events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: News-related prompts may cause the agent to contact thehear.org and use returned headlines, links, and AI summaries. <br>
Mitigation: Expect public API access during use and avoid treating the returned snapshot as private or independently verified. <br>
Risk: Returned headlines and AI-generated overviews can reflect incomplete coverage, editorial framing, or interpretive summarization. <br>
Mitigation: Use the output as a starting snapshot, distinguish raw headlines from AI overviews, and consult additional sources for high-stakes claims. <br>
Risk: Archive and daily overview calls may be constrained by timestamp, date format, and range limits. <br>
Mitigation: Use UTC timestamps, YYYY-MM-DD date ranges, and keep daily-overview requests within the documented 7-day limit. <br>


## Reference(s): <br>
- [REFERENCE.md](REFERENCE.md) <br>
- [The News ClawHub listing](https://clawhub.ai/sfkislev/the-news) <br>
- [The Hear API country-view example](https://www.thehear.org/api/country-view/germany) <br>
- [The Hear web interface example](https://www.thehear.org/en/germany) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown or concise text summaries backed by JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a public, read-only API; returned AI overviews should be treated as interpretive context, not verified facts.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
