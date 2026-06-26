## Description: <br>
A proactive agent that anticipates needs and takes initiative by monitoring context, suggesting actions, and proposing tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[552134926-alt](https://clawhub.ai/user/552134926-alt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to analyze time, market, content, task, and learning context, then generate prioritized suggestions or proposed tasks for proactive workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Background monitoring may observe agent context over time. <br>
Mitigation: Run monitoring only when needed, choose explicit daemon and interval settings, and stop the process when monitoring is no longer required. <br>
Risk: Task and context data may be saved locally. <br>
Mitigation: Review configured output paths before enabling auto-save or daemon mode, and avoid use in sensitive workspaces unless local persistence is acceptable. <br>
Risk: Suggestions for trading, content, tasks, or learning may be incorrect or inappropriate. <br>
Mitigation: Treat outputs as proposals requiring human review, especially for publishing, trading, or external API actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/552134926-alt/shiyi-proactive-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Command-line text and JSON, with local JSON task files and monitoring log lines when persistence features are used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; daemon and auto-save behavior can write task and monitoring data under memory/ paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
