## Description: <br>
Diagnose and repair Microsoft Word DOCX formatting problems, including styles, numbering, section breaks, headers and footers, comments, tracked changes, and OOXML compatibility. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyro-ma](https://clawhub.ai/user/kyro-ma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Knowledge workers, legal and operations teams, documentation maintainers, and developers use this skill to diagnose broken Word DOCX formatting and plan or implement targeted repairs while preserving document structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Document repair can change important formatting, tracked changes, comments, or document structure. <br>
Mitigation: Work on copies, preserve tracked changes and comments unless the user explicitly requests a clean final file, and review changes before relying on the repaired document. <br>
Risk: Confidential legal or business documents may require careful handling. <br>
Mitigation: Request the DOCX only when inspection is required and remind users to handle confidential files according to their privacy and compliance requirements. <br>
Risk: Word desktop behavior may not be fully verifiable in the local environment. <br>
Mitigation: Validate by reopening or rendering the document when possible and report any remaining Word-specific verification limits. <br>


## Reference(s): <br>
- [Requirement Plan](references/requirement-plan.md) <br>
- [ClawHub Release Page](https://clawhub.ai/kyro-ma/word-docx-formatting-repair-helper-180322) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with optional code blocks or shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include diagnosis, repair plan or implemented document/code changes, validation notes, and remaining risks.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
