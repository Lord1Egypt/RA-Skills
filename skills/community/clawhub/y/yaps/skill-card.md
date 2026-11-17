## Description:

Yaps helps an agent handle speech, media, translation, and memory requests through the locally installed Yaps app.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaps](https://clawhub.ai/user/yaps)

### License/Terms of Use:

MIT

## Use Case:

People using Yaps on their own computer can ask an agent to create or process audio, video, images, captions, and translations, or work with selected memory and vault content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private media, vault content, or history may enter the agent conversation during a requested task.

Mitigation: Use only user-selected inputs, limit history access to explicit requests, and avoid sharing retrieved content with other services without permission.

Risk: Generated files may replace existing work or an interrupted media job may be repeated.

Mitigation: Save under new filenames, verify outputs, and check running jobs or saved projects before retrying.

Risk: Account access is required for some capabilities.

Mitigation: Have users sign in through Yaps; never request credentials or payment details in chat.

## Reference(s):

- [Yaps runtime guide](references/runtime.md)
- [Yaps download](https://yaps.ai/download)
- [Yaps skill on ClawHub](https://clawhub.ai/yaps/skills/yaps)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Text or Markdown response with paths to requested local artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requested outputs may include audio, video, images, subtitles, or translated text; availability depends on the installed app and account access.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
