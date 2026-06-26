## Description: <br>
Semantic Prospect discovers, qualifies, and enriches high-intent business leads from public forums, Reddit, communities, and web sources using semantic analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simplysemantics](https://clawhub.ai/user/simplysemantics) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External sales teams, SaaS companies, consultants, creators, and AI builders use this skill to turn public web discussions into prioritized lead records for outreach, enrichment, or agent handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prospecting criteria are sent to an external Simply Semantics SaaS provider. <br>
Mitigation: Use a dedicated API key where possible, avoid submitting confidential targeting strategy or private customer data, and review vendor retention and export controls before production use. <br>
Risk: Returned public lead data may be used for outreach subject to source community terms and compliance obligations. <br>
Mitigation: Review each source community's terms of service and apply internal compliance review before using collected leads for outreach. <br>
Risk: New accounts can return synthetic mock leads rather than real prospects. <br>
Mitigation: Pass strategy as brave or llm for real lead discovery and clearly label mock results as test data. <br>


## Reference(s): <br>
- [Semantic Prospect product page](https://www.simplysemantics.com/semantic-prospect.html) <br>
- [ClawHub listing](https://clawhub.ai/simplysemantics/semantic-prospect) <br>
- [Simply Semantics publisher profile](https://clawhub.ai/user/simplysemantics) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, API calls, Guidance] <br>
**Output Format:** [Markdown lead report with JSON API request and response fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMPLY_SEMANTICS_API_KEY. Real lead discovery requires an explicit brave or llm strategy; mock strategy returns synthetic test data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and clawhub.json; SKILL.md frontmatter and CHANGELOG list 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
