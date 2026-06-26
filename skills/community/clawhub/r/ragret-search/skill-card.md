## Description: <br>
Searches a RAGret knowledge-base service for semantic retrieval with provenance when the user intends RAGret-backed search rather than local files or open-web search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sugarsong404](https://clawhub.ai/user/sugarsong404) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to clarify retrieval scope, list available RAGret indexes, and query a RAGret knowledge base through API calls while preserving source cues from retrieved results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries and retrieved content may be sent to a RAGret service outside the user's control. <br>
Mitigation: Confirm the intended RAGret base URL before retrieval and avoid sending sensitive queries to untrusted services. <br>
Risk: An overbroad API key could expose indexes beyond the intended retrieval scope. <br>
Mitigation: Use a least-privilege RAGRET_API_KEY scoped to the indexes the agent should search. <br>
Risk: Ambiguous search requests could be routed to RAGret when the user meant local files or open-web search. <br>
Mitigation: Ask the user to choose RAGret, open-web search, or local-file search when retrieval scope is unclear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sugarsong404/ragret-search) <br>
- [RAGret repository](https://github.com/SugarSong404/RAGret.git) <br>
- [Publisher profile](https://clawhub.ai/user/sugarsong404) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and retrieved text or JSON result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include explicit source URLs from retrieval output when returned by the RAGret service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
