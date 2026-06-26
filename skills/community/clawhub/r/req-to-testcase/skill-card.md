## Description: <br>
Generates structured test cases from requirement documents and can export them as an XMind mind map. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deathknightorg](https://clawhub.ai/user/deathknightorg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QA engineers, product teams, and developers use this skill to turn uploaded requirement documents or pasted requirement text into requirement breakdowns, prioritized test cases, and downloadable XMind files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded requirement documents or spreadsheets may contain sensitive product, customer, or business information. <br>
Mitigation: Use the skill only with documents intended for processing, and avoid sensitive spreadsheets unless that handling is explicitly intended. <br>
Risk: The helper scripts depend on optional Python packages for document parsing and XMind generation. <br>
Mitigation: Install dependencies in an isolated Python environment before running the scripts. <br>
Risk: Generated test cases may omit requirements or include inferred scenarios that do not match the system under test. <br>
Mitigation: Review the generated requirement breakdown and test cases before using them for release decisions. <br>


## Reference(s): <br>
- [Test Coverage Strategy](references/test-coverage.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/deathknightorg/req-to-testcase) <br>
- [Publisher Profile](https://clawhub.ai/user/deathknightorg) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown tables with optional shell commands and generated .xmind files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can read uploaded Word, PDF, Markdown, TXT, Excel, and CSV requirement documents when the required Python dependencies are installed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
