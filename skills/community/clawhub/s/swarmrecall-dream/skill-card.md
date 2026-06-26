## Description: <br>
Agent dreaming - memory consolidation, deduplication, pruning, contradiction resolution, and session summarization via the SwarmRecall API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[waydelyle](https://clawhub.ai/user/waydelyle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to run idle-time SwarmRecall memory maintenance, including deduplicating memories, pruning stale content, resolving contradictions, and summarizing sessions through the SwarmRecall API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and modifies stored agent memories on SwarmRecall servers. <br>
Mitigation: Install only if you trust SwarmRecall with the agent's stored memories and review the disclosed data handling before use. <br>
Risk: Auto-dream settings can enable pruning, merging, or contradiction-resolution operations that change memory state. <br>
Mitigation: Review auto-dream settings before enabling them and prefer explicit confirmation before running state-changing operations. <br>
Risk: The skill requires an API key for authenticated SwarmRecall requests. <br>
Mitigation: Use an API key you control and store it only in the SWARMRECALL_API_KEY environment variable. <br>


## Reference(s): <br>
- [SwarmRecall Dream on ClawHub](https://clawhub.ai/waydelyle/swarmrecall-dream) <br>
- [SwarmRecall homepage](https://www.swarmrecall.ai) <br>
- [SwarmRecall API base](https://swarmrecall-api.onrender.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JSON and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SWARMRECALL_API_KEY for authenticated SwarmRecall requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
