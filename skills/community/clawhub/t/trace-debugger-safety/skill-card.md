## Description:

Safer end-to-end trace debugging from trace_id using Jaeger and Elasticsearch with guarded Codex analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gakkiismywife](https://clawhub.ai/user/gakkiismywife)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and reliability engineers use this skill to generate trace debug reports from Jaeger spans and Elasticsearch logs, with optional repository context for suspected bug areas. It is intended for controlled troubleshooting workflows where logs and generated reports may contain sensitive operational data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The implementation contradicts its safety claims and may expose logs, repository content, or attacker-selected local file lines during analysis.

Mitigation: Review carefully before installing, use only in a tightly controlled environment, and run against a trusted or disposable repository path.

Risk: Untrusted logs can influence Codex analysis and generated troubleshooting guidance.

Mitigation: Use trusted logs, a sandboxed Codex configuration, and do not rely on the documented no-Codex or no-hardcoded-repository behavior until the implementation is fixed.

Risk: Generated reports may contain sensitive logs, filesystem paths, source snippets, and Codex output.

Mitigation: Treat reports as sensitive artifacts and review or redact them before sharing outside the troubleshooting team.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gakkiismywife/skills/trace-debugger-safety)
- [Publisher profile](https://clawhub.ai/user/gakkiismywife)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown trace debug report plus a concise text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report may include Jaeger span tables, Elasticsearch log excerpts, bug hypotheses, repair suggestions, repository file matches, and Codex analysis output when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
