## Description: <br>
Generate images using the WuyinKeji GPT-Image-2 API (速创科技), including text-to-image, reference images, multiple aspect ratios, and async result polling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alex-shen1121](https://clawhub.ai/user/alex-shen1121) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to submit WuyinKeji GPT-Image-2 text-to-image or reference-image generation jobs, poll for async completion, and download generated image files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires WuyinKeji API credentials and the evidence warns that key handling may expose credentials through command history, process listings, or URL logs. <br>
Mitigation: Use a scoped or disposable API key, avoid reusing sensitive credentials, and prefer a revised workflow that avoids literal keys and query-string credentials. <br>
Risk: Prompts and reference image URLs are sent to a third-party image-generation service. <br>
Mitigation: Avoid sensitive prompts, private reference images, or confidential URLs unless the service and account terms are acceptable for the data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alex-shen1121/wuyin-gpt-image2) <br>
- [WuyinKeji async image API endpoint](https://api.wuyinkeji.com/api/async/image_gpt) <br>
- [WuyinKeji async detail endpoint](https://api.wuyinkeji.com/api/async/detail) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, files] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces helper-script usage guidance and can download generated PNG image files through the WuyinKeji API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
