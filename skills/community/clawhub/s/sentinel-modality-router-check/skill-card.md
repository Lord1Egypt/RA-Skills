## Description:

Confirms Sentinel's PII redaction guardrail survives routing through a modality-aware LiteLLM router to text and vision backends, checks routing correctness for each modality, and links a Jaeger trace when tracing is available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mark-stadtmueller](https://clawhub.ai/user/mark-stadtmueller)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run a local health check that verifies Sentinel redaction and modality routing across text and image requests before relying on the gateway for sensitive workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the skill can restart and reconfigure the local Sentinel gateway, briefly interrupting other workflows that depend on it.

Mitigation: Run it only in environments where the operator is authorized to restart the gateway and where brief local gateway interruption is acceptable.

Risk: If Telegram variables are configured, diagnostic pass/fail data, trace links, and short failure snippets may leave the local machine.

Mitigation: Leave Telegram variables blank for local-only output, or treat Telegram delivery as intentional external diagnostic egress.

Risk: Adapting the skill to real user prompts or untrusted webhook arguments could expose real prompt content or unsafe configuration values.

Mitigation: Add validation, redaction, and confirmation controls before accepting prompts or configuration from any source outside the operator-managed environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mark-stadtmueller/skills/sentinel-modality-router-check)
- [Superwise PII redaction documentation](https://docs.superwise.ai/docs/pii-redaction)
- [Superwise MCP documentation](https://docs.superwise.ai/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown status report with pass/fail results, routing checks, optional failure snippets, and an optional Jaeger trace link.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can print locally and optionally send the same diagnostic result through Telegram when Telegram environment variables are configured.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill.py SKILL_META)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
