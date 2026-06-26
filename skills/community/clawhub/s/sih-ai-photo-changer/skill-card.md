## Description: <br>
Sih.AI Photo Changer edits images from natural-language prompts, including background changes, clothing changes, face swaps, style conversion, and beauty retouching through the Sih.AI image API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a3273283](https://clawhub.ai/user/a3273283) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to transform a provided image using a natural-language editing prompt and receive generated image URLs from the service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Provided images and prompts may be uploaded to an external image API. <br>
Mitigation: Avoid sensitive, private, or non-consensual images and confirm the service privacy boundary before use. <br>
Risk: The artifact includes a hardcoded bearer token. <br>
Mitigation: Use a version that requires the user to provide their own API key through a secret or environment variable, and rotate any exposed token. <br>
Risk: The exact provider domain and data-handling boundary are not clearly disclosed. <br>
Mitigation: Verify the API provider and data retention terms before sending production or personal images. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/a3273283/sih-ai-photo-changer) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, JSON] <br>
**Output Format:** [JSON API response plus plain-text generated image URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated image URLs are documented as expiring after 24 hours.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
