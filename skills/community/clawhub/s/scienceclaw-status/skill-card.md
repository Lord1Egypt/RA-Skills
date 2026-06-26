## Description: <br>
Check the status of a ScienceClaw agent: journal stats, recent investigations, knowledge graph size, and activity summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fwang108](https://clawhub.ai/user/fwang108) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ScienceClaw users use this skill to inspect a local ScienceClaw agent's memory, activity, journal entries, active investigations, topics, and health status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can surface private research activity from journal entries, topics, and graph searches. <br>
Mitigation: Review the generated status output before sharing it outside the trusted workspace. <br>
Risk: The skill invokes a local ScienceClaw memory CLI and depends on the user's local ScienceClaw installation. <br>
Mitigation: Install and run it only in environments where the local ScienceClaw installation is expected and trusted. <br>
Risk: ANTHROPIC_API_KEY appears in the skill metadata even though this status workflow does not require exposing it. <br>
Mitigation: Do not expose ANTHROPIC_API_KEY for this status skill unless another trusted ScienceClaw component separately requires it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fwang108/scienceclaw-status) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and an existing local ScienceClaw installation.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
