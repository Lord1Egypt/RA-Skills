## Description: <br>
Automates Chaoxing Xuexitong homework workflows, including assignment discovery, question fetching, answer template generation, draft saving, final submission, and a handwritten-image answer pipeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallwhiteman](https://clawhub.ai/user/smallwhiteman) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to operate Chaoxing Xuexitong homework flows through repeatable commands, including listing assignments, preparing answer files, saving drafts, and submitting only after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a live Chaoxing session cookie. <br>
Mitigation: Install and run it only when that account access is intended, keep the cookie file private with restrictive permissions, and rotate the cookie if exposure is suspected. <br>
Risk: The skill can save drafts or submit homework to a live Chaoxing account. <br>
Mitigation: Use draft-save first, review the result in Chaoxing, and use final submission only after explicit confirmation. <br>
Risk: The handwritten upload pipeline may expose cookies and answer images over plaintext HTTP. <br>
Mitigation: Avoid that pipeline on untrusted networks unless the user accepts the exposure risk. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smallwhiteman/xuexitong-homework-submit) <br>
- [Chaoxing Xuexitong homework API endpoint](https://mooc1-api.chaoxing.com/work/stu-work) <br>
- [Chaoxing upload endpoint used by handwritten pipeline](http://notice.chaoxing.com/pc/files/uploadNoticeFile) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, JSON, Files] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON or image file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create homework work files, answer templates, rendered PNG images, upload records, and save or submit result JSON.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
