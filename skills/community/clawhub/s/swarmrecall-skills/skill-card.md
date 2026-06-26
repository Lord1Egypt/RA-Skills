## Description: <br>
SwarmRecall Skills helps agents register, list, and query installed skills through the SwarmRecall API for task-relevant recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[waydelyle](https://clawhub.ai/user/waydelyle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent developers and operators use this skill to keep an external registry of agent capabilities and retrieve skill suggestions that match the current task context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Skill metadata and task descriptions may be sent to SwarmRecall for registration and suggestion queries. <br>
Mitigation: Use explicit SwarmRecall commands, avoid sensitive project details in suggestion queries, and get user consent before storing personal or sensitive information. <br>
Risk: The API key grants access to the agent's SwarmRecall data. <br>
Mitigation: Keep SWARMRECALL_API_KEY private, store it only as an environment variable, and do not write it to disk without user consent. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/waydelyle/swarmrecall-skills) <br>
- [SwarmRecall homepage](https://www.swarmrecall.ai) <br>
- [SwarmRecall API service](https://swarmrecall-api.onrender.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, API calls] <br>
**Output Format:** [Markdown instructions with endpoint descriptions and JSON request examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SWARMRECALL_API_KEY for authenticated requests and may use SWARMRECALL_API_URL to override the default API host.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
