## Description: <br>
Digital construction foreman: crew management, work acceptance, work logs, hidden works acts, safety, schedules and executive documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raaipro](https://clawhub.ai/user/raaipro) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External construction foremen, site managers, contractors, technical customers, and construction business owners use this skill to plan crews, inspect work against standards, maintain site logs and hidden-works acts, coordinate subcontractors and supplies, and prepare executive documentation. It is intended for Russian-language construction workflows where a responsible human foreman remains accountable for site facts, safety, and legal acceptance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shell scripts are included for local installation, packaging, and smoke testing. <br>
Mitigation: Review or fix the shell scripts before running them, and run them only in an environment where local file-copying and archive creation are expected. <br>
Risk: Configuration files may contain construction site, client, team, supplier, schedule, or contact details. <br>
Mitigation: Avoid entering unnecessary sensitive client or site data into config files, and limit stored details to what the foreman workflow needs. <br>
Risk: Safety, legal, standards-based, and site-acceptance outputs can affect real construction decisions. <br>
Mitigation: Verify all safety, legal, standards-based, and acceptance outputs with a qualified human responsible for the actual site before relying on them. <br>


## Reference(s): <br>
- [Foreman Pro ClawHub Release](https://clawhub.ai/raaipro/raai-foreman-pro) <br>
- [Publisher Profile](https://clawhub.ai/user/raaipro) <br>
- [README](artifact/README.md) <br>
- [Onboarding Guide](artifact/docs/onboarding.md) <br>
- [Anti-Fail Guide](artifact/docs/anti-fail.md) <br>
- [ROI Guide](artifact/docs/roi.md) <br>
- [Quick Start Examples](artifact/examples/quick-start.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown with checklists, tables, document templates, configuration fields, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include Russian-language construction plans, acceptance checklists, safety notes, work-log entries, hidden-works acts, Gantt-style schedules, subcontractor coordination notes, and foreman reports.] <br>

## Skill Version(s): <br>
3.5.4 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
