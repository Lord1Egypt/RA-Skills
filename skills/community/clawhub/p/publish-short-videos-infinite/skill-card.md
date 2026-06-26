## Description: <br>
Coordinates browser automation for a short-video workflow across Kuaishou, Douyin, and Xiaohongshu, publishing to Kuaishou and saving Douyin and Xiaohongshu as drafts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[infiniteask](https://clawhub.ai/user/infiniteask) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators and social-media operators use this skill to run a sequential multi-platform short-video upload workflow with one video file, reused browser state, and platform-specific metadata settings. It is intended for workflows that need Kuaishou published first, then Douyin and Xiaohongshu saved as drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automates actions against live social-media accounts and publishes to Kuaishou while Douyin and Xiaohongshu are saved as drafts. <br>
Mitigation: Confirm the video file, target accounts, per-platform settings, and final action for each platform before browser automation starts. <br>
Risk: Users may misunderstand which platforms are published live versus saved as drafts. <br>
Mitigation: Treat Kuaishou as the live publish step and Douyin and Xiaohongshu as draft-save steps unless updated release evidence says otherwise. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/infiniteask/publish-short-videos-infinite) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/infiniteask) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands] <br>
**Output Format:** [Markdown instructions with ordered browser automation steps and local sub-skill paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Delegates to three local platform-specific skills and should be run only after confirming the video file, target accounts, platform settings, and final action.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
