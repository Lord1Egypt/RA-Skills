## Description: <br>
Fail-closed security auditing for OpenClaw/ClawHub skills and repos: trufflehog secrets scanning, semgrep SAST, prompt-injection and persistence signals, and supply-chain hygiene checks before enabling or installing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[virtaava](https://clawhub.ai/user/virtaava) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and security reviewers use this skill to run fail-closed audits of OpenClaw/ClawHub skills or codebases before enabling, installing, or promoting them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A bundled convenience wrapper may run from a hard-coded local workspace and report success even when the audit fails. <br>
Mitigation: Use the main command, bash scripts/run_audit_json.sh <path>, and check the JSON .ok result; avoid using scripts/security_audit.sh for CI or install gates unless it is patched to use the bundled runner by relative path, require an explicit target, and propagate failure status. <br>
Risk: The audit depends on local scanner tools, so missing jq, trufflehog, semgrep, or python3 can prevent a complete result. <br>
Mitigation: Install the required tools before use and treat missing-tool results as failed audits until the environment is fixed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/virtaava/sona-security-audit) <br>
- [OpenClaw Skill Manifest Schema](docs/OPENCLAW_SKILL_MANIFEST_SCHEMA.md) <br>
- [Zero-trust install workflow](docs/README_ZERO_TRUST_INSTALL.md) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance and JSON audit output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Audit results are emitted as JSON; shell examples expect jq, trufflehog, semgrep, and python3.] <br>

## Skill Version(s): <br>
0.1.3 (source: openclaw-skill.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
