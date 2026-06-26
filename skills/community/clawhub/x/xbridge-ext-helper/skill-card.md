## Description: <br>
Helps developers use extension fields in the xbridge3 framework, including country-specific transaction extensions, EntityColumnSchema mappings, ExtensionUtils access patterns, index-field allocation, and schema configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dongwangwangyangyan](https://clawhub.ai/user/dongwangwangyangyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design, implement, read, write, and troubleshoot xbridge3 transaction extension fields, especially country-specific extensions and indexed JSON-backed fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Java examples may be reused in financial transaction systems without adequate production review. <br>
Mitigation: Review examples before implementation, add validation and tests around extension-field save/load behavior, and adapt the code to local data-handling requirements. <br>
Risk: Reference code includes production caveats such as full transaction payload logging and audit-history handling concerns. <br>
Mitigation: Remove full transaction payload logging and restore or redesign audit-history handling before using similar patterns in a real system. <br>


## Reference(s): <br>
- [Transaction Extension Fields Usage Guide](references/xbridge-ext-use.md) <br>
- [ExtensionUtils.java](references/ExtensionUtils.java) <br>
- [VNCommonExtension.java](references/VNCommonExtension.java) <br>
- [VNTransactionExtension.java](references/VNTransactionExtension.java) <br>
- [VNTransactionProcessor.java](references/VNTransactionProcessor.java) <br>
- [TransactionDAO.java](references/TransactionDAO.java) <br>
- [TransactionConverter.java](references/TransactionConverter.java) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown with Java code examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only output; examples should be reviewed before use in production systems.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
