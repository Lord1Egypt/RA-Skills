## Description: <br>
Transforms clothing image URLs into professional e-commerce product photos with AI models wearing the garments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangyang-youloft](https://clawhub.ai/user/wangyang-youloft) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Fashion e-commerce teams, retail operators, and design teams use this skill to turn one to four garment images into model-based product photos for catalogs, marketplace listings, and design visualization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends referenced clothing image URLs and the user's workflow API key to a third-party image-processing API. <br>
Mitigation: Use scoped or revocable API keys, avoid sensitive or regulated images unless the provider's privacy and retention terms are acceptable, and review outbound URLs before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wangyang-youloft/virtual-try-on) <br>
- [Pixify product console](https://ai.ngmob.com) <br>
- [ngmob API base URL](https://api.ngmob.com) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Text, Guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and bash commands; workflow responses are JSON containing a generated image URL.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Pixify/ngmob API key and publicly accessible clothing image URLs; task status is retrieved through asynchronous polling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
