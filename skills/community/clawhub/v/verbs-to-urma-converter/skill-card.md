## Description: <br>
Migrates RDMA Verbs (libibverbs) code to the URMA API with API mapping, data structure conversion, and URMA-specific optimization guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[derricjs](https://clawhub.ai/user/derricjs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to migrate RDMA, InfiniBand, RoCE, or libibverbs projects to URMA while preserving original files and producing converted code under urma_output/. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation can apply the migration workflow to RDMA or verbs-related requests where code conversion was not intended. <br>
Mitigation: Install and invoke the skill only for intentional verbs/libibverbs-to-URMA migration work. <br>
Risk: Generated networking and remote-memory code can introduce unsafe peer exchange, fixed or plaintext tokens, or unvalidated peer identity. <br>
Mitigation: Require authenticated encrypted peer exchange, avoid fixed or plaintext tokens, validate peer identity, and review generated code before production use. <br>
Risk: Automated migration can leave semantic issues that compilation does not catch, including resource leaks, incomplete cleanup, or verbs residue. <br>
Mitigation: Review all output under urma_output/, verify lifecycle and cleanup paths, scan for verbs residue, and build and test before running the converted project. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/derricjs/skills/verbs-to-urma-converter) <br>
- [URMA/UMDK source repository](https://atomgit.com/openeuler/umdk) <br>
- [URMA API Mapping Reference](references/mapping.md) <br>
- [URMA Code Patterns and Best Practices](references/patterns.md) <br>
- [Common Pitfalls and Solutions](references/pitfalls.md) <br>
- [URMA Complete Working Example](references/urma_sample.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code edits, shell commands, verification summaries, and generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces converted files under urma_output/ while preserving the original source tree.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
