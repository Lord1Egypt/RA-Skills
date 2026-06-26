## Description: <br>
Task decomposition and execution framework for Claude that breaks complex work into verified subtasks, plants context anchors to survive compaction, and helps agents keep track of progress. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiajiaoy](https://clawhub.ai/user/jiajiaoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Task Pilot to manage multi-step Claude workflows that need explicit planning, progress checkpoints, context anchors, and recovery after long conversations or compaction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task plans and context anchors may preserve passwords, API keys, private customer data, or other sensitive information in conversation history if users include them. <br>
Mitigation: Avoid placing secrets or sensitive data in task plans, checkpoints, or context anchors; summarize sensitive work without copying confidential values. <br>


## Reference(s): <br>
- [Task Pilot ClawHub listing](https://clawhub.ai/skills/task-pilot) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown task plans, checkpoints, context anchors, recovery notes, and completion summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only workflow guidance; no code execution, credential requests, network access, or local file access requested by the skill.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.1 with no functional changes detected) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
