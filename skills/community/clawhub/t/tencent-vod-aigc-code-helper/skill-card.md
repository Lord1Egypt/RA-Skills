## Description: <br>
Helps developers integrate Tencent Cloud VOD AIGC APIs for image generation, video generation, custom subjects, custom voices, task polling, callbacks, and SDK-based examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tencent-mpaas-skills](https://clawhub.ai/user/tencent-mpaas-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when building against Tencent Cloud VOD AIGC APIs and need implementation guidance, SDK examples, task-status handling, callback guidance, and billing reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated examples may call paid Tencent Cloud VOD AIGC APIs and create unexpected charges. <br>
Mitigation: Read current billing documentation before calling APIs, start with low-cost test parameters, and configure Tencent Cloud billing alerts or limits. <br>
Risk: Examples require Tencent Cloud credentials and a correct VOD SubAppId; misuse can expose keys or operate on the wrong sub-application. <br>
Mitigation: Use least-privilege credentials stored in environment variables, avoid hardcoding secrets, and verify the target SubAppId before running generated code. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tencent-mpaas-skills/tencent-vod-aigc-code-helper) <br>
- [Tencent Cloud VOD API overview](https://cloud.tencent.com/document/product/266/31753) <br>
- [CreateAigcImageTask documentation](https://cloud.tencent.com/document/product/266/126240) <br>
- [CreateAigcVideoTask documentation](https://cloud.tencent.com/document/product/266/126239) <br>
- [CreateAigcCustomElement documentation](https://cloud.tencent.com/document/product/266/127544) <br>
- [CreateAigcCustomVoice documentation](https://cloud.tencent.com/document/product/266/129120) <br>
- [DescribeTaskDetail documentation](https://cloud.tencent.com/document/product/266/33431) <br>
- [Tencent Cloud API key documentation](https://cloud.tencent.com/document/api/266/31757) <br>
- [Tencent Cloud VOD callback events](https://cloud.tencent.com/document/product/266/35579) <br>
- [Tencent Cloud VOD AIGC billing documentation](https://cloud.tencent.com/document/product/266/95125#9c4dc6ff-4b3f-4b25-bf2d-393889dfb9ac) <br>
- [Tencent Cloud International VOD AIGC billing documentation](https://www.tencentcloud.com/zh/document/product/266/14666#87e472ca-9c95-4658-ab7b-8f2130608419) <br>
- [Tencent Cloud SDK for Python](https://github.com/TencentCloud/tencentcloud-sdk-python) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with SDK code examples, shell commands, links, and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Examples may include Tencent Cloud credential environment variables, SubAppId configuration, polling logic, callback handling, and billing warnings.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
