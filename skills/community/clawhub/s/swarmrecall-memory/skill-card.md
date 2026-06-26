## Description: <br>
Conversational memory persistence with semantic search and session tracking via the SwarmRecall API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[waydelyle](https://clawhub.ai/user/waydelyle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let an agent store, search, update, and recall conversational memories across sessions through the SwarmRecall API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory content and session summaries may include personal or sensitive information stored on SwarmRecall servers. <br>
Mitigation: Obtain user consent before storing user-provided content and avoid sending secrets or sensitive data unless the user explicitly approves. <br>
Risk: The SwarmRecall API key grants access to the agent's memory operations. <br>
Mitigation: Keep SWARMRECALL_API_KEY in the environment and do not write the key to disk or shared files without user consent. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/waydelyle/swarmrecall-memory) <br>
- [Publisher Profile](https://clawhub.ai/user/waydelyle) <br>
- [SwarmRecall Homepage](https://www.swarmrecall.ai) <br>
- [SwarmRecall API Base URL](https://swarmrecall-api.onrender.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON API request examples and memory recall text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SWARMRECALL_API_KEY or self-registration; memory content is stored on SwarmRecall servers.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
