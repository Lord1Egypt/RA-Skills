## Description:

Run cargo check on the agent-browser CLI to catch compile errors and warnings before committing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eohmig](https://clawhub.ai/user/eohmig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run a fast Rust compile check for the agent-browser CLI and summarize any errors or warnings before committing changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cargo checks can execute Rust build scripts from the target project or its dependencies.

Mitigation: Review the target Rust project and dependency set before allowing the Cargo command to run.

Risk: The skill targets a hardcoded local agent-browser path.

Mitigation: Install or invoke it only in environments where that path is expected and appropriate.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with shell commands and diagnostic summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports cargo check results, including file and line details when available; does not format code or perform full builds.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
