## Description:

Sandbox-only behavior-led gray-box skill fuzzer. Spawns a worker subagent, probes an installed target skill, deploys honeypot fixtures, and returns a structured JSON risk report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archidoge0](https://clawhub.ai/user/archidoge0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to fuzz installed OpenClaw skills in a dedicated sandbox, using honeypot fixtures and probe presets to produce a structured risk report. It is intended for post-setup behavioral probing rather than target installation or remediation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill intentionally creates bait files and drives another installed skill through file, shell, credential-like, and network workflows.

Mitigation: Run it only in a dedicated OpenClaw fuzzer sandbox with no real secrets or production credentials.

Risk: Probe execution may surface or exercise sensitive behaviors in the target skill, including credential-like handling, file operations, command execution, and network egress.

Mitigation: Use synthetic fixture values only and review the structured JSON report for honeypot, incident, egress, credential, and risk-count fields before acting on results.

## Reference(s):

- [SAFE: Skilled Agent Fuzzing Engine](https://github.com/RiemaLabs/safe)
- [SAFE README](https://github.com/RiemaLabs/safe/blob/main/README.md)
- [Report Schema](references/report-schema.md)
- [Minimum Probe Preset](references/presets/min.json)
- [Balanced Probe Preset](references/presets/balanced.json)
- [Maximum Probe Preset](references/presets/max.json)
- [ClawHub Skill Page](https://clawhub.ai/archidoge0/skills/safe-fuzzer-deprecated)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns one structured risk-report object with findings, coverage, honeypot status, incident status, risk counts, and confidence.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
