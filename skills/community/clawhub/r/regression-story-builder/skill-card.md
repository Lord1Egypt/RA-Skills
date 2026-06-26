## Description: <br>
Generates regression test story sets, risk levels, and priorities from historical issues for regression, testing, and QA workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QA engineers, developers, and release reviewers use this skill to turn historical bug notes, affected modules, and release timing into review-ready regression stories, high-risk scenarios, priorities, triggers, acceptance signals, and follow-up data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill drafts regression plans and should not be treated as evidence that tests were executed. <br>
Mitigation: Review the generated stories and run validation separately before using them as release evidence. <br>
Risk: The helper script can write to a user-selected output path. <br>
Mitigation: Use dry-run or stdout for review first, and choose an output path that is safe to create or overwrite. <br>
Risk: Input may contain bug details, personal data, or sensitive release context. <br>
Mitigation: Provide only intended or redacted input data before generating regression stories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/regression-story-builder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown by default, with optional JSON report output from the local helper script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write a user-chosen local output file when the helper script is used; dry-run or stdout output is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: skill frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
