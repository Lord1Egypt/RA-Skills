## Description:

Fail-closed security auditing for OpenClaw/ClawHub skills and repositories: trufflehog secrets scanning, semgrep SAST, prompt-injection and persistence signals, and supply-chain hygiene checks before enabling or installing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[virtaava](https://clawhub.ai/user/virtaava)

### License/Terms of Use:

MIT

## Use Case:

Developers and security reviewers use this skill to audit codebases and OpenClaw/ClawHub skill bundles for secrets, static-analysis findings, prompt-injection signals, persistence mechanisms, and supply-chain hygiene issues before enabling or installing them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The convenience wrapper can run an unreviewed hard-coded external audit script instead of the packaged runner.

Mitigation: Invoke artifact/scripts/run_audit_json.sh directly from the skill directory until the wrapper is fixed to call the packaged runner.

Risk: The advertised fail-closed behavior is not reliably enforced when callers rely only on the wrapper's shell exit status.

Mitigation: Parse the JSON .ok field and scanner error state, and treat scanner errors or ok=false as audit failure.

Risk: The audit processes untrusted repositories and skill bundles using subprocess-based scanners.

Mitigation: Run audits in a read-only, network-denied sandbox against an explicit target path.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/virtaava/skills/sona-security-audit)
- [OpenClaw Skill Manifest Schema](artifact/docs/OPENCLAW_SKILL_MANIFEST_SCHEMA.md)
- [Zero-Trust Install Workflow](artifact/docs/README_ZERO_TRUST_INSTALL.md)
- [OpenClaw Skill Manifest](artifact/openclaw-skill.json)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Analysis, Guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON audit reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audit strictness is configurable with OPENCLAW_AUDIT_LEVEL=standard|strict|paranoid; callers should parse the JSON ok field and scanner error state.]

## Skill Version(s):

0.1.3 (source: server release metadata and openclaw-skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
