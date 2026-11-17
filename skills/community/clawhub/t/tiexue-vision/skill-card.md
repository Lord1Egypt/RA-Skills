## Description:

Recognizes text, objects, and scenes in images from Feishu chats, Feishu documents, or local files, with English-to-Chinese translation for ASCII OCR text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ldt5200-sys](https://clawhub.ai/user/ldt5200-sys)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users working with Feishu or local image folders use this skill to extract OCR text, identify objects or scenes, translate English OCR output to Chinese, and write the recognition report back to the source or to a companion text file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recognition results may be written back to Feishu chats or documents automatically.

Mitigation: Require explicit invocation and preview the generated report before modifying the original message or document.

Risk: English or ASCII OCR text may be sent to Google Translate.

Mitigation: Use a local-only mode or obtain consent before enabling external translation.

Risk: Dependency health may need review before deployment.

Mitigation: Pin, scan, and update dependencies before installing the skill in managed environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ldt5200-sys/skills/tiexue-vision)
- [Publisher profile](https://clawhub.ai/user/ldt5200-sys)
- [Skill usage documentation](artifact/SKILL.md)
- [Package manifest](artifact/package.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Markdown-style recognition report; local mode writes a .txt companion file and returns its path.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write results back to Feishu messages or documents when invoked with a Feishu source.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
