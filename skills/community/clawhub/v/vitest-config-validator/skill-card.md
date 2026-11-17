## Description:

Validate vitest.config.ts/js and vitest workspace configurations for syntax, deprecated options, plugin conflicts, and best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect Vitest and Vite test configuration files for syntax issues, deprecated options, conflicting settings, and practical test setup improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local validator reads the Vitest or Vite configuration files supplied to it.

Mitigation: Run it only against intended project configuration files in workspaces where local file reads are acceptable.

Risk: Regex-based static checks can miss dynamic configuration behavior or report issues that require human review.

Mitigation: Treat findings as advisory and confirm important changes with project tests or Vitest documentation before applying them.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional text, JSON, or summary validator output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled validator can return human-readable findings, machine-readable JSON, or a PASS/WARN/FAIL summary.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
