## Description: <br>
TencentCloud VITA helps agents analyze images, image sequences, and public video URLs with Tencent Cloud's VITA multimodal media understanding service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wayne-j151](https://clawhub.ai/user/wayne-j151) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to submit images, image sequences, or public video URLs to TencentCloud VITA for media description, summarization, event analysis, highlight extraction, and prompt-driven visual understanding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Media and prompts are sent to TencentCloud VITA for processing, which can expose private or sensitive content to an external service. <br>
Mitigation: Use this skill only when Tencent Cloud processing is acceptable, and avoid submitting private or sensitive media unless approved for the use case. <br>
Risk: The skill requires a TencentCloud VITA API key in the environment. <br>
Mitigation: Use a dedicated API key with appropriate scope, store it outside the artifact, and rotate it if exposure is suspected. <br>
Risk: A saved VITA prompt can change future analysis behavior unexpectedly. <br>
Mitigation: Review or reset the persisted prompt before relying on analysis results, especially in shared environments. <br>
Risk: Video inputs must be public or otherwise accessible URLs, and local videos are not uploaded by the script. <br>
Mitigation: Upload local videos with an approved separate tool and pass only URLs whose access level is appropriate for the media. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wayne-j151/tencentcloud-vita) <br>
- [TencentCloud VITA service management](https://console.cloud.tencent.com/tiia/vita-service-management) <br>
- [TencentCloud VITA API endpoint](https://api.vita.cloud.tencent.com/v1/video2text) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON result with usage metadata by default, or streamed text when streaming is enabled] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TENCENTCLOUD_VITA_API_KEY; local images are converted to data URLs, while local videos require separate upload to an accessible URL.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
