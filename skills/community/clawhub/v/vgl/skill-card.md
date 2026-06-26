## Description: <br>
Vgl helps agents produce structured VGL JSON that explicitly controls object placement, lighting, camera settings, composition, color scheme, and style for Bria FIBO image workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[galbria](https://clawhub.ai/user/galbria) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative operators use this skill to convert natural-language image requests, edits, masked edits, captions, or refinements into structured VGL JSON for controllable Bria FIBO image generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated image prompts can include sensitive appearance attributes or misleading descriptions of people. <br>
Mitigation: Review generated VGL JSON before use and include sensitive appearance attributes only when they are necessary for the requested image. <br>
Risk: The skill documents a Bria API example that relies on an API key. <br>
Mitigation: Keep API keys in environment variables and do not paste credentials into prompts, generated JSON, or shared artifacts. <br>


## Reference(s): <br>
- [VGL Output Schema Reference](references/schema-reference.md) <br>
- [Bria image generation API endpoint](https://engine.prod.bria-api.com/v2/image/generate) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Guidance] <br>
**Output Format:** [Single valid JSON object following the VGL schema] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes required visual-description fields for generation, edit, masked edit, caption, and refinement modes; no shell execution or automatic API calls.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
