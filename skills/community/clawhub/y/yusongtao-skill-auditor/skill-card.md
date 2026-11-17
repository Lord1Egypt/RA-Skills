## Description:

Audits OpenClaw skills for security risks such as dynamic code execution, command execution, network activity, file writes, dangerous imports, and sensitive strings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yustnust](https://clawhub.ai/user/yustnust)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill reviewers use this skill to scan OpenClaw skill directories for risky patterns and generate a human-readable security report before installation or release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner needs read access to directories selected for audit.

Mitigation: Install and run it only for directories you intentionally choose, with the narrowest practical filesystem access.

Risk: File-reading logic can escape the intended audit folder through symlinks.

Mitigation: Avoid scanning untrusted archives that contain symlinks unless they are unpacked and inspected in a sandbox.

Risk: Clean reports may be falsely reassuring because the checks are heuristic pattern scans.

Mitigation: Treat results as triage and combine them with source review or additional security tools before installation or release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yustnust/skills/yusongtao-skill-auditor)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain text security report with issue summaries by severity]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are heuristic pattern-scan results and should not be treated as proof that a skill is safe.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
