## Description: <br>
Converts text scripts and articles into MP3 podcast audio using text-to-speech. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utopiabenben](https://clawhub.ai/user/utopiabenben) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to convert articles, scripts, and Markdown or text files into podcast-style MP3 audio. It supports single-file and batch conversion, voice selection, speed control, and preview generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected text to OpenAI for speech generation. <br>
Mitigation: Do not convert secrets, regulated data, or private drafts unless that external processing is acceptable. <br>
Risk: The skill requires an OpenAI API key and installs Python dependencies with pip. <br>
Mitigation: Install only in an environment where providing the API key and installing those dependencies are acceptable. <br>
Risk: Configuration and output paths may need verification before use. <br>
Mitigation: Check the .env and output locations after installation and before converting important content. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/utopiabenben/text-to-podcast) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Command-line guidance and MP3 audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces MP3 output from user-selected text files; supports batch conversion, voice selection, speed control, model selection, and preview mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
