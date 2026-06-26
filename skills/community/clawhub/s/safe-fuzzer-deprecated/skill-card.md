## Description: <br>
Sandbox-only behavior-led gray-box skill fuzzer. Spawns a worker subagent, probes an installed target skill, deploys honeypot fixtures, and returns a structured JSON risk report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archidoge0](https://clawhub.ai/user/archidoge0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use SAFE-Fuzzer to probe installed OpenClaw skills inside a locked fuzzer sandbox, deploy synthetic honeypot fixtures, and collect a structured JSON report of file, shell, credential, and network behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the fuzzer in a normal workspace could expose valuable files or real credentials while probes exercise target skills. <br>
Mitigation: Run it only in the intended locked fuzzer sandbox and require preflight refusal when sandbox controls are absent or elevated execution is available. <br>
Risk: Probe cycles may create files, run commands, and observe network behavior while testing a target skill. <br>
Mitigation: Use synthetic honeypot fixtures and synthetic credentials only, then review the structured JSON report for observed file, shell, credential, and network activity. <br>
Risk: Fuzzer outputs may contain target behavior details and synthetic bait observations that should not be mixed with host data. <br>
Mitigation: Keep fixtures and reports inside the sandbox workspace and do not provide real secrets, host configuration, or valuable local files to the run. <br>


## Reference(s): <br>
- [SAFE-Fuzzer ClawHub page](https://clawhub.ai/archidoge0/safe-fuzzer-deprecated) <br>
- [SAFE: Skilled Agent Fuzzing Engine](https://github.com/RiemaLabs/safe) <br>
- [SAFE README](https://github.com/RiemaLabs/safe/blob/main/README.md) <br>
- [Report Schema](references/report-schema.md) <br>
- [Balanced Preset](references/presets/balanced.json) <br>
- [Minimum Preset](references/presets/min.json) <br>
- [Maximum Preset](references/presets/max.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [One structured JSON risk report, with setup and invocation guidance in Markdown and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The report records sandbox preflight status, target resolution, probe strategy, honeypot status, observed evidence, findings, risk counts, and confidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
