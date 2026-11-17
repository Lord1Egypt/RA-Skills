## Description:

Host-specific Python execution guidance for OpenClaw on this machine, preferring $PYTHON over python/python3 in PATH because OpenClaw exec runs in a non-interactive shell and may not inherit interactive shell initialization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cndaqiang](https://clawhub.ai/user/cndaqiang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to run Python reliably in OpenClaw sessions where non-interactive shells may not expose python, python3, or conda through PATH.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PYTHON may point to an unintended or invalid interpreter.

Mitigation: Confirm that PYTHON is set to the intended executable and verify it with test -x "$PYTHON" and "$PYTHON" --version before running commands.

Risk: Unpinned pip install examples may introduce supply-chain or reproducibility risk.

Mitigation: Approve package installs deliberately and prefer pinned versions or a project lockfile when adapting the examples.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cndaqiang/skills/py-env-setup)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Host-specific guidance that depends on a valid PYTHON environment variable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
