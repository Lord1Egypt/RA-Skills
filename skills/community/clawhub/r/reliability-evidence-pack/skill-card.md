## Description: <br>
Provides tools to record, validate, and report agent operational reliability artifacts using standardized schemas for consistent monitoring and compliance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChristineOpenclaw](https://clawhub.ai/user/ChristineOpenclaw) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to create, validate, and report reliability evidence for agent decisions, handoffs, heartbeats, context snapshots, and related operational events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security summary says validation and integrity guarantees are materially weaker than the documentation suggests. <br>
Mitigation: Treat REP output as local logging and demo validation evidence, and do not rely on it as authoritative tamper-evident audit infrastructure without independent controls. <br>
Risk: Reliability artifacts can include context snapshots, decision logs, and memory-like records that may contain sensitive data. <br>
Mitigation: Store artifacts in an isolated access-controlled directory, redact sensitive content before sharing, and audit artifacts before external disclosure. <br>
Risk: The security guidance warns against the GitHub Action's automatic external package install path unless the dependency source is pinned and reviewed. <br>
Mitigation: Review the action entrypoint before CI use, pin package sources and versions, and prefer local reviewed scripts in automated workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ChristineOpenclaw/reliability-evidence-pack) <br>
- [Skill overview](artifact/SKILL.md) <br>
- [REP specification](artifact/SPEC.md) <br>
- [Quickstart guide](artifact/QUICKSTART.md) <br>
- [Integration guide](artifact/INTEGRATION.md) <br>
- [CLI README](artifact/cli/README.md) <br>
- [GitHub Action README](artifact/github-action/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON/JSONL artifact files, validation output, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local filesystem artifacts and configurable artifact, schema, and log paths.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
