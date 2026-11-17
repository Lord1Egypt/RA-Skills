## Description:

中文 Word 文档自动化校对工具。当用户需要对中文文本或 Word 文档进行标点符号检查、语法检查、错别字检查时使用此 skill。触发词：语法检查、错别字、标点符号、校对、检查文档。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bbxiudeyi](https://clawhub.ai/user/bbxiudeyi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to proofread Chinese Word documents for punctuation, typo, and sentence-level grammar issues, then generate structured corrections, a Word review report, and a corrected document copy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local JSON, report, and corrected document outputs may contain extracted or modified text from sensitive Word documents.

Mitigation: Run the skill only in a workspace appropriate for the document sensitivity and handle generated files under the same confidentiality controls as the source document.

Risk: The workflow depends on python-docx for reading and writing Word files.

Mitigation: Install python-docx from a trusted, pinned Python environment before use.

Risk: Automated proofreading suggestions can be incorrect or change intended meaning if applied without review.

Mitigation: Review corrections.json and the generated proofreading report before applying changes to the document.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bbxiudeyi/skills/word-chinese-automation)
- [Common Sentence Errors](references/common-sentence-errors.md)
- [Common Typos](references/common-typos.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON correction data and generated Word document files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local outputs may include sentences JSON, corrections JSON, a Word proofreading report, and a corrected Word document copy.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
