## Description: <br>
Batch-generates customer-support reply templates with consistent empathy statements, action statements, boundary language, and escalation prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Support teams, customer-success teams, and agents use this skill to turn issue types, brand tone, and prohibited phrasing into reviewable Markdown macro drafts with clear escalation and risk notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated support replies can contain incorrect commitments, unsuitable wording, or policy-sensitive guidance if used without review. <br>
Mitigation: Review all generated macros before customer use and keep boundary, escalation, and risk notes in the final workflow. <br>
Risk: Customer inputs may include personal or sensitive information. <br>
Mitigation: Redact sensitive customer data where possible before using the skill or running the local helper. <br>
Risk: The optional Python helper reads chosen inputs and can write an output file. <br>
Mitigation: Run it only on input files and output paths intentionally selected by the operator. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/support-macro-crafter) <br>
- [Publisher profile](https://clawhub.ai/user/52YuanChangXing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON, with optional local shell command usage for file-based generation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include template directories, standard structure, empathy statements, action statements, escalation cues, risk notices, missing information, and next steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
