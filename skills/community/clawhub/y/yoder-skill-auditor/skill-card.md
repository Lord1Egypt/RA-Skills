## Description: <br>
Yoder Skill Auditor scans OpenClaw and ClawHub skills for security issues, computes trust scores, compares releases, and generates audit reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yoder-bawt](https://clawhub.ai/user/yoder-bawt) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and security reviewers use this skill to audit OpenClaw or ClawHub skill directories before installation, during updates, and across skill collections. It provides scanner findings, trust scoring, comparisons, and markdown reporting to support review decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled tests contain intentionally malicious-looking fixture files. <br>
Mitigation: Run the test harness rather than manually executing files under artifact/tests/. <br>
Risk: Scanner findings and trust scores are advisory and may not catch every issue. <br>
Mitigation: Review important findings manually and combine the tool output with normal security review before installation. <br>
Risk: Allowlist entries can reduce the severity of findings for known-good credential-handling skills. <br>
Mitigation: Review the built-in allowlist before relying on downgraded results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yoder-bawt/yoder-skill-auditor) <br>
- [Publisher profile](https://clawhub.ai/user/yoder-bawt) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>
- [TEST-FIXTURES-WARNING.md](artifact/TEST-FIXTURES-WARNING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Terminal text, JSON audit data, trust-score summaries, and Markdown reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit codes indicate pass, review, fail, or input error.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release metadata, SKILL.md frontmatter, skill.json, CHANGELOG.md released 2026-02-16) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
