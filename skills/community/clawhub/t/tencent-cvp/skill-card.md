## Description:

All-in-one Android phone automation via ADB: screen analysis, touch/input, foreground app detection, app install. Use for any task that involves operating the Android device.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cobeizailin](https://clawhub.ai/user/cobeizailin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation operators use this skill to observe and control a Tencent Cloud Virtual Phone through ADB, including UI inspection, touch and text input, foreground app detection, launching apps, and guided app installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad ADB control can operate the device, install apps, and enter text on behalf of the agent.

Mitigation: Use only on intended Tencent Cloud Virtual Phone sessions, review proposed commands before execution, and require explicit confirmation before sensitive account or app-install actions.

Risk: APK-search fallback can lead to untrusted downloads.

Mitigation: Prefer trusted app stores or verified first-party sources and avoid arbitrary APK search results.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ADB on linux or darwin systems and an accessible Android or Tencent Cloud Virtual Phone target.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
