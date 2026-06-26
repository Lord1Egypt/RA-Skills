## Description: <br>
Encodes open-ended survey responses into themes, sentiment, and tags, and generates a reviewable coding manual. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, user researchers, and analysts use this skill to organize open-ended survey responses into a structured, reviewable coding workflow with sample overview, theme coding, sentiment distribution, coding rules, difficult samples, and follow-up analysis suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Survey responses may contain respondent identifiers or sensitive personal information. <br>
Mitigation: De-identify respondent data before use and review generated coding outputs before sharing them. <br>
Risk: The local helper reads user-selected files and can write a report to a user-selected output path. <br>
Mitigation: Prefer stdout or dry-run when reviewing behavior, and run only on files intentionally selected for analysis. <br>
Risk: Changing the bundled specification to broader audit modes can expand local-file inspection. <br>
Mitigation: Do not change spec.json to directory_audit, pattern_audit, or skill_audit unless broader local-file inspection is intended. <br>
Risk: Theme and sentiment coding can be mistaken for statistically representative conclusions. <br>
Mitigation: Treat results as qualitative organization aids and do not generalize small or biased samples as population-level findings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/survey-response-coder) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>
- [Output template](resources/template.md) <br>
- [Structured specification](resources/spec.json) <br>
- [Smoke test](tests/smoke-test.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report or JSON from a local Python helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can read user-selected survey files and write a user-selected report; supports dry-run review.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
