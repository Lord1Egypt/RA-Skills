## Description: <br>
中文 Word 文档自动化校对工具，用于对中文文本或 Word 文档进行标点符号检查、语法检查和错别字检查。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bbxiudeyi](https://clawhub.ai/user/bbxiudeyi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and document authors use this skill to proofread Chinese Word documents, split document text into sentences, identify punctuation, typo, and grammar issues, and produce correction data, a review report, or a corrected document. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can generate a corrected Word document, so accepted changes may alter user documents. <br>
Mitigation: Keep the original document, review the generated corrected .docx against the proofreading report, and rely on the corrected document only after human approval. <br>
Risk: Proofreading suggestions may be incorrect, especially for context-dependent wording or professional terms the skill says it does not handle. <br>
Mitigation: Use the report as review guidance, preserve specialized terminology, and require a human editor to approve punctuation, typo, and grammar changes before publication. <br>


## Reference(s): <br>
- [Common sentence errors](references/common-sentence-errors.md) <br>
- [Common typos](references/common-typos.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON correction data, Word .docx reports, corrected Word .docx files, and shell commands for the bundled Python scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a corrections.json structure with punctuation, typo, grammar, and summary sections; corrected document output is written as a new .docx file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
