## Description: <br>
Security-camera video annotation skill that extracts representative frames, guides visual analysis, validates structured annotations, and builds VL fine-tuning dataset.jsonl files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aowind](https://clawhub.ai/user/aowind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and dataset annotators use this skill to turn authorized security-camera videos into structured labels and VL model training records. It supports frame extraction, per-video JSON annotation, label and risk-level validation, and dataset.jsonl generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security-camera footage and extracted frames may contain sensitive personal data. <br>
Mitigation: Process only footage you are authorized to use, and review or redact frames, annotations, and dataset.jsonl before training, sharing, or long-term storage. <br>
Risk: Frame extraction and dataset generation write output files and may overwrite previous results. <br>
Mitigation: Run the skill with a dedicated video folder and dedicated output directory, and review target paths before executing the scripts. <br>
Risk: Frame extraction depends on local ffmpeg and ffprobe binaries. <br>
Mitigation: Use trusted ffmpeg and ffprobe binaries in a controlled environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aowind/sjht-cam-anno) <br>
- [System prompt template](references/system-prompt.md) <br>
- [Labels and risk reference](references/labels-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Files] <br>
**Output Format:** [Markdown guidance with shell commands and JSON examples; scripts produce manifest.json and dataset.jsonl files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated records include a shared system prompt, assistant annotation JSON, and video path references.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
