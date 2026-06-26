## Description: <br>
Periodically audit all workspace skills, learnings, memory, and configuration files to recommend refactoring, new skill ideas, and workflow improvements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omaression](https://clawhub.ai/user/omaression) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace maintainers use this skill to review agent skills, memory, and configuration files for stale content, overlap, workflow gaps, and actionable improvement recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads private workspace memory and configuration files and may summarize sensitive information through model providers. <br>
Mitigation: Run a manual dry run first, restrict readable files, and add redaction or exclusions before enabling scheduled audits. <br>
Risk: The skill can send derived audit results to Telegram on a schedule without clear per-run consent. <br>
Mitigation: Verify the Telegram destination, confirm retention and disable controls, and avoid enabling the cron job until those controls are clear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/omaression/skill-enhancer) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown recommendations, JSON audit artifacts, Python helper scripts, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations are advisory and may be formatted for Telegram delivery.] <br>

## Skill Version(s): <br>
1.0.0-alpha (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
