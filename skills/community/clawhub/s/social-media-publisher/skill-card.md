## Description: <br>
Daily social media posting with NewsAPI for PayLessTax & LevelUpLove. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wespeakallday](https://clawhub.ai/user/wespeakallday) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Marketing operators and automation agents use this skill to create daily branded posts for PayLessTax and LevelUpLove from news headlines or prepared one-liners, render accompanying images, and publish them to connected social accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish public social media posts using connected account credentials without built-in review or clear account controls. <br>
Mitigation: Use restricted, revocable API keys, confirm the UploadPost destination accounts outside the skill, and run the workflow in dry-run or manual review mode before enabling a schedule. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wespeakallday/social-media-publisher) <br>
- [NewsAPI endpoint](https://newsapi.org/v2) <br>
- [Templated.io render endpoint](https://api.templated.io/v1/render) <br>
- [UploadPost photo upload endpoint](https://api.upload-post.com/api/upload_photos) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Configuration, JSON] <br>
**Output Format:** [JSON status output plus externally published social media posts and rendered image URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided NewsAPI, Templated.io, and UploadPost credentials and brand-specific configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
