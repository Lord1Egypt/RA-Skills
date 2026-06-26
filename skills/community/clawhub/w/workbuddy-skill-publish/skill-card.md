## Description: <br>
Skill Publish helps agents audit, clean, publish, and verify SKILL.md-based skills for ClawHub and GitHub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to audit skill packages for publish readiness, prepare clean release contents, and coordinate publishing to ClawHub and GitHub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports suspicious publish behavior involving external publishing and repository file changes. <br>
Mitigation: Run audit mode first, review the exact file list and target version, and proceed with publish mode only after confirming the intended ClawHub and GitHub targets. <br>
Risk: Publishing workflows can expose or modify content if credentials are too broad or the wrong repository is targeted. <br>
Mitigation: Use a narrowly scoped GitHub token, verify the repository target before publishing, and review generated changes before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/haiyangchenbj/workbuddy-skill-publish) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance, configuration] <br>
**Output Format:** [Markdown reports with command snippets and checklist-style publish status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include audit tables, clean-file lists, publish targets, version information, URLs, and commit or publish identifiers.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
