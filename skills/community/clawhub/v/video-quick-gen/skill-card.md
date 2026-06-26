## Description: <br>
Generates marketing video scripts and videos through Xiaonian AI from a user's requirement, returning the generated script and final video URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yc556600](https://clawhub.ai/user/yc556600) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing teams and agents use this skill when a user wants a marketing-video request turned directly into a generated video through Xiaonian AI instead of manually writing the script and production steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends video requirements and optional image URLs to xiaonian.cc, with unclear account and data-handling boundaries. <br>
Mitigation: Use only when the user accepts sending that content to xiaonian.cc, and avoid submitting confidential requirements or private image URLs unless the service terms and retention practices are understood. <br>
Risk: The release uses an embedded dashboard access token. <br>
Mitigation: Rotate and remove the embedded token before broader use, and require credentials supplied explicitly by the user or deployment environment. <br>
Risk: Generated videos can be downloaded to a local path selected by the caller. <br>
Mitigation: Write downloads only to explicit, trusted output paths and review the resulting file before sharing or deploying it. <br>


## Reference(s): <br>
- [Video Gen API](references/video-api.md) <br>
- [Xiaonian dashboard API](https://xiaonian.cc/employee-console/dashboard/v2/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, files] <br>
**Output Format:** [JSON containing the generated script, task ID, video URL, and optional downloaded file path.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May download the generated video to a caller-provided local path when requested.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
