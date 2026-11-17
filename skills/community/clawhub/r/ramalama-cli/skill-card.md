## Description:

Run and interact with AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ieaves](https://clawhub.ai/user/ieaves)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to run RamaLama workflows for local or containerized model inference, OpenAI-compatible serving, RAG packaging, benchmarking, and model lifecycle operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts or RAG paths may include private data that is processed by local or containerized model workflows.

Mitigation: Review prompts and RAG inputs before execution, and avoid packaging sensitive files unless the environment is approved for that data.

Risk: Detached serving can expose an OpenAI-compatible endpoint on a host and port.

Mitigation: Verify host and port exposure before running `ramalama serve -d`, resolve port conflicts, and stop the service when finished.

## Reference(s):

- [Model Guide](references/models.md)
- [RamaLama CLI Skill on ClawHub](https://clawhub.ai/ieaves/skills/ramalama-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes RamaLama command recipes, preflight checks, troubleshooting guidance, and model-selection reference material.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
