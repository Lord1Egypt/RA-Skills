## Description:

Fold and score biomolecular complexes and optionally profile ADMET to prioritize molecules in drug discovery pipelines via the refua-mcp server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jbenjoseph](https://clawhub.ai/user/jbenjoseph)

### License/Terms of Use:


## Use Case:

Developers and computational drug discovery teams use this skill to run Refua MCP workflows for complex folding, binding-affinity estimation, BoltzGen design workflows, and optional ADMET profiling when appropriate inputs are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned package installs and model downloads can introduce supply-chain risk.

Mitigation: Run the skill in an isolated virtualenv or container, pin reviewed package versions, and verify model asset sources where possible.

Risk: Default model and molecule asset caches may write to locations unsuitable for restricted or sensitive research environments.

Mitigation: Set cache directories deliberately before use, such as Boltz2 cache and BoltzGen molecule directory overrides.

Risk: Drug discovery predictions may be mistaken for wet-lab, clinical, or safety guidance.

Mitigation: Use outputs only as computational prioritization support and require domain review before synthesis, testing, or clinical decisions.

## Reference(s):

- [Refua skill page](https://clawhub.ai/jbenjoseph/skills/refua)
- [refua-mcp repository](https://github.com/agentcures/refua-mcp)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown with inline shell commands and MCP usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup and operation guidance for connecting an agent to the refua-mcp server; model results depend on user-provided molecular inputs and installed optional extras.]

## Skill Version(s):

0.4.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
