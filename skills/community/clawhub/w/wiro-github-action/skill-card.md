## Description:

Write GitHub Actions workflows that call Wiro AI with the Wiro AI Action (wiroai/Wiro-Action@v1). It runs any of 1,000+ models for images, video, audio and 3D, runs a saved Wiro AI workflow, or asks an LLM through the Wiro AI gateway, and returns URLs, files, text and the cost for later steps. Covers the inputs and outputs, the WIRO_API_KEY secret, the price estimate and the max-cost limit, and ready workflows for an image, a pull request summary, release media and a workflow run. Use when the user wants AI images, video, audio, text or reviews in GitHub Actions, mentions wiroai/Wiro-Action or a WIRO_API_KEY secret, or wants to run Wiro AI from CI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wiroai](https://clawhub.ai/user/wiroai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to write GitHub Actions workflows that generate media, run saved Wiro AI workflows, or request LLM responses, then use the returned files, URLs, text, and cost in later steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository diffs and other supplied files may be sent to an external AI service, including when working with private repositories.

Mitigation: Review which files the workflow submits and confirm that sending their contents to Wiro AI is permitted; exclude sensitive content when needed.

## Reference(s):

- [Wiro AI models](https://wiro.ai/models)
- [Wiro AI workflows](https://wiro.ai/workflows)

## Skill Output:

**Output Type(s):** [Configuration, Code, Guidance]

**Output Format:** [Markdown with YAML GitHub Actions workflow examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples cover model, saved workflow, and LLM modes, along with inputs, outputs, and cost limits.]

## Skill Version(s):

1.0.1 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
