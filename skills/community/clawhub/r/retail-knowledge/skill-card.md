## Description: <br>
Product knowledge Q&A and policy lookup for retail digital employees using the configured store knowledge base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fangwei-frank](https://clawhub.ai/user/fangwei-frank) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Retail teams and digital employee builders use this skill to answer customer and staff questions about products, policies, promotions, store information, membership, and FAQs from a configured knowledge base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can answer from a misconfigured, stale, or overly broad retail knowledge-base file. <br>
Mitigation: Configure it to use only the intended knowledge-base file and review time-sensitive product, promotion, membership, and policy data before deployment. <br>
Risk: Retail Q&A may involve customer or staff personal data during membership lookups or unanswered-query logging. <br>
Mitigation: Avoid storing unnecessary personal data and align membership lookup and gap-digest logging with store privacy rules. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fangwei-frank/retail-knowledge) <br>
- [Answer Style Guide](references/answer-style-guide.md) <br>
- [Conversation Patterns](references/conversation-patterns.md) <br>
- [Knowledge Base Schema Reference](references/kb-schema.md) <br>
- [Knowledge Base Search Strategy](references/search-strategy.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown responses with optional JSON search results from the local knowledge-base search helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Answers should be grounded in the configured knowledge base and use fallback language when matching entries are unavailable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
