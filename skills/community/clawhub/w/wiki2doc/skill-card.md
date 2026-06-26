## Description: <br>
Converts internal Confluence Wiki pages into Word documents, analyzes requirements, and generates structured test cases as Markdown, JSON, and Excel outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yontlly](https://clawhub.ai/user/yontlly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and product teams use this skill to export Confluence requirements, review requirement quality, and create test-case deliverables for test planning and execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary reports hardcoded internal Confluence credentials. <br>
Mitigation: Replace embedded credentials with secure local configuration before use and rotate any exposed credentials if they are real. <br>
Risk: The security summary reports persistent storage of fetched Confluence content. <br>
Mitigation: Run only against content you are authorized to access, restrict output directories, and delete generated debug HTML or sensitive exports after review. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yontlly/wiki2doc) <br>
- [README.md](artifact/README.md) <br>
- [examples.md](artifact/examples.md) <br>
- [skill.md](artifact/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON reports, Word documents, Excel workbooks, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces demand artifacts such as .docx exports, requirement analysis reports, test-case Markdown/JSON, and .xlsx spreadsheets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
