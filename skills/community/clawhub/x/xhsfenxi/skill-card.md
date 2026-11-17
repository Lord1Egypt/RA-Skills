## Description:

Xhsfenxi guides agents through public-evidence-based Xiaohongshu/RED creator analysis, archetype classification, viral topic formula extraction, creator comparisons, and business-ready report deliverables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cosmofang](https://clawhub.ai/user/cosmofang)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content strategy teams use this skill to analyze public Xiaohongshu/RED creator accounts, classify creator archetypes, extract reusable topic formulas, compare benchmark creators, and produce structured DOCX reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary flags that Word-generation guidance can lead agents or users to run unsafe external shell commands built from creator names.

Mitigation: Use the skill only for public Xiaohongshu/RED creator analysis, quote or sanitize creator names and filenames, choose a dedicated output directory, and review generated commands before execution.

Risk: External DOCX build or repair scripts may be invoked from paths outside the packaged skill.

Mitigation: Verify any external build_docx, inspect_docx, or fix scripts before use and require confirmation before creating or repairing Word files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cosmofang/skills/xhsfenxi)
- [Workflow Reference](references/workflow.md)
- [Templates Reference](references/templates.md)
- [Package Metadata](package.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, Node.js script output, shell command suggestions, and DOCX report plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces public-evidence analysis plans and report structures; standard deliverables are DOCX files for single-creator reports, viral topic formulas, and multi-creator comparisons.]

## Skill Version(s):

2.1.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
