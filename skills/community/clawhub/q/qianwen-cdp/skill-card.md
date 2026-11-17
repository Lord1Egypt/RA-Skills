## Description:

Drives Qianwen Browser through native Chrome DevTools Protocol automation while preserving the real logged-in browser profile for opening pages, form filling, clicking, extracting content, and screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noaheleven](https://clawhub.ai/user/noaheleven)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation operators use this skill to automate Qianwen Browser workflows that need an existing authenticated desktop profile, such as page navigation, data capture, form entry, and screenshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automation runs against an authenticated Qianwen browser profile and can affect the user's account or data.

Mitigation: Use a dedicated automation profile when possible and require explicit user confirmation before eval, launch, relaunch, posting, form submission, deletion, or other account-impacting actions.

Risk: The shortcut patch can leave a local CDP debugging interface enabled across browser launches.

Mitigation: Avoid applying the shortcut patch unless persistent CDP access is intended, and remove or disable it when that access is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/noaheleven/skills/qianwen-cdp)
- [Packaged skill instructions](artifact/SKILL.md)
- [Qianwen CDP driver script](artifact/qw.cjs)
- [Shortcut CDP port patch script](artifact/patch_lnk.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance, shell command examples, JavaScript snippets, JSON command results, and screenshot files when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands operate through a local Qianwen Browser CDP session and may create PNG screenshot files.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
