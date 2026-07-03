## Description: <br>
Super Auto Talk Tts converts agent messages to spoken audio using edge-tts, with configurable voice, rate, pitch, volume, and manual auto-speak commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subaru0573](https://clawhub.ai/user/subaru0573) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to have generated responses spoken aloud for accessibility or hands-free workflows. It is intended for environments where always-on text-to-speech behavior is explicitly desired and acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Always-on speech can expose generated responses through audible playback or an external TTS service. <br>
Mitigation: Use only with explicit opt-in, avoid speaking sensitive content, and do not add persistent always-on agent rules unless that behavior is required. <br>
Risk: The artifact describes automatic package installation and depends on node-edge-tts without a pinned exact version. <br>
Mitigation: Review dependencies before installation, prefer pinned dependencies, and install only from trusted package sources. <br>
Risk: The documented auto-speak executable is not included among the provided artifact files. <br>
Mitigation: Verify the executable exists and inspect its behavior before enabling or testing the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/subaru0573/skills/super-auto-talk-tts) <br>


## Skill Output: <br>
**Output Type(s):** [Audio, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Spoken audio with Markdown guidance and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Asynchronous text-to-speech playback with configurable voice, rate, pitch, volume, and summary length.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
