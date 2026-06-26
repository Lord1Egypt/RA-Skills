## Description: <br>
Connects an agent to Bria.ai image generation, editing, background removal, upscaling, and product photography workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[levdavid1](https://clawhub.ai/user/levdavid1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content teams use this skill to generate and edit images through Bria.ai, including background removal, product photos, upscaling, and batch visual-asset workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send selected prompts and images to Bria.ai for processing. <br>
Mitigation: Use it only when the user intends to use Bria.ai, and avoid private, regulated, or internal-only images unless Bria's terms and account settings are acceptable. <br>
Risk: The skill stores Bria credentials in a local credentials file for reuse. <br>
Mitigation: Protect the local credentials file, avoid shared environments, and remove ~/.bria/credentials when the skill should no longer make Bria API calls. <br>
Risk: The skill broadly activates for image-related requests and may trigger external API usage. <br>
Mitigation: Confirm that the requested image workflow should use Bria.ai before running API calls, especially for sensitive inputs or cost-controlled accounts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/levdavid1/test-security) <br>
- [Bria API reference for agents](https://docs.bria.ai/llms.txt) <br>
- [API Endpoints Reference](references/api-endpoints.md) <br>
- [Shell Client](references/code-examples/bria_client.sh) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline bash commands and API call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return Bria-hosted image URLs or API error messages when used.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
