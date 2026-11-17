## Description:

Diagnose and repair Microsoft Word DOCX formatting problems, including styles, numbering, section breaks, headers and footers, comments, tracked changes, and OOXML compatibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Knowledge workers, legal and operations teams, documentation maintainers, and developers use this skill to diagnose Word DOCX formatting failures and create safe repair plans or targeted document/code changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be invoked broadly for Word or DOCX topics.

Mitigation: Use it when DOCX formatting diagnosis, repair, automation, or OOXML inspection is actually intended.

Risk: DOCX repair can alter sensitive legal or business documents, tracked changes, comments, or low-level OOXML structures.

Mitigation: Keep the original file, work on a copy, and confirm before accepting tracked changes, deleting comments, or making direct OOXML edits.

Risk: Word desktop rendering and compatibility behavior may not be fully verifiable in the local execution environment.

Mitigation: Validate repaired documents by reopening or rendering them in Word-compatible tooling when possible, and report any remaining verification limits.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [Skill page](https://clawhub.ai/kyro-ma/skills/word-docx-formatting-repair-helper-180322)
- [markdown + pandoc DOCX/PDF discussion](https://segmentfault.com/a/1190000004887280)
- [SAP Document Builder Word control discussion](https://segmentfault.com/a/1190000023469253)
- [Python Word table tutorial](https://segmentfault.com/a/1190000044727832)
- [PDF/HTML to DOCX discussion](https://segmentfault.com/a/1190000047409513)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional code blocks, shell commands, repair plans, validation notes, and document-change guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include diagnosis, targeted repair steps, implementation details, and residual risk notes.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
