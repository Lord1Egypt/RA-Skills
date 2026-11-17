## Description:

Sandbox-only behavior-led gray-box skill fuzzer. Spawns a worker subagent, probes an installed target skill, deploys honeypot fixtures, and returns a structured JSON risk report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentsey](https://clawhub.ai/user/agentsey)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use SAFE-Fuzzer to run sandboxed gray-box probes against installed OpenClaw skills and receive a structured risk report covering file, shell, network, credential, prompt-injection, and honeypot behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill intentionally follows target-skill workflows that may involve sandbox file writes, shell commands, network calls, and synthetic credential handling.

Mitigation: Install and run only in a disposable locked sandbox with host data unreachable and elevated execution unavailable.

Risk: Honeypot fixtures include synthetic secret-like values that can expose unsafe target behavior if copied, logged, persisted, or transmitted.

Mitigation: Use only synthetic credentials and review the JSON report for honeypot triggers, incidents, and egress findings before acting on results.

Risk: Gray-box probing may inspect target-owned instructions, documentation, manifests, or source when needed for planning or blocker diagnosis.

Mitigation: Run the fuzzer only against intended installed target skills and treat the report as behavioral evidence requiring reviewer judgment.

## Reference(s):

- [ClawHub SAFE-Fuzzer skill page](https://clawhub.ai/agentsey/skills/safe-fuzzer-skill)
- [SAFE repository](https://github.com/RiemaLabs/safe)
- [SAFE README](https://github.com/RiemaLabs/safe/blob/main/README.md)
- [Report schema](artifact/references/report-schema.md)
- [Balanced preset](artifact/references/presets/balanced.json)
- [Min preset](artifact/references/presets/min.json)
- [Max preset](artifact/references/presets/max.json)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [JSON risk report, with concise text and optional shell-command guidance for setup blockers.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One JSON object only after a run; presets control probe depth and timeout expectations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
