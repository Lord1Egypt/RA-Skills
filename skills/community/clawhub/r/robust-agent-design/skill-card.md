## Description: <br>
Apply robust Agent design patterns for building fault-tolerant, state-driven automation systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bhbb2000](https://clawhub.ai/user/bhbb2000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design or refactor agent systems that need high reliability, state persistence, retry behavior, compensation transactions, graceful degradation, and coordinated recovery across distributed components. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example code may persist state files in shared /tmp paths or retain sensitive task data if reused directly. <br>
Mitigation: Move persisted state to controlled storage with restrictive permissions, avoid storing secrets or raw task data, and apply retention and redaction rules. <br>
Risk: Example workflows include email, SMS, and payment-adjacent actions that can have real-world effects when adapted to production. <br>
Mitigation: Require explicit human approval and environment-specific safeguards before enabling real email, SMS, payment, or purchasing actions. <br>
Risk: Rollback and compensation examples are instructional and may be incomplete for production business logic. <br>
Mitigation: Add tests for rollback behavior, failure ordering, idempotency, and recovery paths before deploying derived implementations. <br>


## Reference(s): <br>
- [Robust Agent Design Skill](https://clawhub.ai/bhbb2000/robust-agent-design) <br>
- [Agent Template Reference](artifact/references/agent_template.py) <br>
- [Compensation Example Reference](artifact/references/compensation_example.py) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code] <br>
**Output Format:** [Markdown guidance with Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces design patterns, checklists, architecture guidance, and reusable Python examples for robust agent workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
