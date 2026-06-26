## Description: <br>
Automatically extracts structured long-term knowledge from OpenClaw conversation sessions, filters low-value content, clusters topics, and tracks follow-up status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mashirops](https://clawhub.ai/user/Mashirops) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to distill conversation history into durable memory artifacts, including topic cards, domain summaries, pending-task reports, and cleanup recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can copy and persist private conversation history, including deleted or reset session variants. <br>
Mitigation: Review the scripts before installing, exclude sensitive and deleted/reset sessions, and inspect or delete generated chunks, tasks, cards, and reports that may contain private content. <br>
Risk: Hardcoded workspace paths and weak scoping can direct processing toward the wrong local data. <br>
Mitigation: Change the hardcoded paths to a scoped workspace owned by the intended user before running any scripts. <br>
Risk: Cron-based execution can create ongoing capture of new conversation data. <br>
Mitigation: Do not enable scheduled runs until the workspace scope, retention expectations, and generated outputs have been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Mashirops/subagent-distiller) <br>
- [Skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON files with command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates conversation slices, cursor state, extraction tasks, topic cards, domain summaries, cleanup reports, and pending-task reports in the configured workspace.] <br>

## Skill Version(s): <br>
3.0.1 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
