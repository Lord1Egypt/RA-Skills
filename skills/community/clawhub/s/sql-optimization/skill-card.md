## Description: <br>
Deep SQL performance workflow—symptom framing, execution plans, indexing strategy, query rewrite, locking/transaction behavior, statistics, partitioning, and verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codekungfu](https://clawhub.ai/user/codekungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database engineers use this skill to diagnose slow SQL queries, execution plan regressions, lock waits, indexing trade-offs, and production-like verification paths before changing database behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated DDL, index, timeout, or transaction advice can affect correctness, availability, write load, or lock behavior if applied directly to production. <br>
Mitigation: Review proposed changes with a database owner, test against production-like data, and apply them in staging or during a planned production change window with a rollback path. <br>
Risk: Prompts may include sensitive SQL parameters, credentials, or customer data while diagnosing database performance. <br>
Mitigation: Redact credentials, tokens, and sensitive customer values before sharing query text, logs, plans, or schema details with an agent. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with SQL, DDL, configuration, and verification recommendations when relevant] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include engine-specific caveats, measurement checklists, indexing rationale, rollback notes, and staging or production-change-window guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
