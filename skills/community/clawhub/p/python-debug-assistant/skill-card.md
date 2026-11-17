## Description:

Python Debug Assistant helps diagnose and fix Python errors, covering common exception types such as SyntaxError, TypeError, and NameError with error interpretation, code localization, repair options, and debugging tips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laninga](https://clawhub.ai/user/laninga)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and learners use this skill to interpret Python tracebacks or code snippets, locate likely causes, and receive concise repair steps with example corrected code. It is especially suited to Chinese-language debugging workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may produce incorrect or incomplete debugging advice for user-provided code.

Mitigation: Review proposed fixes and run tests before applying changes to production or important code.

Risk: The reviewed security guidance notes the skill is primarily Chinese-language and may feel rigid for other languages or output formats.

Mitigation: Use it for Chinese-language Python debugging workflows, and request a different format or language explicitly when needed.

## Reference(s):

- [Python Built-in Exceptions](https://docs.python.org/3/library/exceptions.html)
- [ClawHub Skill Page](https://clawhub.ai/laninga/skills/python-debug-assistant)
- [Common Python Errors](references/common-errors.md)
- [Python Debugging Tools](references/debugging-tools.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown diagnostic report with explanatory text, code blocks, and occasional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The source artifact requests a fixed report structure for problem analysis, location, repair plan, and debugging advice.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata; artifact frontmatter reports 2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
