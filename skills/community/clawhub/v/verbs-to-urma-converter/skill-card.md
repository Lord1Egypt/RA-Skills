## Description: <br>
Migrate RDMA verbs code to URMA API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[derricjs](https://clawhub.ai/user/derricjs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to migrate RDMA Verbs or libibverbs applications to the URMA API while preserving source files and producing converted code in a separate output directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated URMA networking and token-exchange code may be unsafe if used directly in production. <br>
Mitigation: Require authenticated encrypted control channels, validate peer identity, avoid fixed or plaintext tokens, and review remote memory metadata handling before production use. <br>
Risk: The skill can activate broadly around RDMA, InfiniBand, RoCE, verbs, or URMA migration language. <br>
Mitigation: Install it only when explicit verbs-to-URMA migration assistance is needed and review generated migration plans before execution. <br>


## Reference(s): <br>
- [URMA API Mapping Reference](references/mapping.md) <br>
- [URMA Code Patterns and Best Practices](references/patterns.md) <br>
- [Common Pitfalls and Solutions](references/pitfalls.md) <br>
- [URMA Complete Working Example](references/urma_sample.md) <br>
- [OpenEuler UMDK Source Repository](https://atomgit.com/openeuler/umdk) <br>
- [ClawHub Skill Page](https://clawhub.ai/derricjs/verbs-to-urma-converter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, migration checklists, and converted project files when applied by an agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Converted code is expected under urma_output/ with original files left unchanged.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
