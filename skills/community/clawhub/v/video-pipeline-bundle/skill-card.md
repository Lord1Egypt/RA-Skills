## Description:

Video Pipeline Bundle helps agents run a complete video-processing workflow that trims silence, transcribes speech to subtitles, burns subtitles into video, concatenates clips, and coordinates those steps with user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leochens](https://clawhub.ai/user/leochens)

### License/Terms of Use:


## Use Case:

Developers and content operations teams use this skill to process batches of raw videos into edited outputs with generated subtitles, burned-in captions, optional concatenation, and transcript text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server scan reports command-execution flaws around user-controlled paths.

Mitigation: Run the workflow only on trusted directories and filenames, review commands before execution, and prefer an isolated container or virtual environment.

Risk: The workflow can modify the Python environment when dependency installation paths are used.

Mitigation: Install dependencies in an isolated virtual environment or container after reviewing the scripts.

Risk: API keys may be exposed if passed on the command line, and transcript correction sends text to the selected LLM provider.

Mitigation: Use environment variables or secret management for API keys, avoid command-line secrets, use restricted keys, and avoid sending sensitive transcripts unless provider handling is acceptable.

Risk: Optional Feishu notifications can disclose filenames or workflow status to the configured target.

Mitigation: Disable notifications unless needed and set notification targets only to trusted recipients.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leochens/skills/video-pipeline-bundle)
- [MiniMax Open Platform](https://platform.minimaxi.com/)

## Skill Output:

**Output Type(s):** [shell commands, files, text, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; generated artifacts include video files, SRT subtitles, and text transcripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call local video tools and configured LLM APIs when the user runs the provided workflow scripts.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
