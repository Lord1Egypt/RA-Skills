## Description: <br>
Extracts auto-generated caption transcripts from privacy-locked, domain-restricted Vimeo embeds by using the allowed host page as the Referer and downloading the exposed VTT caption track. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heavenchenggong](https://clawhub.ai/user/heavenchenggong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and analysts use this skill to retrieve available Vimeo caption text from domain-restricted embeds when they are authorized to access the host page and need transcript-driven analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can be used to bypass Vimeo domain/privacy restrictions or a publisher's intended access controls. <br>
Mitigation: Use only for videos and captions you are authorized to access; prefer official transcripts, publisher permission, or Vimeo-supported access. <br>
Risk: Extracted captions may violate publisher terms, copyright expectations, or paywall restrictions. <br>
Mitigation: Confirm rights and terms before downloading, storing, or redistributing transcript text. <br>
Risk: Auto-generated captions may contain transcription errors in names, acronyms, or numbers. <br>
Mitigation: Review transcript text against the source context before using it for decisions or publication. <br>


## Reference(s): <br>
- [Vimeo Player text-tracks documentation](https://developer.vimeo.com/player/sdk/reference#texttrack) <br>
- [WebVTT specification](https://www.w3.org/TR/webvtt1/) <br>
- [ClawHub skill page](https://clawhub.ai/heavenchenggong/vimeo-locked-captions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and transcript text outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces VTT and plain-text transcript files when the suggested commands are executed; caption accuracy depends on Vimeo-provided tracks.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
