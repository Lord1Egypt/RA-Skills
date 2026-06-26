## Description: <br>
Error tracking, correction logging, and pattern detection via the SwarmRecall API for surfacing recurring agent mistakes, corrections, and discoveries as actionable rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[waydelyle](https://clawhub.ai/user/waydelyle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to record agent mistakes, corrections, discoveries, recurring patterns, and promotion candidates through the SwarmRecall API so future sessions can reuse those learnings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send and persist detailed command failures, corrections, discoveries, and other learning records to a third-party service. <br>
Mitigation: Confirm what will be logged before upload and avoid sending raw command output or sensitive repository, terminal, personal, or customer data. <br>
Risk: Shared pools can expose learning records to other pool members. <br>
Mitigation: Use shared pools only when the agent has the expected access and the user has approved sharing the learning data. <br>
Risk: Automatic pattern promotion can turn recurring records into durable best-practice guidance. <br>
Mitigation: Surface promotion candidates to the user for approval before acting on them or recording promoted learnings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/waydelyle/swarmrecall-learnings) <br>
- [SwarmRecall homepage](https://www.swarmrecall.ai) <br>
- [SwarmRecall API base URL](https://swarmrecall-api.onrender.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API Calls, configuration] <br>
**Output Format:** [Markdown instructions with JSON request examples and HTTP endpoint descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the SWARMRECALL_API_KEY environment variable; may self-register for an API key when one is not configured.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
