## Description: <br>
Summarizes completed work, blockers, lessons learned, and next-week plans into reviewable management and execution summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, managers, and operators use this skill to turn weekly task notes, blockers, and plans into a structured Markdown review draft for approval and follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weekly notes may contain sensitive personal, business, or planning information. <br>
Mitigation: Use only intended local input files, redact sensitive content where appropriate, and review the generated summary before sharing it. <br>
Risk: The generated review can be incomplete or misleading if the source notes omit work, blockers, or uncertainty. <br>
Mitigation: Keep source notes attached or traceable and use the skill's confirmation items to resolve gaps before relying on the summary. <br>
Risk: The helper can write an output report when an output path is provided. <br>
Mitigation: Choose the output path deliberately and use dry-run or stdout output when reviewing behavior. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/52YuanChangXing/weekly-review-pilot) <br>
- [Publisher Profile](https://clawhub.ai/user/52YuanChangXing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown review draft with optional local script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can emit markdown or JSON through the bundled helper script; output is intended for human review before sharing.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
