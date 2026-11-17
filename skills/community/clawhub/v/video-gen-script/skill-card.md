## Description:

How to generate video scripts for the Video Generator from user prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itspremkumar](https://clawhub.ai/user/itspremkumar)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn storytelling prompts into structured video-generator script JSON with narration text, visual cue tags, orientation, voice, and optional display settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated script JSON may use unsupported voice IDs, malformed fields, or visual cue syntax that downstream video tooling cannot process.

Mitigation: Validate generated entries against the documented keys, accepted orientation values, supported voice IDs, and `[Visual: ...]` tag format before use.

Risk: Voiceover text may accidentally include production notes or scene labels that would be read aloud.

Mitigation: Review the final `script` value and remove non-narration instructions such as scene labels before passing it to text-to-speech.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/itspremkumar/skills/video-gen-script)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces video-generator script entries using supported voice IDs, orientation settings, optional caption and fallback-video keys, and inline visual cue tags.]

## Skill Version(s):

5.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
