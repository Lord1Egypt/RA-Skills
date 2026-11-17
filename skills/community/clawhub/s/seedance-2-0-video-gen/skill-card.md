## Description:

Generate Seedance 2.0 videos through WeryAI for text-to-video, image-to-video, multi-image video, and first-frame/last-frame transitions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[632657122](https://clawhub.ai/user/632657122)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and creators use this skill to generate WeryAI Seedance 2.0 videos from text prompts, HTTPS reference images, ordered image sequences, or first/last-frame controls after reviewing expanded prompt settings before paid execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid generation sends prompts, settings, task IDs, and public HTTPS reference-image URLs to WeryAI and can consume account credits.

Mitigation: Use dry-run and model checks before paid calls, require explicit confirmation before execution, and use a scoped or low-balance WERYAI_API_KEY where possible.

Risk: API endpoint override variables can route requests to a non-default endpoint.

Mitigation: Keep WERYAI_BASE_URL and WERYAI_MODELS_BASE_URL unset unless the endpoint is trusted.

Risk: Reference media must be public HTTPS URLs, which may expose image content to WeryAI during generation.

Mitigation: Use only media intended for that service and do not pass local, private, or sensitive file paths.

## Reference(s):

- [Seedance 2.0 Prompt Optimization](references/seedance-prompt-optimization.md)
- [ClawHub Skill Page](https://clawhub.ai/632657122/skills/seedance-2-0-video-gen)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with confirmation tables, shell command snippets, and JSON task results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns task IDs, status, and video URLs when generation succeeds; real runs are paid WeryAI tasks.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
