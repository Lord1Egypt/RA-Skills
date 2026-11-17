## Description:

Generates high-fidelity 1080p videos with synced audio using Google Veo 3.1.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kghamilton89](https://clawhub.ai/user/kghamilton89)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to generate short cinematic MP4 video clips from text prompts through Google Veo 3.1.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video prompts are sent to Google GenAI.

Mitigation: Use only with prompts that are appropriate to share with Google GenAI and avoid including sensitive information.

Risk: The skill depends on npm packages and the security guidance notes vulnerable transitive packages.

Mitigation: Review and update npm dependencies before production use.

Risk: Passing a user prompt through a shell command string can enable shell injection.

Mitigation: Invoke generate.js with an argv array or execFile-style call and pass the prompt as a separate --prompt argument.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kghamilton89/skills/veo-video-generator)
- [ClawHub publisher profile](https://clawhub.ai/user/kghamilton89)

## Skill Output:

**Output Type(s):** [text, shell commands, code, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell command examples and a generated MP4 file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a local 1080p 9:16 MP4 file and reports the filename.]

## Skill Version(s):

1.2.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
