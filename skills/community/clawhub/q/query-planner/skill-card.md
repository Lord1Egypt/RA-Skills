## Description: <br>
Plans structured search queries by decomposing complex tasks into identity, event, action, and counter-evidence query categories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[z1one0415](https://clawhub.ai/user/z1one0415) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill before web search or multi-step analysis to turn a complex task into a consistent query plan for downstream search and review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated counter-evidence and controversy-oriented search terms may be sensitive or overbroad for the user's task. <br>
Mitigation: Review generated queries for relevance, neutrality, and sensitivity before using them in downstream search or analysis. <br>
Risk: The skill creates query ideas but does not verify facts or judge source credibility. <br>
Mitigation: Use separate retrieval, source evaluation, and human review before relying on search results produced from the planned queries. <br>


## Reference(s): <br>
- [Query Patterns](references/query-patterns.md) <br>
- [Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON query plan] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes identity_queries, event_queries, action_queries, and counter_queries; counter_queries must contain at least two entries.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
