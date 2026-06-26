## Description: <br>
Converts PRDs, interface documentation, and requirements specifications into acceptance, integration, testing, go-live, boundary, and open-question checklists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product managers, QA engineers, and release reviewers use this skill to turn PRDs, API/interface docs, and scope notes into reviewable acceptance, integration, test, and launch checklists with explicit pending questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input specifications or requirements may contain secrets, sensitive personal data, or proprietary details. <br>
Mitigation: Provide only the files needed for the checklist task and redact unnecessary sensitive content before use. <br>
Risk: The helper can write a report to the requested output path. <br>
Mitigation: Choose output paths deliberately and use dry-run or stdout review when you do not want a file written. <br>
Risk: Generated checklists can be mistaken for completed testing or approval evidence. <br>
Mitigation: Treat outputs as review drafts and verify test execution, approvals, and launch readiness separately. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/52YuanChangXing/spec-to-checklist) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Checklist template](artifact/resources/template.md) <br>
- [Structured skill configuration](artifact/resources/spec.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown or JSON checklist/report content, with optional file output when an output path is provided] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local Python helper supports file, directory, CSV/TSV, and pattern-scan inputs; outputs should be treated as review drafts rather than proof that testing passed.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
