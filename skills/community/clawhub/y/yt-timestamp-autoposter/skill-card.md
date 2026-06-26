## Description: <br>
Generate SEO-optimized YouTube timestamps from a YouTube URL or a raw transcript string, then optionally append them to the description of that specific video or your latest upload. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robj1925](https://clawhub.ai/user/robj1925) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, channel operators, and agents use this skill to generate concise YouTube chapter timestamps from a video URL, transcript text, or the latest channel upload, with an option to append the generated timestamps to a YouTube description. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Posting mode can update live YouTube video descriptions without a final confirmation. <br>
Mitigation: Run the skill without --post first, review the generated timestamps and target video, then use --post only when the update is intended. <br>
Risk: The local token.pickle file can authorize future YouTube channel updates. <br>
Mitigation: Keep token.pickle out of shared storage and version control, delete it when access is no longer needed, and revoke access from Google Account permissions if needed. <br>
Risk: Transcript text is sent to Gemini for timestamp generation. <br>
Mitigation: Avoid submitting confidential or sensitive transcript content unless that sharing is acceptable for the channel workflow. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/robj1925/yt-timestamp-autoposter) <br>
- [Google Cloud Console](https://console.cloud.google.com/) <br>
- [Google AI Studio](https://aistudio.google.com/) <br>
- [Google Account permissions](https://myaccount.google.com/permissions) <br>
- [YouTube OAuth scope](https://www.googleapis.com/auth/youtube.force-ssl) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text timestamp block and Markdown usage guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Gemini API key for generation; posting mode requires local YouTube OAuth credentials and can update video descriptions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
