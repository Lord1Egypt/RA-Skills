## Description: <br>
Create, inspect, and edit Microsoft Word documents and DOCX files with reliable styles, numbering, tracked changes, tables, sections, and compatibility checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tonydesign1999](https://clawhub.ai/user/tonydesign1999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, editors, and document-review agents use this skill when creating, inspecting, or editing Word/DOCX files where tracked changes, comments, fields, tables, sections, styles, numbering, templates, or round-trip compatibility matter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Word documents can contain tracked changes, comments, deleted text, fields, and hidden review metadata that an agent may inspect. <br>
Mitigation: Use the skill only with documents whose review metadata the user is comfortable exposing to the agent. <br>
Risk: Complex DOCX layout, numbering, tables, fields, and headers can drift after editing or when opened in Word, LibreOffice, Google Docs, or conversion tools. <br>
Mitigation: Preserve existing styles and OOXML structure, make minimal review-style edits, and verify round-trip rendering before delivery. <br>
Risk: Macro-bearing `.docm` and legacy `.doc` files carry higher compatibility or automation risk than ordinary `.docx` files. <br>
Mitigation: Treat macro-bearing or legacy files as higher risk, avoid executing macros, and convert or inspect them with an appropriate workflow before editing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tonydesign1999/word-docx-1) <br>
- [Skill homepage](https://clawic.com/skills/word-docx) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline examples, commands, and document-handling recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance-only skill; no executable code or credential access was identified in the security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
