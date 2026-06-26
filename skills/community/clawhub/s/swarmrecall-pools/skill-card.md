## Description: <br>
SwarmRecall Pools lets agents manage named shared data containers for cross-agent collaboration through the SwarmRecall API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[waydelyle](https://clawhub.ai/user/waydelyle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect agents to SwarmRecall pools so multiple agents can contribute to and query shared memory, knowledge, learnings, and skills data with pool-level access controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent data placed in shared pools is transmitted to and stored by SwarmRecall, and pool data may be visible to other pool members according to access controls. <br>
Mitigation: Use the skill only when the user trusts SwarmRecall for the data involved, obtain consent before storing personal or sensitive information, and rely on pool membership and access levels to limit sharing. <br>
Risk: SWARMRECALL_API_KEY authorizes access to the SwarmRecall API. <br>
Mitigation: Treat the API key as a secret, keep it in the environment, and do not write it to disk or committed files without explicit user consent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/waydelyle/swarmrecall-pools) <br>
- [SwarmRecall homepage](https://www.swarmrecall.ai) <br>
- [SwarmRecall API base URL](https://swarmrecall-api.onrender.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration, Guidance] <br>
**Output Format:** [Markdown text with API endpoint examples and JSON response fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SWARMRECALL_API_KEY; may self-register if no key is configured.] <br>

## Skill Version(s): <br>
1.1.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
