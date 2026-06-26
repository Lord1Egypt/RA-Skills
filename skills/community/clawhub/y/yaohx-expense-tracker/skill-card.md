## Description: <br>
Expense Tracker records personal spending from text or payment screenshots, stores monthly expense records, and generates monthly spending summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nontrace](https://clawhub.ai/user/nontrace) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and agent users use this skill to capture expenses from manual descriptions or payment screenshots, maintain monthly JSON expense records, and review category-based spending reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores sensitive expense history in local JSON files. <br>
Mitigation: Use it only where local persistent storage of spending history is acceptable, protect the generated files, and remove records that should not be retained. <br>
Risk: Payment screenshots can expose raw payment text through OCR logs. <br>
Mitigation: Avoid screenshots with unrelated sensitive information and remove or disable raw OCR logging before routine use. <br>


## Reference(s): <br>
- [Data Schema Reference](references/data_schema.md) <br>
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash snippets and JSON expense records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local JSON files for categories, monthly expenses, and monthly summaries.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
