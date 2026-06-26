## Description: <br>
Helps OpenClaw users diagnose and reduce token consumption and API costs through context control, model routing, monitoring, cleanup, and scheduled task tuning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taod7062-a11y](https://clawhub.ai/user/taod7062-a11y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to identify token and API cost drivers, tune context, model, and workflow settings, and set up ongoing monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cleanup guidance may delete local OpenClaw workspace or memory files if commands are run without review. <br>
Mitigation: Require a dry run or explicit file listing, confirm backups, and approve exact paths before running deletion commands. <br>
Risk: Aggressive compaction or low-cost model routing may reduce context quality for complex tasks. <br>
Mitigation: Apply changes incrementally, compare task outputs after each change, and reserve stronger models for complex analysis or high-impact work. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes diagnostic steps, cleanup guidance, model routing suggestions, and monitoring recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
