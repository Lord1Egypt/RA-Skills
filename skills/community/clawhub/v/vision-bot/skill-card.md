## Description: <br>
Vision Bot helps agents describe images, detect objects, extract text, count visual elements, and analyze webpage screenshots from user-provided image tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unixlamadev-spec](https://clawhub.ai/user/unixlamadev-spec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Use for accessibility descriptions, OCR from screenshots or photos, object identification and counting, multilingual image analysis, and visual review of webpage screenshots when external image processing is acceptable. <br>

### Deployment Geography for Use: <br>
Global, subject to the user's organization, local laws, service availability, and restrictions for external image processing. <br>

## Known Risks and Mitigations: <br>
Risk: Image URLs, screenshots, OCR targets, webpage references, and task text are sent to a disclosed external API. <br>
Mitigation: Use this skill only when external processing is acceptable, avoid confidential images or private internal URLs, and review the request content before submission. <br>
Risk: The skill requires an AIPROX_SPEND_TOKEN for paid API access. <br>
Mitigation: Use a spend-limited token where possible and manage it as a secret in the agent environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/unixlamadev-spec/vision-bot) <br>
- [Publisher Profile](https://clawhub.ai/user/unixlamadev-spec) <br>
- [Project Homepage](https://aiprox.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Natural-language analysis and structured examples for image description, object detection, OCR, counting, and webpage screenshot review.] <br>
**Output Parameters:** [Accepts an image URL in the task string or a separate image_url field, task text that selects the analysis mode, and AIPROX_SPEND_TOKEN in the environment for API access.] <br>
**Other Properties Related to Output:** [Responses follow the language of the user's task and may include descriptions, detected objects, extracted text, and visual observations.] <br>

## Skill Version(s): <br>
1.2.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
