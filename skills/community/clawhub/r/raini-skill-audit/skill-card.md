## Description: <br>
Scans OpenClaw skill files for patterns that may indicate credential exposure, suspicious network calls, dynamic execution, filesystem traversal, or obfuscation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xRaini](https://clawhub.ai/user/0xRaini) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and security reviewers use this skill to inspect OpenClaw skill directories before installation or deployment and review a risk-scored report of suspicious patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads files from skill directories selected for scanning, and --all scans the local OpenClaw skills workspace. <br>
Mitigation: Run it only against skill folders you intend to inspect and are comfortable granting read access to. <br>
Risk: Static pattern matching can miss risky behavior or flag benign code that resembles suspicious patterns. <br>
Mitigation: Treat the report as review guidance and manually inspect flagged or security-sensitive findings before installing or deploying a skill. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/0xRaini/raini-skill-audit) <br>
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) <br>
- [Moltbook Security Discussion](https://www.moltbook.com/post/cbd6474f-8478-4894-95f1-7b104a73bcd5) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style terminal report with risk score, severity-grouped findings, file and line references, and installation guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are generated from static pattern matching over JavaScript, TypeScript, JSON, and Markdown files in selected skill directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and artifact/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
