## Description:

Rich helps agents guide developers in adding styled terminal output, tables, progress indicators, Markdown rendering, syntax highlighting, logging, tracebacks, object inspection, and HTML/SVG exports to Python programs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cn-big-cabbage](https://clawhub.ai/user/cn-big-cabbage)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to ask an agent for Rich installation guidance, Python code snippets, terminal UI patterns, and troubleshooting support for styled command-line output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package installation guidance could alter a user's Python environment or project dependencies.

Mitigation: Use a virtual environment when possible, prefer pinned PyPI releases, and review dependency file changes before applying them.

Risk: Rich traceback examples that show local variables can expose secrets in logs, CI output, or shared terminals.

Mitigation: Avoid show_locals=True and traceback-local logging in production, CI, shared terminals, and any context that may contain credentials or sensitive data.

## Reference(s):

- [Rich documentation](https://rich.readthedocs.io)
- [Rich GitHub repository](https://github.com/Textualize/rich)
- [Rich PyPI package](https://pypi.org/project/rich/)
- [Rich examples](https://github.com/Textualize/rich/tree/master/examples)
- [ClawHub skill page](https://clawhub.ai/cn-big-cabbage/skills/rich)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python, shell, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include installation commands, requirements or pyproject dependency entries, Python examples, terminal compatibility checks, and troubleshooting steps.]

## Skill Version(s):

0.1.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
