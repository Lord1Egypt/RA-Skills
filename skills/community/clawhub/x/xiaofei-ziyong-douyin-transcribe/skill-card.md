## Description:

Downloads a Douyin video from a provided link, extracts its audio, transcribes speech locally, and can optionally prepare Feishu upload steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mengzi53](https://clawhub.ai/user/mengzi53)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and content operations teams use this skill to turn Douyin video links into local text transcripts. It supports a local transcription workflow and optional Feishu organization steps for generated outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied Douyin links and file paths are exposed to unsafe shell execution.

Mitigation: Run only in a restricted environment with non-sensitive files, avoid crafted or untrusted Douyin links, do not use elevated privileges, and remediate shell command construction before normal use.

Risk: The workflow sends links and downloaded content through third-party services.

Mitigation: Use non-sensitive inputs and credentials, and review data handling for Douyin, Hellotik, and Feishu before deployment.

Risk: The implementation depends on loading a runtime dependency from /tmp.

Mitigation: Audit and replace the /tmp dependency load with a trusted, pinned installation path before normal use.

Risk: Feishu upload behavior is not suitable to rely on without review.

Mitigation: Audit and fix the Feishu upload implementation and credential handling before enabling upload workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mengzi53/skills/xiaofei-ziyong-douyin-transcribe)
- [Publisher profile](https://clawhub.ai/user/mengzi53)
- [Hellotik web parser used by the skill](https://www.hellotik.app/zh)
- [Feishu Open APIs endpoint referenced by the skill](https://open.feishu.cn/open-apis)

## Skill Output:

**Output Type(s):** [text, files, shell commands, configuration]

**Output Format:** [Plain text transcript printed to the terminal and saved as transcript.txt, with downloaded video and audio files retained unless cleanup is requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional Feishu upload workflow; local media cleanup is controlled by the cleanup option.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
