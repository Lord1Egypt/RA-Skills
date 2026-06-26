## Description: <br>
Generate professional, structured PowerPoint presentations from optimized topic keywords. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dzy-1026](https://clawhub.ai/user/Dzy-1026) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, educators, and business users use this skill to turn optimized presentation topics into structured PowerPoint decks for reports, strategy planning, technical presentations, training, and academic summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Presentation topics and generated content requests are sent to iFLYTEK using the configured API credentials. <br>
Mitigation: Use only inputs approved for that third-party data flow and avoid sensitive or confidential presentation content unless your organization has approved it. <br>
Risk: The document-outline helper can send local files or document URLs to the third-party service. <br>
Mitigation: Do not invoke the document-outline helper for confidential local files or private URLs unless that workflow has been explicitly approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Dzy-1026/xfyun-ppt-gen) <br>
- [iFLYTEK PPT API documentation](https://www.xfyun.cn/doc/spark/PPTv2.html) <br>


## Skill Output: <br>
**Output Type(s):** [files, text] <br>
**Output Format:** [PowerPoint deck plus CLI status text and a download URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires XF_PPT_APP_ID and XF_PPT_API_SECRET; one invocation creates one deck from an optimized topic.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
