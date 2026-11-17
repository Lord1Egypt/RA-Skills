## Description:

Configure LLM providers, use fallback models, handle streaming, and manage model settings in PydanticAI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to select PydanticAI model providers, configure model settings, implement fallback behavior, stream responses, and track usage limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples require API keys for model providers and could expose credentials if copied into production or shared scripts.

Mitigation: Keep API keys in environment variables or a platform secret store.

Risk: Custom provider endpoints can route prompts and outputs to unintended services.

Mitigation: Review any custom base_url or provider endpoint before sending data to it.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration]

**Output Format:** [Markdown guidance with Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; no files, commands, or runtime actions are produced directly.]

## Skill Version(s):

1.0.1 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
