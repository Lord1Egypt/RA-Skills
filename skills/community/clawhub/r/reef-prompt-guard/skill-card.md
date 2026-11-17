## Description:

Detect and filter prompt injection attacks in untrusted input before that content is passed to an LLM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[staybased](https://clawhub.ai/user/staybased)

### License/Terms of Use:


## Use Case:

Developers and agent builders use Reef Prompt Guard to scan untrusted text before passing it to an LLM and to integrate prompt-injection filtering into email, web, API, Discord, and sub-agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented Node.js execSync integration constructs a shell command around untrusted input and could expose adopters to command injection if copied.

Mitigation: Use an argument-array API such as execFileSync, call the Python scanner directly, and apply timeouts and input-size limits.

Risk: Regex-based filtering can miss novel semantic, multimodal, or heavily obfuscated prompt-injection attacks.

Mitigation: Use this skill as one layer in a defense-in-depth design, keep untrusted content isolated, review suspicious outputs, and update detection patterns as attacks evolve.

Risk: Security research discussions or benign examples of attack strings may be flagged as suspicious or blocked.

Mitigation: Review blocked or suspicious results before enforcement in sensitive workflows and tune context thresholds or patterns for the deployment.

## Reference(s):

- [Reef Prompt Guard on ClawHub](https://clawhub.ai/staybased/skills/reef-prompt-guard)
- [Prompt Injection Attack Patterns and Defense Strategies](references/attack-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON scan results from the CLI, Python helper return values, and Markdown guidance with shell and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit code 0 means clean, 1 means blocked, and 2 means suspicious; verbose mode can include context and input length.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence, created 2026-02-12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
