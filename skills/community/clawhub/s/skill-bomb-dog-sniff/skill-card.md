## Description: <br>
Security-first skill management for OpenClaw that scans skills for malicious payloads before installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LvcidPsyche](https://clawhub.ai/user/LvcidPsyche) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and security reviewers use this skill to statically scan OpenClaw skills, audit installed skills, and gate installation of untrusted skills based on pattern findings and risk score. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes runnable malware-like test fixtures. <br>
Mitigation: Review the fixture contents before installation and remove or convert them into inert data for normal use. <br>
Risk: The safe-install workflow downloads code and can modify existing installed skills. <br>
Mitigation: Run safe-install in an isolated environment, use dry-run first for untrusted sources, and review scan findings before allowing installation. <br>
Risk: Static, pattern-based scanning can miss novel, heavily obfuscated, or runtime-only malicious behavior. <br>
Mitigation: Use this skill as an initial screening layer and require manual review or additional security tooling for high-risk deployments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LvcidPsyche/skill-bomb-dog-sniff) <br>
- [Publisher profile](https://clawhub.ai/user/LvcidPsyche) <br>
- [Declared project homepage](https://github.com/openclaw/skills/bomb-dog-sniff) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text or JSON scan reports, Markdown guidance, shell commands, and JavaScript configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include risk score, risk level, findings, severity breakdown, confidence, file and line references, and install/audit recommendations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter and package metadata state 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
