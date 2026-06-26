## Description: <br>
Knowledge graph with entities, relations, traversal, and semantic search via the SwarmRecall API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[waydelyle](https://clawhub.ai/user/waydelyle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to store, link, traverse, and search structured knowledge graph data through SwarmRecall's hosted API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected knowledge graph content is sent to and stored by SwarmRecall's hosted service. <br>
Mitigation: Require explicit user consent before storing personal or sensitive information externally. <br>
Risk: Shared pool IDs can make entities and relations visible to other pool members. <br>
Mitigation: Confirm the intended pool and access level before writing shared entities or relations. <br>
Risk: Delete operations can remove entities or relations from the knowledge graph. <br>
Mitigation: Confirm entity and relation IDs with the user before deletion. <br>


## Reference(s): <br>
- [SwarmRecall website](https://www.swarmrecall.ai) <br>
- [SwarmRecall API service](https://swarmrecall-api.onrender.com) <br>
- [ClawHub skill listing](https://clawhub.ai/waydelyle/swarmrecall-knowledge) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/waydelyle) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, configuration, text] <br>
**Output Format:** [Markdown guidance with JSON request examples and API endpoint references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SWARMRECALL_API_KEY for authenticated API use; may self-register when the key is absent.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
