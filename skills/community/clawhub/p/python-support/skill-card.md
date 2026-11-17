## Description:

Python Support gives OpenClaw agents guidance for Python environment setup, dependency management, script execution, linting, testing, debugging, and code-quality practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to help agents perform Python-related work consistently, including environment checks, script execution, dependency setup, and code-quality practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead agents to install Python packages quietly or automatically, which can be risky in shared environments or when working with untrusted code.

Mitigation: Require explicit approval for package installs, prefer isolated virtual environments, and use pinned, reviewed dependencies.

## Reference(s):

- [Python Style Guide](references/style-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands for environment inspection, package installation, script execution, testing, linting, and formatting.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
