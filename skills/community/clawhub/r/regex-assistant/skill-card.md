## Description:

RegexAssistant helps agents test, debug, and generate regular expressions, including match checks, capture groups, extraction, and replacement workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crossallen](https://clawhub.ai/user/crossallen)

### License/Terms of Use:


## Use Case:

Developers and agents use RegexAssistant to validate regex behavior, inspect matches and capture groups, extract matched content, perform regex replacements, and retrieve common regex patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted or very complex regular expressions can stall execution through catastrophic backtracking on large input.

Mitigation: Test unfamiliar patterns on small inputs first, bound input size, and stop the process if evaluation stalls.

Risk: The CLI output is localized in Chinese, which may be unsuitable for workflows that require English-only operator output or logs.

Mitigation: Install only where Chinese-language command output is acceptable, or wrap and translate output before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crossallen/skills/regex-assistant)

## Skill Output:

**Output Type(s):** [text, shell commands, code, guidance]

**Output Format:** [Plain text CLI output and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Localized Chinese CLI output; regex runtime depends on pattern complexity and input size.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
