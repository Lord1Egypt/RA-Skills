## Description:

Generates AI images from text prompts using Tencent Cloud HunYuan Text-to-Image, with support for reference images, resolution control, prompt rewriting, seed-based reproducibility, and asynchronous job polling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neck-cn](https://clawhub.ai/user/neck-cn)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to submit Tencent Cloud HunYuan text-to-image jobs, optionally guide generation with reference image URLs, and poll for result image URLs. It is suited to AI art, illustration, poster, cover, and other text-to-image workflows that can use Tencent Cloud credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically install an unpinned Tencent Cloud SDK at runtime.

Mitigation: Preinstall and pin the Tencent Cloud SDK in an isolated environment before using the skill.

Risk: The skill uses Tencent Cloud credentials and makes external API calls.

Mitigation: Use least-privilege temporary credentials and review the environment before running the scripts.

Risk: Prompts and reference image URLs are submitted to Tencent Cloud.

Mitigation: Avoid submitting private prompts or private image URLs unless that disclosure is intended.

## Reference(s):

- [Submit Text-to-Image API](references/submit_text_to_image_api.md)
- [Query Text-to-Image API](references/query_text_to_image_api.md)
- [Tencent Cloud SubmitTextToImageProJob documentation](https://cloud.tencent.com/document/product/1668/124632)
- [Tencent Cloud QueryTextToImageProJob documentation](https://cloud.tencent.com/document/product/1668/124633)
- [Tencent Cloud AIART console](https://console.cloud.tencent.com/aiart)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, JSON, Configuration guidance, Text]

**Output Format:** [JSON results and error messages, with Markdown usage guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns job IDs, polling status, generated image URLs, optional result details, and optional revised prompts; generated image URLs are time-limited.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
