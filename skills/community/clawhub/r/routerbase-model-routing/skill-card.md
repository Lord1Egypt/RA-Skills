## Description:

Choose RouterBase model IDs and routing strategies for chat, image, video, audio, and embeddings workloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zenlee123](https://clawhub.ai/user/zenlee123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to compare RouterBase model options, design primary and fallback routing plans, and document model-routing decisions for applications that use RouterBase's OpenAI-compatible API surface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide agents to query RouterBase catalog or pricing APIs using an existing ROUTERBASE_API_KEY.

Mitigation: Review proposed API calls before execution, provide credentials only through the intended environment, and restrict invocation text when the skill should be used only for explicit RouterBase requests.

Risk: RouterBase model IDs, availability, and prices can change with upstream providers.

Mitigation: Verify catalog and pricing data at recommendation time and include the check status in routing plans.

Risk: A fallback model may not support the same request features, such as tool calling, vision, JSON mode, context size, prompt caching, or streaming.

Mitigation: Test the exact request shape and validation fixture before production use, and keep fallback models compatible with the required modality and features.

## Reference(s):

- [RouterBase Model Routing Notes](references/routerbase-models.md)
- [RouterBase](https://routerbase.com)
- [RouterBase Models API](https://routerbase.com/api/v1/models?task=chat)
- [RouterBase Pricing API](https://routerbase.com/api/v1/pricing)
- [RouterBase Model Pricing API](https://routerbase.com/api/v1/models/{model_id}/pricing)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, API call examples, code snippets, and validation checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include RouterBase catalog and pricing check status, model IDs, fallback rationale, caveats, and minimal evaluation fixtures.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
