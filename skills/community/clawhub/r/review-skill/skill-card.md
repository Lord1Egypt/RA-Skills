## Description: <br>
Reviews PRs that add or modify Agent Skills, checking structural validity, design quality, and marketplace consistency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to review pull requests that add or modify Agent Skills, with emphasis on structure, design quality, marketplace consistency, and clear reviewer findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes a local review report and may overwrite an existing file if the selected output path already exists. <br>
Mitigation: Choose the output path deliberately and check for an existing file before running when overwriting would matter. <br>
Risk: Review findings can affect skill publication decisions if accepted without inspection. <br>
Mitigation: Read the generated findings and verify cited file and line evidence before acting on the verdict. <br>


## Reference(s): <br>
- [Structural Checks](references/structural-checks.md) <br>
- [Design Checks](references/design-checks.md) <br>
- [Marketplace Checks](references/marketplace-checks.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown review report with categorized findings, severity, confidence, and verdict] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes the review report to a user-selected local output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
