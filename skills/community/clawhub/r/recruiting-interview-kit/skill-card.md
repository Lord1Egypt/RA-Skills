## Description: <br>
Generates interview questions, scoring dimensions, red flags, and interview record templates from job descriptions for recruiting, interview, and hiring workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiters, hiring managers, and interview coordinators use this skill to turn job descriptions, role level, and key competencies into structured interview kits with question banks, scoring dimensions, red flags, interview notes templates, and candidate experience reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recruiting drafts can include biased or legally inappropriate interview questions or scoring criteria if the input is flawed or incomplete. <br>
Mitigation: Use the skill as a drafting aid, review outputs for bias and legal appropriateness, and do not use it to make final hiring decisions. <br>
Risk: Job descriptions and candidate materials may contain personal or sensitive information. <br>
Mitigation: Redact unnecessary candidate personal data before use and keep inputs limited to information needed for interview preparation. <br>
Risk: The optional local script reads input paths and can write an output file selected by the user. <br>
Mitigation: Run the script only on trusted input and output paths, and review generated Markdown or JSON before sharing or using it operationally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/recruiting-interview-kit) <br>
- [Publisher profile](https://clawhub.ai/user/52YuanChangXing) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Output template](artifact/resources/template.md) <br>
- [Structured spec](artifact/resources/spec.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, configuration] <br>
**Output Format:** [Structured Markdown by default, with optional JSON output from the local script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are review-ready drafts based on local input, with explicit missing-information prompts and boundaries against discriminatory questions or final hiring decisions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
