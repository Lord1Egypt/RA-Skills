## Description: <br>
Review YouTube upload metadata and publish-readiness notes before a human handles the final upload. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, channel operators, and content teams use this skill to review YouTube titles, descriptions, thumbnail notes, tags, playlist choices, and upload-readiness details before a human performs the final upload. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may expose sensitive YouTube account data while asking for upload help. <br>
Mitigation: Provide only the content needed for review, and do not share YouTube credentials, cookies, recovery information, or private analytics exports. <br>
Risk: Readiness notes could be mistaken for confirmation that a video has been published. <br>
Mitigation: Require a user-provided public or unlisted URL before stating that a video is live. <br>
Risk: Metadata may contain unsupported claims, copyrighted media concerns, private personal information, or an incorrect made-for-kids audience setting. <br>
Mitigation: Have the human uploader review policy-sensitive claims, source support, copyright status, private information, audience choice, and missing assets before upload. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zack-dev-cm/youtube-openclaw-creator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown publish-readiness packet] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes cleaned metadata, tag and playlist recommendations, thumbnail notes, a human-upload checklist, and risks or missing assets; does not perform uploads or scheduling.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
