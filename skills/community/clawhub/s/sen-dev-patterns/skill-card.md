## Description: <br>
Personal development patterns for reusing UI styles, coding standards, code modules, algorithm recipes, and pitfalls documentation across projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[the13ai](https://clawhub.ai/user/the13ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to apply a consistent personal development playbook for desktop and web UI styling, Python module structure, reusable calculation formulas, Git workflow guidance, and documented pitfalls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled publishing scripts can obtain sensitive Git credentials, rewrite git remotes, and push code to external repositories. <br>
Mitigation: Review before installing, do not run publish_skill.py or publish_gitee.py unless publishing is intended, and use least-privilege tokens. <br>
Risk: Publishing workflows may place tokens in git remote URLs or other local configuration. <br>
Mitigation: Avoid token-in-URL remotes, inspect git configuration before and after publishing, and rotate any token that may have been embedded. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/the13ai/sen-dev-patterns) <br>
- [README](README.md) <br>
- [UI Style Guide](references/ui-style-guide.md) <br>
- [Web Development Guide](references/web-guide.md) <br>
- [Coding Standards](references/coding-standards.md) <br>
- [Algorithm Library](references/algorithm-library.md) <br>
- [Code Modules](references/code-modules.md) <br>
- [Performance Guide](references/performance-guide.md) <br>
- [Git Workflow](references/git-workflow.md) <br>
- [Pitfalls Record](references/pitfalls-record.md) <br>
- [Evaluation Report](references/evaluation-report.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with inline code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation or reuse of local project files and module templates.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter and package.json report 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
