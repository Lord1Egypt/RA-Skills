## Description:

Minimal TypeScript hello-world skill that demonstrates bundling TypeScript code, using a Node dependency, and documenting package instructions for ClawHub publication.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[whgreate](https://clawhub.ai/user/whgreate)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill as a minimal TypeScript example for installing npm dependencies, running a hello-world script, and reusing a small exported function.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing npm dependencies can introduce ordinary supply-chain and reproducibility risk.

Mitigation: Review package.json and prefer a lockfile or pinned dependency versions before installing.

Risk: The embedding-demo.ts script is present even though the main documentation focuses on hello.ts.

Mitigation: Review both scripts before reuse and treat embedding-demo.ts as demo wiring rather than a production embedding implementation.

## Reference(s):

- [README Usage](references/README-usage.md)

## Skill Output:

**Output Type(s):** [text, code, shell commands, guidance]

**Output Format:** [Plain text greeting, TypeScript source, and Markdown usage notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a timestamped greeting implemented with dayjs and a deterministic fake embedding demo script.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
