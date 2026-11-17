## Description:

Provides a structured multi-agent deliberation framework with role schemas, verification protocols, and stopping criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tatsuko-tsukimi](https://clawhub.ai/user/tatsuko-tsukimi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to design and run non-trivial multi-agent deliberations, especially architecture, strategy, or methodology reviews where explicit claims, cross-agent verification, and stopping criteria are needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reference scripts have implementation quality issues and should not be treated as production-ready automation.

Mitigation: Review and test the scripts before using them for consequential deliberations.

Risk: JSONL parse failures or weak evidence references can reduce the reliability of claims, verifications, and decisions.

Mitigation: Tighten JSONL error handling and restrict evidence references to approved project paths and real anchors before relying on outputs.

Risk: Stopping decisions may be misleading if the detector math is not calibrated for the user's deliberation setup.

Mitigation: Review and calibrate the stopping-detector logic against representative deliberation runs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tatsuko-tsukimi/skills/structured-deliberation)
- [Role Schemas](references/role-schemas.md)
- [Verification Protocol](references/verification-protocol.md)
- [Claims Infrastructure](references/claims-infrastructure.md)
- [Stopping Criteria](references/stopping-criteria.md)
- [Failure Modes](references/failure-modes.md)
- [Condensed Deliberation Example](examples/condensed-deliberation.md)
- [Stress Test Walkthrough](examples/stress-test-walkthrough.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with JSONL schemas, shell commands, and Python reference code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a deliberation protocol and optional local state files such as claims.jsonl, verifications.jsonl, and decisions.jsonl when adopted by the user.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
