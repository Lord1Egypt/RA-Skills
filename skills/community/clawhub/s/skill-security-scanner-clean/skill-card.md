## Description: <br>
Security scanner for OpenClaw skills that detects malicious backdoors, suspicious code patterns, data exfiltration risks, and security vulnerabilities in Python, JavaScript, and Shell code, then provides a security score and installation recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CookieMikeLiu](https://clawhub.ai/user/CookieMikeLiu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security reviewers use this skill to statically scan OpenClaw skills before installation, update, or audit, then review findings, scores, verdicts, and installation recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports can include snippets from scanned files. <br>
Mitigation: Review reports before sharing them and scan only the skill folders intended for review. <br>
Risk: Static scanner findings can require human judgment, including false positives or missed behavior outside the covered rules. <br>
Mitigation: Inspect flagged code, compare behavior with the skill documentation, and use strict mode for untrusted sources. <br>
Risk: Untrusted skill archives may contain files that should not be unpacked directly into a trusted workspace. <br>
Mitigation: Use sandboxed copies or temporary directories when scanning untrusted .skill archives. <br>


## Reference(s): <br>
- [Security Scanner Detection Rules Reference](references/rules-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Terminal summaries plus JSON or Markdown reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit codes indicate PASS or REVIEW, WARNING, and REJECT outcomes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
