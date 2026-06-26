## Description: <br>
Analyze any codebase - architecture, patterns, diagrams, and agent context - so developers can understand repositories quickly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[selvatuple](https://clawhub.ai/user/selvatuple) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Revibe Codes to analyze GitHub repositories, understand architecture and design decisions, inspect file roles and execution flows, and save structured codebase context for follow-on agent work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository URLs and source code are sent to Revibe for analysis and stored for later exploration and re-analysis. <br>
Mitigation: Use the skill only with repositories you are authorized to analyze, and review Revibe privacy terms before using it with private or sensitive code. <br>
Risk: The Revibe API key is required for authentication and is sent with analysis requests. <br>
Mitigation: Store REVIBE_API_KEY in the agent configuration or environment, avoid pasting it into prompts or logs, and rotate it if exposure is suspected. <br>
Risk: Generated repository summaries, diagrams, and agent_context.json may be incomplete or inaccurate. <br>
Mitigation: Review the generated analysis against the repository before relying on it for architecture, security, or implementation decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/selvatuple/revibe) <br>
- [Publisher Profile](https://clawhub.ai/user/selvatuple) <br>
- [Revibe Codes](https://www.revibe.codes) <br>
- [Revibe App](https://app.revibe.codes) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, JSON agent context, shell commands, and optional rendered HTML diagrams.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REVIBE_API_KEY, curl, jq, and git; saves agent_context.json in the working directory.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
