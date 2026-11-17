## Description:

Xiabb is a free macOS voice-to-text tool for Vibe Coding that uses Google Gemini to transcribe speech, support mixed Chinese and English input, and produce translations, optimized prompts, or emails through Smart Modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dyz2102](https://clawhub.ai/user/dyz2102)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Xiabb to dictate text into macOS applications with a Globe-key workflow, especially when writing mixed Chinese and English development prompts. Users can also invoke Smart Modes to translate dictated speech, turn spoken ideas into AI prompts, or draft emails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install flow may weaken macOS protections.

Mitigation: Review before installing and prefer a signed, notarized release with published checksums over source installation.

Risk: Dictated audio and generated text may be sent to Google Gemini.

Mitigation: Avoid dictating secrets or regulated data, and use the tool only where sending audio and text to Gemini is acceptable.

Risk: The Gemini API key can be exposed or misused if handled casually.

Mitigation: Restrict the API key to the minimum needed scope and rotate it if it may have been exposed.

Risk: Transcripts may be stored in local logs.

Mitigation: Check and clear ~/Library/Logs/XiaBB.log when dictated content should not remain on disk.

## Reference(s):

- [Xiabb homepage](https://xiabb.lol)
- [ClawHub skill page](https://clawhub.ai/dyz2102/skills/xiabb)
- [Google AI Gemini documentation](https://ai.google.dev/)
- [Google AI Studio API keys](https://aistudio.google.com/apikey)
- [Swift](https://swift.org)
- [macOS](https://www.apple.com/macos/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Text and Markdown with shell commands, code snippets, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces dictated text, translations, prompt drafts, email drafts, and setup guidance for macOS users.]

## Skill Version(s):

1.3.2 (source: ClawHub release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
