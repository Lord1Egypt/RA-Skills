## Description: <br>
Generates short AI scene video clips from storyboard prompts or reference images using configured providers such as Jimeng, Kling, Runway, Pika, or Vidu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OliviaPp8](https://clawhub.ai/user/OliviaPp8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content production teams use this skill to turn storyboard or scene descriptions, optionally with reference images, into short AI-generated scene clips for stitching into larger videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured video providers receive prompts, reference images, and related generation metadata. <br>
Mitigation: Use only trusted providers and avoid submitting confidential prompts, unreleased assets, personal photos, or regulated data unless the provider terms are acceptable. <br>
Risk: Provider API keys and access credentials can be exposed through shared files, logs, or source control. <br>
Mitigation: Store credentials as secrets, keep them out of shared files and Git, and rotate keys if exposure is suspected. <br>
Risk: External video generation can incur provider charges and may take longer than expected. <br>
Mitigation: Monitor provider spending limits, start with small batches, and use asynchronous handling for render waits. <br>
Risk: Complex actions, multi-person scenes, and provider-specific prompt limits can produce unstable or low-quality results. <br>
Mitigation: Review generated clips before downstream stitching, keep prompts concise, and save seeds for reproducing acceptable outputs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/OliviaPp8/scene-video-generator) <br>
- [Backend Setup Guide](references/backend-setup.md) <br>
- [Prompt Optimization Guide](references/prompt-guide.md) <br>
- [Jimeng API Documentation](https://www.volcengine.com/docs/jimeng/) <br>
- [Kling API Documentation](https://docs.qingque.cn/d/home/eZQClV8BFVPVr2FVHI_0p0FUu) <br>
- [Runway API Documentation](https://docs.runwayml.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, API Calls, Guidance] <br>
**Output Format:** [Markdown guidance with YAML-style video metadata examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces provider-selected short video clip metadata such as URL, duration, resolution, prompt, seed, and status; actual video generation depends on configured external provider credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
