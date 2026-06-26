## Description: <br>
Veo, Veo 3.1 Fast - Google AI video generation models for AI agents. 1080p HD output, reference image support, intelligent audio generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seekton](https://clawhub.ai/user/seekton) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to create and monitor Monet-hosted Google Veo video generation tasks, including text-to-video and image-guided video workflows with optional audio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, reference images, uploaded files, and generated outputs are sent to Monet's hosted service. <br>
Mitigation: Use only content approved for Monet processing, and avoid secrets, confidential media, private customer data, regulated content, or other sensitive inputs unless Monet's terms are approved for that use. <br>
Risk: The skill requires a MONET_API_KEY for authenticated API requests. <br>
Mitigation: Store the API key in environment configuration or a secrets manager, avoid hard-coding it in prompts or source files, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/seekton/veo-skill) <br>
- [Monet](https://monet.vision) <br>
- [Monet API Keys](https://monet.vision/skills/keys) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with bash, TypeScript, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MONET_API_KEY; video generation tasks are asynchronous and should be polled until success or failure.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
