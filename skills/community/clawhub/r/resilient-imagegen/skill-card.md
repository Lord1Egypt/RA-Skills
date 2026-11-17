## Description:

Stabilize multi-image generation by converting prompts into a retryable serial job queue, inspecting runtime capabilities, routing through built-in ImageGen, ChatGPT Computer Use, manual handoff, local rendering, or a separately confirmed CLI/API fallback, and producing a manifest for downstream cards-to-images or article-to-illustrations workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangchao228](https://clawhub.ai/user/yangchao228)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content workflow authors use this skill to run multi-image generation as recoverable serial jobs with retries, backend selection, visual review, and manifest handoff. It is suited for card-image and article-illustration pipelines where interrupted or partially failed batches need to resume without losing progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference files, or generated outputs may be sent through Computer Use, manual handoff, or paid API fallback when those routes are approved.

Mitigation: Keep uploads and paid fallback disabled until explicit confirmation, and review prompts and generated files before submission or publishing.

Risk: An interrupted or partially failed image batch may be mistaken for a complete run.

Mitigation: Use the manifest to preserve job status, attempts, errors, output paths, and human review state before downstream handoff.

Risk: Generated images may contain inaccurate text, labels, dimensions, or factual details, especially for exact Chinese text.

Mitigation: Inspect every output and use deterministic typography or downstream rendering for exact text and factual diagrams.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangchao228/skills/resilient-imagegen)
- [OpenClaw homepage](https://github.com/yangchao228/my_open_skills/tree/main/skills/content/resilient-imagegen)
- [Publisher profile](https://clawhub.ai/user/yangchao228)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown run report with YAML manifest fields and optional handoff prompt pack]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes job status, attempt counts, selected backend, generated file paths, visual QA status, and fallback decision points.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
