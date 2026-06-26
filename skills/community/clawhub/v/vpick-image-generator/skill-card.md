## Description: <br>
VPick AI Image Generator helps agents create and manage multi-model AI image generation on a visual canvas with prompts, reference images, style transfer, batch generation, and aspect ratio control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snoopyrain](https://clawhub.ai/user/snoopyrain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to generate and organize images through VPick's canvas using multiple image models, prompts, reference images, and batch workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and uploaded reference images are sent through VPick and downstream model providers. <br>
Mitigation: Avoid sensitive or confidential prompts and images unless that external processing is acceptable. <br>
Risk: The MCP Connector URL contains an authentication token. <br>
Mitigation: Keep the connector URL private and rotate or replace it if it is exposed. <br>
Risk: Batch, fast, or high-resolution generations can consume VPick credits. <br>
Mitigation: Check model pricing and generation history before running large batches. <br>


## Reference(s): <br>
- [VPick MCP Connection Guide](https://vpick-doc.10xboost.org/guide/mcp-connection.html) <br>
- [VPick App](https://vpick.10xboost.org) <br>
- [ClawHub Skill Listing](https://clawhub.ai/snoopyrain/vpick-image-generator) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides calls to VPick canvas and image-generation tools; generated images are stored by VPick under the user's account.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
