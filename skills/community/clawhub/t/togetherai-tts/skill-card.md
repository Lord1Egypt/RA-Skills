## Description: <br>
Convert text to speech using the TogetherAI API with the MiniMax speech-2.6-turbo model and save the generated audio as an MP3 file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marcus20232023](https://clawhub.ai/user/marcus20232023) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to turn supplied text into a speech audio file through TogetherAI. It is suited for workflows that need generated spoken output saved to a local file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input text is sent to TogetherAI for speech synthesis. <br>
Mitigation: Use the skill only with text that may be shared with TogetherAI under that service's terms, and use a scoped or low-risk API key when possible. <br>
Risk: The output file path is supplied by the caller and may overwrite an existing local file. <br>
Mitigation: Choose an output filename in a safe working directory and avoid paths that point to important files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marcus20232023/togetherai-tts) <br>
- [TogetherAI speech API endpoint](https://api.together.ai/v1/audio/speech) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [MP3 audio file with console status or error text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a TogetherAI API key and writes the generated audio to the requested output path.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
