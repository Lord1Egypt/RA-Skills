## Description: <br>
TencentCloud Text AIGC Detection helps an agent send user-provided text to Tencent Cloud TextModeration to identify likely AI-generated content and return structured detection results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawn233](https://clawhub.ai/user/shawn233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and review teams use this skill to check text supplied directly, from a file, or from standard input for likely AI-generated content. It is intended for article screening, moderation review, news authenticity checks, and similar text-analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Checked text is sent to Tencent Cloud for processing. <br>
Mitigation: Avoid submitting confidential, regulated, or proprietary text unless the user's data-handling rules allow Tencent Cloud processing. <br>
Risk: The skill requires Tencent Cloud credentials to call the service. <br>
Mitigation: Use least-privilege or temporary credentials where possible, keep credentials in environment variables, and do not hardcode secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shawn233/tencentcloud-aigc-recog-text) <br>
- [TextModeration API reference](references/text_moderation_api.md) <br>
- [Tencent Cloud TextModeration documentation](https://cloud.tencent.com/document/product/1124/51860) <br>
- [Tencent Cloud SDK guide](https://cloud.tencent.com/document/product/1124/100983) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON responses with optional setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Consumes text from an argument, file, or stdin; requires Tencent Cloud credentials and a BizType.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
