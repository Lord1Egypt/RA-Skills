## Description: <br>
Generates standardized XMind-format test cases from requirements documents and supporting code analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wxl1779766474](https://clawhub.ai/user/wxl1779766474) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QA engineers, developers, and product teams use this skill to turn requirements and implementation details into XMind test-case files with prioritized P1 smoke and P3 normal cases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger wording may activate the skill for generic Chinese requests to write or generate test cases. <br>
Mitigation: Confirm that the user expects XMind-format output when the request is not explicitly XMind-specific. <br>
Risk: The bundled generator writes .xmind files to a fixed local Desktop work directory by default. <br>
Mitigation: Confirm the desired output location or adjust the generator path before running it in a new environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wxl1779766474/xmind-testcase-generator) <br>
- [XMind Test Case Specification](artifact/xmind-testcase.md) <br>
- [gen_xmind.py API Reference](artifact/reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance plus Python code edits and generated .xmind files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated XMind files are ZIP packages containing content.json, metadata.json, and manifest.json.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
