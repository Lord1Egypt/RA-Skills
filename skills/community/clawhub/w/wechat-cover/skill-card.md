## Description:

Generate WeChat official account cover images with proper 2.35:1 aspect ratio. Supports OpenAI DALL-E and Gemini image generation with customizable styles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[derekdong-star](https://clawhub.ai/user/derekdong-star)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to generate WeChat official account cover PNGs from article titles and topics, using OpenAI or Gemini as the image provider.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles API credentials and supports custom provider URLs.

Mitigation: Use trusted HTTPS provider endpoints, prefer separate low-privilege API keys, and do not let untrusted content choose base URL or API key values.

Risk: The skill can download externally generated images and write output files.

Mitigation: Write outputs to a dedicated directory with simple filenames, and do not let untrusted content choose filename or output directory values.

Risk: Article titles and topics are sent to external image generation providers.

Mitigation: Avoid sensitive unpublished titles or topics when configuring prompts for provider calls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/derekdong-star/skills/wechat-cover)
- [OpenAI Platform API Keys](https://platform.openai.com/api-keys)
- [Google AI Studio API Keys](https://aistudio.google.com/app/apikey)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions]

**Output Format:** [PNG image file with terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are cropped and resized to 900x383 for the WeChat cover aspect ratio.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
