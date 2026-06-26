## Description: <br>
Cloud-based video enhancement skill that uploads a user-selected local MP4 or MOV video to Wondershare-hosted endpoints for AI enhancement, then downloads the processed result to local storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[double-ing](https://clawhub.ai/user/double-ing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to enhance, upscale, or clarify a local non-sensitive MP4 or MOV video after explicit consent to third-party cloud processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow uploads the selected video, checksum, metadata, locale, and a stable hashed device identifier to Wondershare-hosted cloud services. <br>
Mitigation: Use only after explicit user consent, and do not use it for confidential or sensitive media. <br>
Risk: Task IDs or status URLs may appear in local logs or transcripts during processing. <br>
Mitigation: Avoid sharing logs from processing sensitive material and keep responses focused on the saved output path and necessary warnings. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/double-ing/video-enhancer) <br>
- [Wondershare cloud API base endpoint](https://filmora-cloud-api-alisz.wondershare.cc) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Enhanced video file saved to disk with concise Markdown status guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves output using the pattern <input_stem>_hd_YYYYMMDD_HHMMSS.<ext>.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
