## Description: <br>
Diagnose and repair Microsoft Word DOCX formatting problems, including styles, numbering, section breaks, headers and footers, comments, tracked changes, and OOXML compatibility. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyro-ma](https://clawhub.ai/user/kyro-ma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Knowledge workers, legal and operations teams, documentation maintainers, and developers use this skill to diagnose DOCX formatting failures and plan or implement targeted repairs while preserving document structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive legal or business documents may contain confidential content. <br>
Mitigation: Use only the files needed for the task, preserve an original backup, and review any repaired copy before relying on it. <br>
Risk: Broad Word-related activation could apply the skill to requests where document repair is not intended. <br>
Mitigation: Invoke deliberately for DOCX formatting or automation work and review recommendations before changing documents. <br>
Risk: Local tooling may not fully reproduce Microsoft Word desktop rendering behavior. <br>
Mitigation: Validate repaired files by reopening or rendering them when possible, checking page count, styles, numbering, headers, footers, comments, tracked changes, and tables. <br>


## Reference(s): <br>
- [Requirement Plan](references/requirement-plan.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/word-docx-formatting-repair-helper) <br>
- [Markdown to DOCX/PDF](https://segmentfault.com/a/1190000004887280) <br>
- [Word Control Read-Only Mode](https://segmentfault.com/a/1190000023469253) <br>
- [Add Tables to Word with Python](https://segmentfault.com/a/1190000044727832) <br>
- [PDF/HTML to DOCX](https://segmentfault.com/a/1190000047409513) <br>
- [Tracked Change Records](https://segmentfault.com/q/1010000005983758/a-1020000005984066) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional code, shell commands, configuration snippets, and document repair notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include diagnosis, repair plans, implementation changes, validation notes, and remaining risk notes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
