## Description: <br>
Organizes reusable templates and snippets by scenario, role, tone, and length, then produces reviewable structured outputs for writing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and writing teams use this skill to turn existing templates, snippets, scenarios, and style requirements into a structured, reviewable Markdown template library with maintenance and retirement guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated snippets or templates may contain sensitive or unreviewed language from local inputs. <br>
Mitigation: Use only intended input files, remove sensitive material before processing, and review generated drafts before publishing or reuse. <br>
Risk: The optional Python helper reads local files and may produce misleading reports if pointed at the wrong path or customized without review. <br>
Mitigation: Run the helper only on files or directories meant for processing, prefer dry-run or review workflows, and recheck customized specs before operational use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/52YuanChangXing/template-snippet-switchboard) <br>
- [Publisher Profile](https://clawhub.ai/user/52YuanChangXing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON structured reports, with optional local shell command usage for the bundled Python helper.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended as reviewable drafts, checklists, or dry-run reports; review generated content before publishing or applying it.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
