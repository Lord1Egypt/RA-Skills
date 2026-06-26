## Description: <br>
Manage Vikunja projects and tasks (overdue/due/today), mark done, and get quick summaries via the Vikunja API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tmigone](https://clawhub.ai/user/tmigone) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Vikunja users use this skill to query projects and tasks, review overdue or due-today work, and explicitly mark selected tasks done from an agent-assisted shell workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill needs credentials that can access a Vikunja account. <br>
Mitigation: Install only when that account access is acceptable; prefer revocable or least-privileged JWT credentials when available and store credentials carefully. <br>
Risk: The configured Vikunja endpoint determines where credentials and task requests are sent. <br>
Mitigation: Verify VIKUNJA_URL before use and ensure it points to the intended Vikunja instance. <br>
Risk: The done command changes task state. <br>
Mitigation: Review task IDs before invoking the done command so only intended tasks are marked complete. <br>


## Reference(s): <br>
- [Vikunja](https://vikunja.io/) <br>
- [Vikunja Filters Documentation](https://vikunja.io/docs/filters/) <br>
- [ClawHub Skill Page](https://clawhub.ai/tmigone/vikunja-fast) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and plain-text task summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, VIKUNJA_URL, and Vikunja authentication through VIKUNJA_TOKEN or username/password fallback.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
