## Description: <br>
Parse traffic accident legal documents and generate exam answers for Chinese traffic safety law workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhanghaibo7612](https://clawhub.ai/user/zhanghaibo7612) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, legal operations teams, and developers use this skill to parse local Word documents containing traffic accident legal material, build structured legal-reference JSON, and draft Markdown answer templates for traffic safety exams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated legal text or exam answers may be incomplete, outdated, or unsuitable for a specific case. <br>
Mitigation: Review generated outputs with a qualified legal professional or authoritative current legal source before relying on them. <br>
Risk: Parsed Word documents and generated JSON or Markdown may contain private legal, case, or exam information. <br>
Mitigation: Run the skill only on trusted local folders, choose output locations deliberately, and avoid sharing generated files that contain sensitive source content. <br>
Risk: The document parsing scripts depend on local file paths and have limited support for older .doc files. <br>
Mitigation: Confirm the target folder and file formats before execution, and manually review files that the parser reports as unsupported or requiring manual parsing. <br>


## Reference(s): <br>
- [Traffic Accident Legal Articles Quick Reference](references/legal_articles.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zhanghaibo7612/traffic-law-doc) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown answers, structured JSON legal extracts, Python scripts, and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local user-selected Word documents and writes generated JSON or Markdown outputs to chosen paths.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
