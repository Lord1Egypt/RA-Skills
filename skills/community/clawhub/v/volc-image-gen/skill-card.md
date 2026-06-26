## Description: <br>
Use Volc Engine AI to generate, edit, batch produce, and create variations of images with customizable styles and sizes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rfdiosuao](https://clawhub.ai/user/rfdiosuao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content-producing teams use this skill to call Volcengine Ark image-generation services for text-to-image, image editing, batch generation, and image-variation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and input images are sent to Volcengine for processing. <br>
Mitigation: Avoid confidential or regulated prompts and images unless the deployment has approved Volcengine processing for that data. <br>
Risk: API keys, prompts, local paths, and generated file locations can appear in runtime logs or local output. <br>
Mitigation: Use a dedicated low-quota VOLC_API_KEY, restrict log access, and avoid including secrets or sensitive paths in prompts and filenames. <br>
Risk: Changing VOLC_API_BASE can route prompts and images to a non-default service. <br>
Mitigation: Keep VOLC_API_BASE on the official Volcengine endpoint unless another endpoint has been explicitly reviewed and trusted. <br>
Risk: Generated outputs and downloaded input images may remain on disk under /tmp/openclaw. <br>
Mitigation: Review retention expectations and clean /tmp/openclaw after workflows that use sensitive source images or generated results. <br>


## Reference(s): <br>
- [ClawHub Volc Image Gen Listing](https://clawhub.ai/rfdiosuao/volc-image-gen) <br>
- [Volcengine Ark Documentation](https://www.volcengine.com/docs/82379) <br>
- [Volcengine Ark Console](https://console.volcengine.com/ark) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files, API calls, guidance] <br>
**Output Format:** [JSON responses with generated image URLs, local file paths, usage metadata, and error details; help output is structured JSON guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated and input images may be written under /tmp/openclaw; repeated text-to-image requests can be served from an in-memory cache for one hour.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
