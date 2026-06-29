## Description: <br>
Professional home inspection for Taiwan residential properties with structured checklists, severity grading, Taiwan standards references, and formal report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tsaitepiao-alt](https://clawhub.ai/user/tsaitepiao-alt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users such as home buyers, property managers, and inspection professionals use this skill to plan Taiwan residential inspections, grade findings, and generate formal markdown reports. <br>

### Deployment Geography for Use: <br>
Taiwan <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may contain sensitive property location and condition details. <br>
Mitigation: Store and share reports carefully, limit access to intended recipients, and avoid adding unnecessary personal or location details. <br>
Risk: The optional analytics command may record usage when run. <br>
Mitigation: Avoid running the analytics command or confirm how ClawHub analytics are handled in the target environment. <br>
Risk: Inspection guidance may identify structural concerns that require licensed professional judgment. <br>
Mitigation: Refer structural safety findings to a qualified structural engineer before relying on them for transaction or occupancy decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tsaitepiao-alt/taiwan-home-inspection) <br>
- [Inspection checkpoints](artifact/references/checkpoints.md) <br>
- [Defect grading criteria](artifact/references/defects.md) <br>
- [Taiwan building standards](artifact/references/standards.md) <br>
- [Report template](artifact/assets/report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance and reports, with JSON input for report generation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; generated reports may include sensitive property details.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
