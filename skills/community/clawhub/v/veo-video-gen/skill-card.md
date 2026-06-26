## Description: <br>
Generate videos using Pixwith API's Veo 3.1 model with text-to-video and image-to-video workflows, including Fast preview and Pro HD-with-audio tiers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tate-kt](https://clawhub.ai/user/tate-kt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create AI-generated videos from prompts or supplied start/end frame images through the Pixwith API. It helps agents check credits, choose the appropriate generation tier, upload reference images when needed, create tasks, poll status, and return resulting video URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and reference images are sent to Pixwith and upload storage providers. <br>
Mitigation: Avoid confidential images or sensitive prompt text unless Pixwith is trusted for that data. <br>
Risk: The Pixwith API key is required for authenticated API requests. <br>
Mitigation: Install only when Pixwith is trusted with the API key and provide the key through the runtime's standard secret or environment mechanism. <br>
Risk: Prompt optimization may change exact wording. <br>
Mitigation: Disable prompt optimization when exact wording matters. <br>
Risk: Video generation consumes Pixwith credits and has Fast and Pro cost tiers. <br>
Mitigation: Confirm the credit tier and available balance before creating video tasks. <br>


## Reference(s): <br>
- [Pixwith](https://pixwith.ai) <br>
- [Pixwith API Dashboard](https://pixwith.ai/api) <br>
- [Pixwith Pricing](https://pixwith.ai/pricing) <br>
- [ClawHub Skill Page](https://clawhub.ai/tate-kt/veo-video-gen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns exact Pixwith task IDs, upload URLs, image URLs, and result URLs without modification.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
