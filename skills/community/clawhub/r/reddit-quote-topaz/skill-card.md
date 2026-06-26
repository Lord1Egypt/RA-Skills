## Description: <br>
Creates an Instagram carousel from a popular-picks page using Reddit quotes, Topaz 2x photo upscaling, text overlays, and Instagram publishing steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[psyduckler](https://clawhub.ai/user/psyduckler) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Content creators or social media operators use this skill to turn a destination and category page into a Topaz-enhanced Instagram carousel with Reddit quote overlays and publishing guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use stored Topaz and Instagram credentials and publish generated carousel content without an explicit review gate. <br>
Mitigation: Review images, captions, source rights, destination account, and generated repository changes before any publish step, and use narrowly scoped credentials where possible. <br>
Risk: Generated images may be pushed to a repository before being used as Instagram carousel media. <br>
Mitigation: Inspect repository changes and hosted image URLs before publishing, and remove temporary hosted files after the post is complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/psyduckler/reddit-quote-topaz) <br>
- [Topaz Labs image enhance endpoint](https://api.topazlabs.com/image/v1/enhance) <br>
- [Topaz Labs async image enhance endpoint](https://api.topazlabs.com/image/v1/enhance/async) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown instructions with JSON examples and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces carousel slide specifications, local image file paths, API calls, captions, and publishing steps for an agent workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
