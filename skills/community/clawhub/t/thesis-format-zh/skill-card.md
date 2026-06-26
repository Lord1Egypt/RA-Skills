## Description: <br>
Chinese thesis formatting checker that parses school DOCX templates, compares thesis documents against extracted formatting rules, and generates difference and risk reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yeyeeyeeee](https://clawhub.ai/user/yeyeeyeeee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, researchers, thesis editors, and academic writing support teams use this skill to check Chinese Word thesis documents against school templates before submission. It helps extract template rules, compare document formatting, and produce Markdown or JSON reports for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill needs access to user-selected thesis and template DOCX files, which may contain private academic content. <br>
Mitigation: Install and run it only when comfortable granting access to those files, and avoid providing unrelated sensitive documents. <br>
Risk: Document-editing or auto-formatting workflows can alter thesis files if the user chooses those paths. <br>
Mitigation: Use the documented check and report commands for review first, and keep backups before using repair or auto-formatting workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yeyeeyeeee/thesis-format-zh) <br>
- [Publisher profile](https://clawhub.ai/user/yeyeeyeeee) <br>
- [Format rules reference](artifact/references/format_rules.md) <br>
- [Citation cross-reference reference](artifact/references/citation_crossref.md) <br>
- [Thesis formatting roadmap](artifact/references/作战地图.md) <br>
- [python-docx styles documentation](https://python-docx.readthedocs.io/en/latest/user/styles-understanding.html) <br>
- [python-docx-template](https://github.com/elapouya/python-docx-template) <br>
- [Python-Redlines](https://github.com/JSv4/Python-Redlines) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON rule or diff data, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads user-selected DOCX and template files locally and writes user-requested report outputs.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence.json release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
