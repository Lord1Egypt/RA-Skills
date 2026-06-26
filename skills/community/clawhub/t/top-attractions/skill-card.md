## Description: <br>
Discovers popular and highly rated attractions in a city using FlyAI CLI data, then presents POIs with ticket prices, opening hours, and booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travel users and agent operators use this skill to retrieve current attraction recommendations for a city through the FlyAI CLI. It formats CLI results into concise travel guidance with prices, hours, ratings, and booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install an unpinned global FlyAI CLI through npm. <br>
Mitigation: Review or perform the CLI installation yourself, and prefer a pinned or sandboxed install before use. <br>
Risk: FlyAI/Fliggy may receive attraction queries, and the optional local execution log can retain raw travel queries. <br>
Mitigation: Use the skill only when that data sharing is acceptable, and delete or disable .flyai-execution-log.json for sensitive travel requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/top-attractions) <br>
- [Output templates](references/templates.md) <br>
- [Scenario playbooks](references/playbooks.md) <br>
- [Fallback handling](references/fallbacks.md) <br>
- [Execution log schema](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown response with comparison tables, booking links, and optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results should be derived from FlyAI CLI output, include booking links when available, and avoid raw JSON in the final user response.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
