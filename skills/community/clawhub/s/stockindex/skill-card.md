## Description: <br>
Queries minute-level quotes for major mainland China stock indices, including the SSE Composite, SZSE Component, ChiNext, CSI 300, and SSE STAR 50 indices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to answer current mainland China market-index questions and summarize index points, previous close, opening price, and minute-level trends from JisuAPI data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a JisuAPI key for stock-index requests. <br>
Mitigation: Store JISU_API_KEY in the agent environment or secret manager and avoid exposing it in prompts, logs, or shared transcripts. <br>
Risk: Live index data can be mistaken for investment advice or used outside the intended market scope. <br>
Mitigation: Use the skill only for mainland China index quote retrieval and summarize results as market data, not recommendations. <br>
Risk: Responses depend on a third-party API and may fail or return business errors. <br>
Mitigation: Surface the structured error JSON to the user and retry or verify against another source before relying on time-sensitive market data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/stockindex) <br>
- [JisuAPI stock index documentation](https://www.jisuapi.com/api/stockindex/) <br>
- [JisuAPI homepage](https://www.jisuapi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON responses from the stock-index API, with Markdown usage guidance and shell examples in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a JISU_API_KEY environment variable; returns structured error JSON for request, HTTP, JSON parsing, and API errors.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
