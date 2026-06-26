## Description: <br>
Detects and filters prompt injection attacks in untrusted text before it is passed to an LLM, covering direct injection, jailbreaks, data exfiltration, privilege escalation, and context manipulation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[staybased](https://clawhub.ai/user/staybased) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use Reef Prompt Guard to scan external content such as emails, web scrapes, API payloads, Discord messages, and sub-agent outputs before sending that text to an LLM. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A documented JavaScript shell-string integration pattern could expose an application to command injection if copied with untrusted input. <br>
Mitigation: Use the direct Python import, pass input through stdin or JSON as data, or invoke child processes with an argument array instead of interpolating untrusted text into a shell command. <br>
Risk: Regex-based scanning catches known patterns but may miss novel semantic, multimodal, or obfuscated prompt-injection attempts. <br>
Mitigation: Use the filter as one layer in a broader control set, review suspicious outputs, keep detection patterns current, and avoid treating a clean result as a complete security guarantee. <br>


## Reference(s): <br>
- [Prompt Injection Attack Patterns & Defense Strategies](references/attack-patterns.md) <br>
- [ClawHub release page](https://clawhub.ai/staybased/reef-prompt-guard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code examples and JSON scanner results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI exits with clean, suspicious, or blocked status and returns score, sanitized text, and detected threats.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
