## Description: <br>
Check visa requirements, application procedures, required documents, and processing times for any destination, covering tourist, business, and transit visas plus related travel booking workflows powered by Fliggy (Alibaba Group). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to answer visa and entry-requirement questions through flyai CLI results, then format concise Markdown answers with booking links when relevant. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install and run an unpinned global travel CLI. <br>
Mitigation: Install only after approving the global npm CLI dependency and run it in an environment appropriate for third-party travel tooling. <br>
Risk: Visa answers and booking-oriented results may be incomplete, outdated, or provider-specific. <br>
Mitigation: Verify visa requirements with official government or consular sources before travel decisions. <br>
Risk: Queries may include sensitive travel details and may be persisted in local execution logs. <br>
Mitigation: Avoid entering passport numbers or highly sensitive details unless necessary, and remove .flyai-execution-log.json if local logs are created. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiejinsong/visa-check) <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, comparison tables, and booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output; responses should include detailUrl booking links when results are shown.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
