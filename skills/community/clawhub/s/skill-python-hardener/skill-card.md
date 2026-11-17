## Description:

Hardens Python scripts by applying a complete security review, clean-code refactoring, robust error handling, proper logging, and full docstring coverage, then produces a companion Markdown documentation file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kikikari](https://clawhub.ai/user/kikikari)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review and harden Python scripts in place, addressing security, error handling, logging, resource management, type hints, and documentation. It is intended for ordinary Python review or fix requests where broad code hardening and a companion Markdown documentation file are desired.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may rewrite Python code broadly during hardening.

Mitigation: Review generated diffs before accepting changes, especially in critical scripts or shared modules.

Risk: The skill text recommends assert-based SQL identifier validation in one place, which can be disabled when Python runs with optimization.

Mitigation: Replace assert-based checks with explicit runtime validation such as raising ValueError for invalid identifiers.

## Reference(s):

- [Server-resolved source repository path](https://github.com/KikiKari/OpenClaw/tree/main/packages/skill-python-hardener)
- [ClawHub skill page](https://clawhub.ai/kikikari/skills/skill-python-hardener)

## Skill Output:

**Output Type(s):** [Analysis, Code, Markdown, Configuration guidance]

**Output Format:** [Modified source files plus Markdown documentation and concise review notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves original Python filenames and produces one companion Markdown documentation file unless the user requests otherwise.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
