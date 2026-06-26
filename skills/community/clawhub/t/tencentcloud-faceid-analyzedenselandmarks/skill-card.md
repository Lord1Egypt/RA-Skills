## Description: <br>
Calls Tencent Cloud's AnalyzeDenseLandmarks face recognition API to return dense facial landmark coordinates from a Base64 image or image URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoqiangjava](https://clawhub.ai/user/xiaoqiangjava) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to send permitted face images or image URLs to Tencent Cloud and receive dense landmark coordinates for face alignment, contour analysis, or facial feature localization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Face images or image URLs are sent to Tencent Cloud for processing. <br>
Mitigation: Process only images the user has permission to submit and avoid unnecessary sensitive face data. <br>
Risk: Tencent Cloud API credentials are required to run the skill. <br>
Mitigation: Use a least-privilege API key, store credentials in environment variables, and monitor usage. <br>


## Reference(s): <br>
- [Tencent Cloud AnalyzeDenseLandmarks API Documentation](https://cloud.tencent.com/document/product/867/47397) <br>
- [ClawHub skill page](https://clawhub.ai/xiaoqiangjava/tencentcloud-faceid-analyzedenselandmarks) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON response with image dimensions, face count, face rectangles, dense landmark coordinate arrays, keypoint counts, and request ID.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Tencent Cloud credentials and sends the supplied face image or URL to Tencent Cloud for processing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
