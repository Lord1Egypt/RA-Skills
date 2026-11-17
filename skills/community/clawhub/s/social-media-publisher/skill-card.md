## Description:

Daily social media posting with NewsAPI for PayLessTax & LevelUpLove.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wespeakallday](https://clawhub.ai/user/wespeakallday)

### License/Terms of Use:


## Use Case:

Marketing operators and agent developers use this skill to generate scheduled social posts for PayLessTax and LevelUpLove by fetching headlines or rotating one-liners, rendering branded images, and publishing to selected social platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish posts externally on a schedule.

Mitigation: Require human approval or a dry run before scheduled posts go live.

Risk: The workflow depends on API keys and JSON configuration files.

Mitigation: Use least-privilege keys, protect config files, and avoid passing secrets on the command line.

Risk: The skill makes outbound requests to content, rendering, and publishing providers.

Mitigation: Restrict outbound access to the intended NewsAPI, Templated.io, and UploadPost domains.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wespeakallday/skills/social-media-publisher)
- [NewsAPI Endpoint](https://newsapi.org/v2)
- [Templated.io Render API](https://api.templated.io/v1/render)
- [UploadPost Photo Upload API](https://api.upload-post.com/api/upload_photos)

## Skill Output:

**Output Type(s):** [JSON, API Calls, Files, Social media posts]

**Output Format:** [JSON status object plus externally published image-and-caption posts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NewsAPI, Templated.io, and UploadPost credentials; scheduled publication should use a dry run or human approval before posts go live.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 2.7.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
