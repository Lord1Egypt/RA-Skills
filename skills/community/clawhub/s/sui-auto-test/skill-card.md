## Description:

Analyze Sui Move test coverage, identify untested code, write missing tests, and perform security audits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[easonc13](https://clawhub.ai/user/easonc13)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to analyze Sui Move coverage, identify untested functions, assertions, and branches, and guide creation of missing tests with security-focused edge cases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may cause an agent to run local Sui coverage commands and write or modify repository test files.

Mitigation: Install and run it only for intended Sui Move repositories, then review generated coverage reports and diffs before accepting file changes.

Risk: The artifact workflow includes staging and committing test improvements.

Mitigation: Do not allow staging or commits unless you have explicitly approved the final diff and commit message.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, json, code, shell commands, guidance]

**Output Format:** [Markdown, JSON, terminal text, Move test code, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write coverage reports such as coverage.md when the agent is directed to run the included tools.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
