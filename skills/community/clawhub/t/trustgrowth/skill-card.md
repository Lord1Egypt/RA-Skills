## Description:

Use when TrustGrowth is already connected or the user asks to connect it, authenticate, discover its API/MCP capabilities, or use persisted growth evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trustgrowth](https://clawhub.ai/user/trustgrowth)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and growth operators use this skill to connect agents to TrustGrowth, inspect available REST or MCP capabilities, and retrieve persisted SEO and growth evidence for verified sites. It supports evidence-grounded reporting and routing to other Groundcrew skills without inventing endpoints or filling missing measurements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run an unbundled local validator before using evidence in conclusions.

Mitigation: Verify the local groundcrew-doctor.py script and stop if connectivity or evidence validation fails.

Risk: Credentials may be sent to a configurable API base.

Mitigation: Pin TRUSTGROWTH_API_BASE to the official TrustGrowth origin and never print TRUSTGROWTH_API_KEY.

Risk: The callable surface includes write actions such as audit triggers, strategy regeneration, and content or review workflow actions.

Mitigation: Require explicit owner approval before any write, audit trigger, strategy regeneration, or content/review workflow action.

## Reference(s):

- [TrustGrowth contract](references/contract.md)
- [Connectors and categories](references/connectors.md)
- [Reporting contract](references/reporting.md)
- [TrustGrowth developer documentation](https://trustgrowth.ai/developers)
- [WHY-NOT-SLOP](https://github.com/techwright-lab/groundcrew-seo/blob/main/WHY-NOT-SLOP.md)
- [ETHICS](https://github.com/techwright-lab/groundcrew-seo/blob/main/ETHICS.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, markdown, JSON]

**Output Format:** [Markdown guidance with inline commands, REST paths, MCP tool names, and evidence/reporting conventions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should preserve null values, source labels, rate-limit handling, and evidence provenance from the TrustGrowth and Groundcrew contracts.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
