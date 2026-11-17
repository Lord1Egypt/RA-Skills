## Description:

Provides tools to record, validate, and report agent operational reliability artifacts using standardized schemas for consistent monitoring and compliance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[christineopenclaw](https://clawhub.ai/user/christineopenclaw)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to capture runtime reliability evidence, validate REP artifacts, and generate reports for debugging, monitoring, compliance review, and handoff workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Validation paths may mislead operators about pass/fail status.

Mitigation: Review the scripts before use, prefer direct local validation scripts until failure behavior is confirmed, and require validation to fail closed in CI.

Risk: Reliability artifacts and logs can contain sensitive context, decisions, or memory-like records.

Mitigation: Store REP artifacts in an isolated access-controlled directory, redact sensitive lines before sharing, and define retention limits for generated records.

Risk: Packaged CLI and GitHub Action use can introduce installation or CI exposure risk.

Mitigation: Pin package installation, review the GitHub Action entrypoint before public CI use, and keep artifact paths isolated from externally published outputs.

Risk: Serving sensitive bundles may expose artifacts if not bound and protected correctly.

Mitigation: Do not run serve-style commands on sensitive bundles unless bound to loopback and protected by appropriate access controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/christineopenclaw/skills/reliability-evidence-pack)
- [REP specification](artifact/SPEC.md)
- [Quickstart guide](artifact/QUICKSTART.md)
- [Integration guide](artifact/INTEGRATION.md)
- [GitHub Action validation workflow](artifact/github-action/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON files]

**Output Format:** [Markdown guidance with command examples, JSON and JSONL artifacts, schemas, and validation reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes reliability artifacts, logs, and reports to configured local paths.]

## Skill Version(s):

2.0.2 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
