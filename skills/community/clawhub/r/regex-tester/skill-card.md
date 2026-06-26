## Description: <br>
RegexTester helps users test, debug, and generate regular expressions, including match checks, capture groups, replacements, and common pattern generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crossallen](https://clawhub.ai/user/crossallen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to validate regular expressions, inspect matches and capture groups, perform text replacements, and generate common regex patterns during development or data-cleaning work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided regex patterns or very large inputs may cause long-running or stalled local execution. <br>
Mitigation: Test complex patterns on small inputs first and avoid pathological expressions or unexpectedly large text. <br>
Risk: Sensitive text pasted into commands may appear in terminal history or command output. <br>
Mitigation: Avoid using secrets or confidential data as regex test input unless local command exposure is acceptable. <br>
Risk: Adapting shell examples that expand file contents can be unsafe with untrusted text. <br>
Mitigation: Quote shell arguments carefully and do not substitute untrusted shell text into commands. <br>


## Reference(s): <br>
- [RegexTester ClawHub release](https://clawhub.ai/crossallen/regex-tester) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Console text with regex patterns, match details, replacement results, and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with user-provided regex patterns and text inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
