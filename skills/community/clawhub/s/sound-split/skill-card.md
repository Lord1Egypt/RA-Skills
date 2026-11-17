## Description:

智能音频分离工具 helps an agent guide users through running a local audio and video stem-separation tool that outputs vocals, accompaniment, drums, bass, piano, and other tracks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nabian1990amber-cmd](https://clawhub.ai/user/nabian1990amber-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users, musicians, creators, and developers use this skill to separate uploaded audio or video into stems for covers, remixing, mixing practice, podcast cleanup, video music replacement, and music teaching material. Developers can also use the documented FastAPI endpoints to automate separation, status polling, downloads, trimming, history, and cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The unauthenticated localhost API can expose, alter, or delete task files too broadly.

Mitigation: Run it only on localhost, stop it when not in use, and add authentication, stricter CORS, and path validation before broader or sensitive use.

Risk: Sensitive audio could be exposed through the local service while the API access controls remain weak.

Mitigation: Avoid processing sensitive audio until the security guidance is addressed and browser exposure from untrusted sites is controlled.

Risk: Dependency and model installation are performed in the local Python environment.

Mitigation: Use a virtual environment with pinned dependencies before installing or running the service.

Risk: The stated cleanup behavior may not remove files automatically as expected.

Mitigation: Verify or implement cleanup behavior before relying on time-based removal of uploaded, separated, or trimmed audio files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nabian1990amber-cmd/skills/sound-split)
- [Demucs](https://github.com/facebookresearch/demucs)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with command snippets, API examples, and bundled application source files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides local FastAPI operation and file-based audio output; separated audio files are produced by the bundled application, not directly by the agent response.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
