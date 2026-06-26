## Description: <br>
Extracts YouTube video transcripts and provides concise summaries highlighting main points, arguments, and conclusions without watching the full video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vovavvk](https://clawhub.ai/user/vovavvk) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
External users and developers use this skill to extract available YouTube captions and turn them into structured summaries of long videos. It is intended for quick review of educational, news, documentary, or reference videos without watching the full recording. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using browser cookies for restricted YouTube videos can expose an authenticated account session. <br>
Mitigation: Prefer public YouTube videos without cookies. If cookies are used, treat the cookie file like a password, keep it out of shared folders and source control, and delete it after use. <br>
Risk: The extractor disables certificate checks, which can make network interception harder to detect. <br>
Mitigation: Avoid untrusted networks unless certificate checking is restored, especially when using cookies or other sensitive session material. <br>
Risk: Videos without captions, restricted videos, or inaccurate auto-generated captions can produce missing or misleading summaries. <br>
Mitigation: Use the summaries as a review aid, verify important claims against the source video, and inform users when captions are unavailable or extraction fails. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/vovavvk/tldw) <br>
- [Original TL;DW Project](https://github.com/stong/tldw) <br>
- [TL;DW Website](https://tldw.tube) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summary with optional JSON transcript metadata from the extractor.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an available YouTube caption track; may use a local transcript cache and optional browser cookies for restricted videos.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
