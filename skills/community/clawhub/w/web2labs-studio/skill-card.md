## Description: <br>
Edit my recording, turn a long video into shorts, generate captions and thumbnails, estimate cost before processing. Upload local files or YouTube/Twitch URLs and get back edited jump-cut videos, vertical shorts, subtitles, and thumbnail variants. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Vinlow](https://clawhub.ai/user/Vinlow) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External creators, streamers, podcasters, educators, and agents use this skill to upload or fetch recordings, estimate costs, process videos through Web2Labs Studio, retrieve edited videos, shorts, captions, metadata, and thumbnails, and manage related project assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload local media and metadata to Web2Labs for processing. <br>
Mitigation: Install only if you trust Web2Labs with the content you process, and use it only for media you own or have permission to edit. <br>
Risk: The skill can spend API or Creator Credits through processing, rush jobs, thumbnails, and rerenders. <br>
Mitigation: Set WEB2LABS_SPEND_POLICY=explicit when you want approval before paid actions, and review cost estimates before upload or batch processing. <br>
Risk: Watcher automation can repeatedly process new YouTube or Twitch uploads. <br>
Mitigation: Avoid watcher or scheduled automation unless recurring processing is intended, and configure daily upload and duration limits. <br>
Risk: The setup flow can save a Web2Labs API key in local OpenClaw configuration. <br>
Mitigation: Treat the saved API key in ~/.openclaw/openclaw.json as a secret and avoid exposing it in logs, messages, or shared files. <br>
Risk: Webhook callbacks send completion notifications to a configured URL. <br>
Mitigation: Review webhook URLs before use and configure webhook secrets for signed callback verification. <br>


## Reference(s): <br>
- [Web2Labs OpenClaw Landing Page](https://web2labs.com/openclaw) <br>
- [Web2Labs API Documentation](https://www.web2labs.com/api/v1/docs) <br>
- [Web2Labs Product Page](https://www.web2labs.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown and structured tool results with local file downloads when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include project IDs, output URLs, cost estimates, progress updates, webhook guidance, and downloaded media files.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence, package.json, claw.json, CHANGELOG, released 2026-02-23) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
