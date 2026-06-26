## Description: <br>
SeedGen generates local random strings, bytes, numbers, UUIDs, passwords, and batch outputs using /dev/urandom and standard shell tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate local random values such as strings, hex, bytes, integers, floats, UUIDs, passwords, and batch outputs from a shell environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill metadata overclaims deterministic, reproducible, and audit-record capabilities. <br>
Mitigation: Use it only as a local nondeterministic random generator; do not rely on it for reproducible test fixtures, auditable seed records, deterministic replay, or compliance-sensitive salt rotation records. <br>
Risk: Some random-generation modes may not be appropriate for security-sensitive values. <br>
Mitigation: Prefer /dev/urandom-backed modes for security-sensitive random values and review generated outputs before use. <br>
Risk: Unbounded batch requests can consume unnecessary local resources. <br>
Mitigation: Set practical batch-count limits before running large generation jobs. <br>


## Reference(s): <br>
- [BytesAgain homepage](https://bytesagain.com) <br>
- [Seedgen on ClawHub](https://clawhub.ai/bytesagain3/seedgen) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell command examples and plain-text generated values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local nondeterministic random values; some modes depend on standard Linux/macOS command-line tools.] <br>

## Skill Version(s): <br>
3.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
