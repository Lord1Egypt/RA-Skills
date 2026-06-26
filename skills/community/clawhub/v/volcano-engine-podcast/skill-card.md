## Description: <br>
生成火山引擎豆包语音播客（PodcastTTS）。输入主题文本，自动生成双人对话式播客音频。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cindypapa](https://clawhub.ai/user/cindypapa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate Chinese two-speaker podcast audio from topic text through Volcano Engine PodcastTTS, with options for head music, segmented streaming, retries, voice selection, and audio post-processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Podcast prompts and generated text are sent to Volcano Engine/ByteDance services for processing. <br>
Mitigation: Avoid sensitive prompts and review the provider terms, data handling expectations, and account configuration before use. <br>
Risk: Volcano credentials are required, and passing tokens on the command line can expose them through local history or process inspection. <br>
Mitigation: Use environment variables or a protected local configuration file instead of command-line tokens, and restrict credential file permissions. <br>
Risk: The helper script can stage generated audio into a QQ bot delivery path. <br>
Mitigation: Review or modify scripts/kamei_podcast.py before use, or call scripts/generate_podcast.py directly when QQ bot delivery is not intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cindypapa/volcano-engine-podcast) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; generated runs may produce MP3/WAV/PCM audio files and JSON usage metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Volcano Engine PodcastTTS credentials and sends input text to Volcano Engine/ByteDance services.] <br>

## Skill Version(s): <br>
1.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
