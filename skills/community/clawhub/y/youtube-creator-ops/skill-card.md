## Description: <br>
OpenClaw YouTube Publisher helps publish a YouTube Short through a logged-in OpenClaw browser session while recording source provenance, publish steps, checks, screenshots, URLs, and a reusable report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, operators, and developers use this skill to run a visible YouTube Studio publishing workflow through OpenClaw and preserve a structured record of the upload, checks, final URL, screenshots, and upstream asset provenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A logged-in YouTube browser profile can expose account context if notes, manifests, screenshots, or reports capture sensitive details. <br>
Mitigation: Use the skill only with an intended logged-in profile, avoid cookies, tokens, private paths, and sensitive account details in artifacts, and review reports and screenshots before sharing. <br>
Risk: Authentication, CAPTCHA, passkey, 2FA, or the final publish action may require deliberate human control. <br>
Mitigation: Pause automation for manual authentication steps and keep the final publish click user-approved. <br>
Risk: Published content may depend on upstream asset licenses, attribution, or public credit requirements. <br>
Mitigation: Record Midjourney, Suno, or editor provenance in the manifest and include required public credits or attribution in the publish metadata. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zack-dev-cm/youtube-creator-ops) <br>
- [Project homepage](https://github.com/zack-dev-cm/youtube-creator-ops) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown reports, JSON manifests and check reports, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include redacted public URLs, relative artifact paths, screenshots, publish status, and provenance fields for upstream assets.] <br>

## Skill Version(s): <br>
1.1.5 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
