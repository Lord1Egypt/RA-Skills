## Description:

SkillScan scans skill packages for security risk and directs agents to gate installation, loading, evaluation, and first-run reviews based on scanner verdicts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tokauthai](https://clawhub.ai/user/tokauthai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use SkillScan to assess skill packages before installation or use, scan existing local skill directories, and decide whether to proceed, warn, or block based on the reported verdict.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud scanning may upload complete skill directories.

Mitigation: Use only with skills whose contents may be shared with the SkillScan service, or prefer a release that provides explicit upload consent and a local-only mode.

Risk: Persistent device metadata may be sent with scan requests.

Mitigation: Review and approve device metadata collection before deployment; prefer a version that avoids MAC collection and limits stable identifiers.

Risk: Broad local skill path scanning may include more directories than intended.

Mitigation: Run targeted scans against specific skill paths where possible and review configured scan locations before using full-scan commands.

Risk: Runtime auto-update can replace the scanner code from a remote update source.

Mitigation: Disable or control automatic update sources where policy requires fixed code, and prefer signed or user-approved update workflows.

## Reference(s):

- [ClawHub SkillScan page](https://clawhub.ai/tokauthai/skills/skillscan)
- [SkillScan service homepage](https://skillscan.tokauth.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and scanner verdicts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses scanner exit codes to indicate proceed, warn, block, or scan failure outcomes.]

## Skill Version(s):

1.1.6 (source: server release evidence, SKILL.md frontmatter, artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
