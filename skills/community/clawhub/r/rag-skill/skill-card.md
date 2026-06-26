## Description: <br>
Queries a Prana-hosted RagFlow knowledge base for RAG-related content and returns the remote agent response. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaochengzhen](https://clawhub.ai/user/xiaochengzhen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to send natural-language RAG lookup questions to a Prana-hosted RagFlow knowledge-base agent. The release describes knowledge-base content focused on artist profiles and intersections of technology and art. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user queries and an API-key-authenticated request to the Prana service. <br>
Mitigation: Install only if the publisher and claw-uat.ebonex.io Prana service are trusted, and avoid including secrets or private documents in queries. <br>
Risk: The required PRANA_SKILL_API_FLAG may persist on shared machines if configured globally. <br>
Mitigation: Prefer a temporary PRANA_SKILL_API_FLAG on shared machines. <br>
Risk: Purchase-history URL access can expose account-related links. <br>
Mitigation: Only allow purchase or history URL access when that account-related link is explicitly needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaochengzhen/rag-skill) <br>
- [Prana service](https://claw-uat.ebonex.io/) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON responses and Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PRANA_SKILL_API_FLAG and sends user queries to claw-uat.ebonex.io; purchase-history URL access is optional and should be explicitly requested.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
