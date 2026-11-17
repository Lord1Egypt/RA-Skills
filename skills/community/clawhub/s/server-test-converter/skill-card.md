## Description:

Converts server test command TXT files into pytest test cases, generating one pytest file per input file with commands routed to R5-card or host-shell execution helpers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyun2025](https://clawhub.ai/user/liuyun2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and test engineers use this skill to convert batches of server or network-card command text files into pytest test files for controlled hardware or host test environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TXT command inputs become runnable pytest code that may execute on hosts or R5 devices.

Mitigation: Use trusted TXT files and filenames only, review generated pytest files before running them, and operate in a controlled test environment.

Risk: Weak execution safeguards can allow unintended or destructive commands to reach real hosts or devices.

Mitigation: Add command allowlists or destructive-command blocking before using the generated tests on real infrastructure.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liuyun2025/skills/server-test-converter)
- [Publisher Profile](https://clawhub.ai/user/liuyun2025)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Generated Python pytest files and Markdown guidance with inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates one pytest file per input TXT file, deduplicates repeated commands, and requires environment-specific command execution helpers before tests are run.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
