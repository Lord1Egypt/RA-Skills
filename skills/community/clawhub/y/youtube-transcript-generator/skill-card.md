## Description:

Download and generate clean, readable transcripts from any YouTube video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[floriandarroman](https://clawhub.ai/user/floriandarroman)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to extract readable transcript text from YouTube videos for note taking, review, quoting, and downstream content workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted timestamps option can cause unintended local Python code execution when the bundled script is run.

Mitigation: Validate the timestamps option before use and pass dynamic values to Python as arguments rather than interpolating them into source code.

Risk: The script writes transcript output to a local file.

Mitigation: Run the skill in a working directory where local transcript files are expected and review output paths before executing commands with untrusted input.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/floriandarroman/skills/youtube-transcript-generator)
- [Publisher profile](https://clawhub.ai/user/floriandarroman)
- [OpenClaw Lab guides and templates](https://openclawlab.xyz)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Guidance]

**Output Format:** [Plain text transcript written to stdout and a local .txt file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can optionally preserve timestamps and select a subtitle language when the script is invoked with supported arguments.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
