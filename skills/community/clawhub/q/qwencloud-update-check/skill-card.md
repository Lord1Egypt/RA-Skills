## Description:

[QwenCloud] Checks for qwencloud-ai updates and notifies the user when a new version is available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cuixiaoyang123](https://clawhub.ai/user/cuixiaoyang123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents using qwencloud/qwencloud-ai use this skill to check whether the installed skill pack is current and receive update or install guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can print unpinned, auto-confirming npx skills add commands that may change installed skills if run without review.

Mitigation: Treat printed update or install commands as manual actions, verify the QwenCloud/qwencloud-ai source and installer package version, and prefer a pinned installer or trusted lockfile.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cuixiaoyang123/skills/qwencloud-update-check)
- [Publisher profile](https://clawhub.ai/user/cuixiaoyang123)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [JSON status output and plain-text update or install notices]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit update guidance that includes npx skills add commands; users should review commands before running them.]

## Skill Version(s):

0.2.1 (source: version.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
