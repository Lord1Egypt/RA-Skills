## Description: <br>
Generate, edit, and remix images using the Reve AI API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dpaluy](https://clawhub.ai/user/dpaluy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to call the Reve AI API for text-to-image generation, image editing, and reference-image remixing from a Bun CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts and provided input images to Reve for processing. <br>
Mitigation: Only provide prompts and images that are appropriate to process with Reve AI. <br>
Risk: The skill requires a Reve API key and consumes Reve API credits. <br>
Mitigation: Use a dedicated, revocable API key and monitor credit usage. <br>
Risk: API failures such as invalid credentials, insufficient credits, rate limits, or invalid input can interrupt generation. <br>
Mitigation: Check CLI JSON and error output, respect retry-after guidance, and validate prompts, aspect ratios, and remix image counts before use. <br>


## Reference(s): <br>
- [Reve API documentation](https://api.reve.com/console/docs) <br>
- [ClawHub skill page](https://clawhub.ai/dpaluy/reve-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, JSON] <br>
**Output Format:** [PNG image files written to disk plus JSON status output from the CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Reve API credits and reports model version, credits used, credits remaining, and content violation status when returned by the API.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
