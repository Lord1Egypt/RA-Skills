## Description: <br>
Calls Tencent Cloud's DetectFace API to detect faces in images, returning face locations and optional face attribute or quality details from local files, Base64 input, or image URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoqiangjava](https://clawhub.ai/user/xiaoqiangjava) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Tencent Cloud face detection when they need face counts, bounding boxes, optional face attributes, or image quality scores. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected face images, Base64 image data, or image URLs are sent to Tencent Cloud for analysis. <br>
Mitigation: Process only images the user has permission to analyze, avoid unnecessary uploads, and follow the user's privacy and retention requirements. <br>
Risk: Optional attribute and quality detection can expose sensitive personal or biometric-adjacent information. <br>
Mitigation: Enable face attributes or quality detection only when needed for the task and avoid collecting or storing extra results. <br>
Risk: The script requires Tencent Cloud credentials in environment variables. <br>
Mitigation: Use least-privileged credentials, keep secrets out of prompts and logs, and rotate credentials according to the deployment policy. <br>


## Reference(s): <br>
- [Tencent Cloud DetectFace API Documentation](https://cloud.tencent.com/document/product/867/44989) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands] <br>
**Output Format:** [JSON printed by scripts/main.py, with progress and errors on stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes face count, bounding boxes, optional face attributes, optional quality scores, and Tencent Cloud RequestId.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
