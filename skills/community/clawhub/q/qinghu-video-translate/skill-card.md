## Description:

Helps agents translate videos with subtitle, AI voiceover, and lip-sync options using the Qinghu video-translation service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and marketing teams use this skill to guide video localization from Chinese or English into supported languages, with a choice of translated subtitles, dubbing, or lip sync.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing qhkit or Node and changing the shell environment affects the user's system.

Mitigation: Confirm with the user before global installs, Node bootstrap, or PATH and shell-profile changes.

Risk: Processing requires an API token and may upload supplied video files to the qhkit service.

Mitigation: Use a user-provided token and obtain consent before sending video files for processing.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-video-translate)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with commands, task status, and links to translated videos]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports task IDs, completion links, and charged credits when available.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
