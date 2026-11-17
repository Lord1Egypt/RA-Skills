## Description:

Guides an agent through generating NSFW AI videos with ZenCreator.pro using image-to-video, video-to-video, and lipsync workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[makforce](https://clawhub.ai/user/makforce)

### License/Terms of Use:


## Use Case:

Developers and content operators use this skill to guide an agent in operating a logged-in ZenCreator.pro session for AI video generation and downloading clips. It is relevant when the user intentionally provides source media, prompts, and approval for any credit-spending generation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent operation of a logged-in browser session could upload files, submit prompts, or spend credits unintentionally.

Mitigation: Use only intentionally selected files, keep the session scoped, and require explicit confirmation before uploads, generation, downloads, or credit-spending actions.

Risk: Uploaded media and generated NSFW content may be subject to ZenCreator.pro's current terms and privacy practices.

Mitigation: Review the service's current terms and privacy practices before use, and avoid uploading sensitive material unless those practices are acceptable.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/makforce/skills/zencreator-video-skill)
- [ZenCreator.pro](https://zencreator.pro)
- [ZenCreator app](https://app.zencreator.pro)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown instructions with browser automation examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve browser actions, local file uploads, and credit-spending steps in an external service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
