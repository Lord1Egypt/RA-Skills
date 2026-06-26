## Description: <br>
Provides a structured multi-agent deliberation framework with role schemas (action/guardian/observer/critic), verification protocols, and stopping criteria. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tatsuko-tsukimi](https://clawhub.ai/user/tatsuko-tsukimi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to structure multi-agent deliberations for architecture, strategy, methodology, or other non-trivial review work where disagreement, evidence, role coverage, and stopping criteria need to be explicit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Python scripts create, append, and validate files in user-selected state and artifact directories. <br>
Mitigation: Run the scripts only in intended project directories and review generated claims, verifications, decisions, and artifacts before relying on them. <br>
Risk: The round controller is a skeleton that requires user-provided LLM API integration. <br>
Mitigation: Review any added API client, credential handling, and network behavior before execution. <br>
Risk: Poorly configured roles or skipped stress tests can make deliberation output look more robust than it is. <br>
Mitigation: Complete role configuration, run the validation scripts, preserve evidence references, and use the documented stopping criteria before synthesis. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tatsuko-tsukimi/structured-deliberation) <br>
- [Role Schemas](references/role-schemas.md) <br>
- [Cross-Validation Protocol](references/verification-protocol.md) <br>
- [Claims + Verifications Infrastructure](references/claims-infrastructure.md) <br>
- [Stopping Criteria](references/stopping-criteria.md) <br>
- [Failure Modes](references/failure-modes.md) <br>
- [Condensed Deliberation Example](examples/condensed-deliberation.md) <br>
- [Stress Test Walkthrough](examples/stress-test-walkthrough.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSONL schemas, Python helper scripts, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces claims, verifications, decisions, role prompts, round plans, and validation guidance for a user-managed deliberation run.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
