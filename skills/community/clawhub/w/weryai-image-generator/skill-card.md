## Description:

Generate WeryAI images from text prompts or reference images through the WeryAI image APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weryai-developer](https://clawhub.ai/user/weryai-developer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create text-to-image or image-to-image generations with WeryAI, inspect supported image models, submit asynchronous image tasks, and check image task status with bounded polling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send API keys, prompts, and local files to network destinations.

Mitigation: Install only in trusted runtimes, keep WERYAI_API_KEY secret, and provide local file paths only when those files are intended for upload.

Risk: Custom WERYAI_BASE_URL and WERYAI_MODELS_BASE_URL values can redirect requests away from the default WeryAI hosts.

Mitigation: Leave host overrides unset unless the replacement endpoints are trusted and reviewed.

Risk: Generic npx/bun launch behavior has lower assurance than the reviewed task, status, and model entry points.

Mitigation: Prefer reviewed commands such as submit, status, models, wait, and balance entry points for normal use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weryai-developer/skills/weryai-image-generator)
- [WeryAI API keys](https://www.weryai.com/api/keys)
- [WeryAI Image Generation Models](artifact/references/api-models.md)
- [WeryAI Error Codes](artifact/references/error-codes.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and JSON command output with image links when generation results are ready]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return task IDs, batch IDs, task status, generated image URLs, balance information, model metadata, and structured error details.]

## Skill Version(s):

0.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
