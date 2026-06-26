## Description: <br>
Scans installed OpenClaw skills for malicious patterns including prompt injection, credential theft, data exfiltration, obfuscated payloads, and backdoors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[itsclawdbro](https://clawhub.ai/user/itsclawdbro) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to scan newly installed, updated, or periodically audited OpenClaw skills for malicious patterns before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scanner results are heuristic and can miss issues or flag benign security examples. <br>
Mitigation: Review findings manually for sensitive installs and use the single-skill scanner or raw findings when maximum transparency is needed. <br>
Risk: Batch scans use allowlists to suppress known false positives, which can hide details during aggregate review. <br>
Mitigation: Run targeted scans without exclusions when a skill needs stricter review. <br>


## Reference(s): <br>
- [Threat Patterns Reference](references/threat-patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/itsclawdbro/skill-defender) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Human-readable scanner summaries or JSON reports with verdicts, findings, counts, timestamps, and exit codes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs offline with Python standard library only; results are deterministic heuristic scanner output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
