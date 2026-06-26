## Description: <br>
Context-aware recommendations. Learns preferences, researches options, anticipates expectations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to produce personalized recommendations by gathering user context, extracting preferences, researching current options, and ranking candidates against constraints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use prior conversations and memory entries to personalize recommendations, which may surface or retain sensitive preference information. <br>
Mitigation: Use it only when preference memory is acceptable, avoid highly sensitive choices, and review or clear memory where the platform supports it. <br>
Risk: Recommendations may be stale or poorly matched when user context is incomplete or option research is outdated. <br>
Mitigation: Gather at least 3-5 relevant user signals or ask targeted questions, then verify recency and availability before ranking options. <br>


## Reference(s): <br>
- [Recommendation Categories](artifact/categories.md) <br>
- [Where to Find User Context](artifact/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown recommendation summaries with preference signals, ranked candidates, rationale, tradeoffs, and confidence.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include follow-up questions when insufficient user preference signals are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
