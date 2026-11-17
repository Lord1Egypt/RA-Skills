## Description:

Generate cryptographically secure random passwords with customizable length, character classes, and similar-character exclusion using Python's standard library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and other external users can use this skill to generate strong random passwords, API keys, or token-like strings offline with configurable character options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unbounded or invalid length and count values can cause confusing output or excessive local computation.

Mitigation: Use positive, reasonable values for password length and count before running the generator.

Risk: Generated secrets are printed to the terminal and may be exposed through terminal history, logs, or screen sharing.

Mitigation: Run the tool in a trusted local terminal and clear or protect terminal output when generated secrets are sensitive.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/freedompixels/skills/secure-password-tool)
- [Publisher Profile](https://clawhub.ai/user/freedompixels)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated secrets are printed to terminal output; JSON output is available through the --json flag.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
