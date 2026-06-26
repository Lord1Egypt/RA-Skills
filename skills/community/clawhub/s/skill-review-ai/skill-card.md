## Description: <br>
审查 Agent Skills 的规范性、完整性和代码质量。在安装或发布 skills 时使用，验证 SKILL.md 格式、目录结构、脚本代码和文件引用是否符合 Agent Skills 规范。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hwl1413520](https://clawhub.ai/user/hwl1413520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to review Agent Skills before installation or publication, checking specification conformance, completeness, code quality, and file references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reviewer produces heuristic findings that may be incomplete or misleading if treated as a final security decision. <br>
Mitigation: Use the report as guidance and perform human review before installing, publishing, or relying on a skill. <br>
Risk: The local script reads the user-supplied skill directory during review. <br>
Mitigation: Run it only against skill directories you are comfortable letting a local script inspect. <br>


## Reference(s): <br>
- [Agent Skills Specification](references/SPECIFICATION.md) <br>
- [Review Rules](references/RULES.md) <br>
- [FAQ](references/FAQ.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Code] <br>
**Output Format:** [Markdown or JSON review reports with CLI and Python API usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include category scores, pass/warning/fail status, and issue details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
