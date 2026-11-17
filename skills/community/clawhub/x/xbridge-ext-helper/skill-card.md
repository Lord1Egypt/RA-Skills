## Description:

Helps developers use xbridge3 extension fields by explaining indexed and JSON-only extension data, schema annotations, DAO and service handling, and reference Java examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongwangwangyangyan](https://clawhub.ai/user/dongwangwangyangyan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when adding country-specific transaction extension fields in xbridge3, configuring @EntityColumnSchema mappings, and reading or persisting extension data in DAO and service layers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference DAO and processor examples may be copied into financial transaction systems with unsafe access-control, logging, or audit-trail patterns.

Mitigation: Review generated code before use; require tenant-scoped queries and updates, avoid logging full transaction objects, and decide whether audit-history saves must be mandatory for the compliance model.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dongwangwangyangyan/skills/xbridge-ext-helper)
- [xbridge extension field usage guide](references/xbridge-ext-use.md)
- [ExtensionUtils.java](references/ExtensionUtils.java)
- [VNCommonExtension.java](references/VNCommonExtension.java)
- [VNTransactionExtension.java](references/VNTransactionExtension.java)
- [VNTransactionProcessor.java](references/VNTransactionProcessor.java)
- [TransactionDAO.java](references/TransactionDAO.java)
- [TransactionConverter.java](references/TransactionConverter.java)

## Skill Output:

**Output Type(s):** [Guidance, Code, Markdown, Configuration instructions]

**Output Format:** [Markdown with Java code examples and implementation steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include DAO, service, converter, schema annotation, and extension utility examples for xbridge3 transaction extension fields.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
