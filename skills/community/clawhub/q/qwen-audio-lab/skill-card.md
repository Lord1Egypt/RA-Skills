## Description:

Hybrid text-to-speech, reusable voice cloning, and narrated audio generation for macOS plus Aliyun Qwen.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aliyx](https://clawhub.ai/user/aliyx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and agents use this skill to convert text, text files, or PowerPoint speaker notes into narrated audio, using local macOS speech or Aliyun Qwen text-to-speech. It also supports creating and reusing custom voices from consented reference recordings or text voice prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Qwen-backed synthesis and voice features may transmit scripts, slide notes, and voice samples to Aliyun Qwen.

Mitigation: Review inputs for private or sensitive content before use, keep API credentials scoped appropriately, and use the local macOS backend when cloud processing is not acceptable.

Risk: Voice cloning can create reusable custom voices from uploaded recordings.

Mitigation: Use only recordings that the user owns or has consent to clone, and ask for confirmation when third-party voice consent is unclear.

Risk: The security scan reports an output-path weakness that could overwrite user-writable files.

Mitigation: Avoid absolute paths and parent-directory components in --output values until output path validation is fixed.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash commands; commands may produce JSON status output and audio files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Qwen-backed commands require DASHSCOPE_API_KEY and may send text, slide notes, and voice samples to Aliyun Qwen.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
