## Description: <br>
AI木工大师 helps users learn woodworking joinery, tools, machinery, wood selection, safety, finishing, and project planning, and can generate interactive HTML reports with steps, tool lists, precision requirements, safety notes, buying advice, and practical tips. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to answer woodworking questions, generate topic-specific woodworking reports, compare techniques and materials, and receive safety-aware guidance for projects from beginner to advanced levels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local Python script that creates an HTML report file. <br>
Mitigation: Install only if local report generation is acceptable, and review the generated file before sharing or relying on it. <br>
Risk: Custom output paths can write the report to a user-selected destination. <br>
Mitigation: Use the default report filename or choose custom output paths deliberately. <br>
Risk: Tool and brand buying advice may be region-specific. <br>
Mitigation: Validate recommendations against local availability, regulations, safety standards, and project needs before purchase. <br>
Risk: Woodworking and power-tool guidance can involve physical safety hazards. <br>
Mitigation: Follow the skill's safety reminders, use appropriate PPE, and defer to qualified instruction and manufacturer manuals for hazardous operations. <br>


## Reference(s): <br>
- [Woodworking Knowledge Base](references/woodworking_knowledge.md) <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/woodworking-master) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance, files] <br>
**Output Format:** [Markdown-style response text plus a generated interactive HTML report file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes woodworking_report.html by default and supports topic listing, index, detailed-topic, and general-topic report modes.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
