## Description: <br>
Converts web pages or provided text into TTS audio files and emits channel-specific markers for Feishu, WeChat, Telegram, and Discord. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phentse](https://clawhub.ai/user/phentse) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert a URL or text snippet into voice-ready audio for chat channels. It is most useful when an assistant needs to read an article, summary, notice, or user-provided text aloud and return the generated voice file through the user's source channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private text, internal URLs, customer data, or confidential documents may be sent to external TTS or chat channels. <br>
Mitigation: Require an explicit read-aloud request, disclose that content may leave the local environment, and avoid processing sensitive input. <br>
Risk: Bare URLs can be fetched automatically and converted without enough user confirmation. <br>
Mitigation: Ask for confirmation before fetching URLs, especially for private or unfamiliar links. <br>
Risk: Generated audio files are written to local storage. <br>
Mitigation: Write outputs to a controlled directory and clean up generated files after delivery when retention is not needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/phentse/web-tts-speaker) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>
- [OpenClaw Weixin voice issue](https://github.com/openclaw/openclaw/issues/61031) <br>
- [FFmpeg builds](https://www.gyan.dev/ffmpeg/builds/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Text, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands; CLI output is text marker blocks that point to local MP3 or Opus audio files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The default auto mode creates channel-specific audio formats and prints markers for the agent to select the file for the inbound channel.] <br>

## Skill Version(s): <br>
3.2.1 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
