## Description: <br>
Upload, schedule, and batch-manage TikTok videos via browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xmuweili](https://clawhub.ai/user/xmuweili) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and content operators use this skill to prepare agent guidance and wrapper code for uploading, scheduling, and batch-managing TikTok videos through browser automation. It is not intended for TikTok analytics, video downloading, comment management, or follower management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill needs TikTok account session access and can upload or schedule posts on the user's behalf. <br>
Mitigation: Prefer a local cookie-file path over raw session values, keep the cookie file private, rotate or revoke the session if exposed, and verify each video, caption, visibility setting, and schedule before upload. <br>
Risk: Browser automation can be fragile when TikTok changes its web upload flow, and batch activity can be throttled. <br>
Mitigation: Use small batches, space out uploads, retry with a visible browser for debugging, and update the tiktok-uploader and Playwright dependencies when selector or upload failures occur. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xmuweili/tiktok-uploader) <br>
- [tiktok-uploader Project](https://github.com/wkaisertexas/tiktok-uploader) <br>
- [Publisher Profile](https://clawhub.ai/user/xmuweili) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes guidance for cookie-based authentication, upload options, scheduling limits, batch uploads, and local video scanning.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
