## Description: <br>
Creates TikTok image carousels with text overlays via the ViralBaby API, including image search, slideshow editing, previewing, and upload to TikTok drafts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aryanbhasin](https://clawhub.ai/user/aryanbhasin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External creators, marketers, and agents assisting them use this skill to create photo-based TikTok slideshow drafts: search and select images, write slide text and captions, manage collections, preview drafts, and upload to TikTok drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated slideshow content, stored business/style preferences, TikTok draft-upload access, and diagnostic reports may be handled by ViralBaby. <br>
Mitigation: Install only if ViralBaby is trusted for this data, review or clear saved preferences when they contain sensitive business information, and ask the agent to confirm before sending feedback or error reports. <br>
Risk: The workflow asks the agent to persist ViralBaby credentials for reuse across sessions. <br>
Mitigation: Use a managed secret store where available, avoid saving sensitive passwords directly in environment variables, and rotate credentials if they are exposed. <br>
Risk: Connected TikTok access can upload generated slideshows to TikTok drafts. <br>
Mitigation: Complete TikTok authorization intentionally and review every uploaded draft in TikTok before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aryanbhasin/tiktok-slideshow) <br>
- [ViralBaby API](https://viralbaby.co) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON API payloads and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create ViralBaby slideshow resources and upload completed slideshows to TikTok drafts after user authorization.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
