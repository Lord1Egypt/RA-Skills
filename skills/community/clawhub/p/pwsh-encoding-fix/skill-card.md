## Description:

Fix PowerShell file encoding corruption (backtick, dollar sign, Chinese char mangling) when writing Node.js files on Windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeremycooper2077](https://clawhub.ai/user/jeremycooper2077)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to diagnose and repair JavaScript or Node.js files damaged by Windows PowerShell encoding behavior, including lost template backticks, expanded dollar variables, GBK text corruption, syntax errors, and UTF-8 BOMs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A specially crafted JavaScript filename can cause the helper script to run unintended operating-system commands.

Mitigation: Run the helper only on trusted files and filenames until the script uses an argument-based process API with shell execution disabled.

Risk: The --fix mode rewrites files while attempting encoding repair.

Mitigation: Make an independent backup of important files before using --fix, even though the script attempts to create a .bak copy.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jeremycooper2077/skills/pwsh-encoding-fix)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code]

**Output Format:** [Markdown guidance with inline shell commands and a Node.js diagnostic script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a .bak backup and rewrite the target file when the helper script is run with --fix.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
