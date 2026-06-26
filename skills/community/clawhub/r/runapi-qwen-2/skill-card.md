## Description: <br>
Generate and edit images with Qwen 2 through RunAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runapi-ai](https://clawhub.ai/user/runapi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents, developers, and creative users use this skill to generate, transform, or edit images with Qwen 2 through RunAPI. For one-off image tasks it guides CLI usage; for application work it points to RunAPI SDKs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and images may be sent to RunAPI for processing. <br>
Mitigation: Avoid sending secrets, private images, or regulated data unless that processing is intentional and approved. <br>
Risk: The skill depends on the Homebrew-installed runapi CLI and local CLI credentials. <br>
Mitigation: Install only if you trust RunAPI, keep the runapi binary current, and review saved CLI credentials before use. <br>


## Reference(s): <br>
- [RunAPI Qwen 2 model page](https://runapi.ai/models/qwen-2) <br>
- [Qwen 2 model overview, pricing, and rate limits](https://runapi.ai/models/qwen-2.md) <br>
- [Alibaba provider comparison](https://runapi.ai/providers/alibaba.md) <br>
- [RunAPI model catalog](https://runapi.ai/models.md) <br>
- [Qwen 2 text-to-image variant](https://runapi.ai/models/qwen-2/text-to-image.md) <br>
- [Qwen 2 image-to-image variant](https://runapi.ai/models/qwen-2/image-to-image.md) <br>
- [Qwen 2 image edit variant](https://runapi.ai/models/qwen-2/image-edit.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, JSON request-file guidance, and SDK package names.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the runapi CLI for one-off tasks and names SDK packages for JavaScript/TypeScript, Ruby, and Go integrations.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
