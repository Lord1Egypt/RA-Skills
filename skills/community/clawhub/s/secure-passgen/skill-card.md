## Description:

Generate passwords, passphrases, API keys, PINs, hex strings, and base64 tokens with optional entropy display.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hostilespider](https://clawhub.ai/user/hostilespider)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to generate local credentials such as passwords, passphrases, API keys, PINs, and token strings from a command-line script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Entropy display and passphrase strength claims may be misleading.

Mitigation: Review and correct strength calculations before relying on generated values for real credentials.

Risk: Zero, negative, or very large numeric arguments can produce empty secrets or impractical output.

Mitigation: Use positive, bounded values for length, word count, and output count, and add input validation before production use.

Risk: Clipboard use may expose generated credentials to local clipboard history or other local processes.

Mitigation: Avoid clipboard mode for sensitive credentials unless the local clipboard environment is trusted and cleared after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hostilespider/skills/secure-passgen)
- [Publisher profile](https://clawhub.ai/user/hostilespider)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text generated credentials and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with python3; optional clipboard behavior requires a platform clipboard utility.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
