## Description: <br>
Automatically detects security risks in ClawHub, GitHub, and local skills across JavaScript, TypeScript, Python, and Shell files and generates detailed reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[torchesfrms](https://clawhub.ai/user/torchesfrms) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to scan skill packages before installation or release, triage findings, and generate security reports for local or remote skill sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsafe command handling can expose users when untrusted target strings are passed through the Node wrapper. <br>
Mitigation: Use only explicit local paths or trusted URLs, and avoid passing untrusted target strings through the Node wrapper. <br>
Risk: Remote archive extraction behavior is unconfirmed for remote scans. <br>
Mitigation: Review the skill before installing and use trusted remote sources only. <br>
Risk: A prefilled whitelist may suppress expected findings. <br>
Mitigation: Inspect or clear whitelist.txt before scanning. <br>
Risk: Scanner results are advisory rather than comprehensive security approval. <br>
Mitigation: Treat results as triage input and perform separate review before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/torchesfrms/skill-sec-scan-en) <br>
- [Detection rules](references/rules.md) <br>
- [Dangerous commands reference](references/dangerous-commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown security reports, JSON or JSONL scan output, and shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include scanned file counts, issue counts, 0-100 scoring, categorized findings, severity levels, and advisory conclusions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
