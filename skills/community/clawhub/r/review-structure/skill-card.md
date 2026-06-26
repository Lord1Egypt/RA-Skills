## Description: <br>
Repo-wide structural-maintainability review — code-judo restructurings, 1k-line file guard, anti-spaghetti branching, canonical-layer enforcement, anti-magic abstractions, explicit type/boundary contracts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to perform strict structural code reviews of repository changes, focusing on maintainability, abstraction quality, boundary clarity, and opportunities to simplify implementations without changing behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read and quote repository files while reviewing structural changes. <br>
Mitigation: Use it only in repositories where file inspection is appropriate, and review cited findings before acting on them. <br>
Risk: Structural review recommendations could be incorrect or misleading if the agent misreads the changed files or repository context. <br>
Mitigation: Require the skill's artifact-backed gates, including changed-file capture, full-file reads, line counts, and cited search evidence, before accepting findings. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Shell commands] <br>
**Output Format:** [Markdown review with cited file, line, and command evidence plus recommended restructuring steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the agent to inspect changed files, quote reviewed artifacts, and cite search or line-count evidence before issuing structural findings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
