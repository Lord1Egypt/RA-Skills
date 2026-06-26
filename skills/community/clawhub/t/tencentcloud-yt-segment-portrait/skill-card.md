## Description: <br>
Binary classification-based human portrait segmentation for complete body contour recognition and image matting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Neck-cn](https://clawhub.ai/user/Neck-cn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to send a selected portrait image or image URL to Tencent Cloud SegmentPortraitPic and return portrait segmentation results for matting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected portrait images or image URLs are sent to Tencent Cloud and may contain personal data. <br>
Mitigation: Use this skill only with images approved for Tencent Cloud processing and avoid sending sensitive portraits unless the deployment policy permits it. <br>
Risk: Tencent Cloud API credentials may incur charges or be exposed if stored in shared shell profiles. <br>
Mitigation: Use least-privilege Tencent Cloud credentials, prefer short-lived or isolated environment configuration, and avoid committing or sharing secrets. <br>
Risk: The script can install the Tencent Cloud SDK at runtime if it is missing. <br>
Mitigation: Preinstall and pin the Tencent Cloud SDK in a controlled virtual environment before use. <br>


## Reference(s): <br>
- [TencentCloud YT Segment Portrait on ClawHub](https://clawhub.ai/Neck-cn/tencentcloud-yt-segment-portrait) <br>
- [SegmentPortraitPic API Reference](references/SegmentPortraitPicApi.md) <br>
- [Tencent Cloud SegmentPortraitPic Documentation](https://cloud.tencent.com/document/product/1208/42970) <br>
- [Tencent Cloud Portrait Segmentation Console](https://console.cloud.tencent.com/bda/segment-portrait-pic) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON response with ResultImageUrl and ResultMaskUrl, plus Markdown setup and execution guidance in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Tencent Cloud API credentials and network access; returned image and mask URLs may be time-limited.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
