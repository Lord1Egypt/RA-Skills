## Description:

Skill Safe Install helps agents install ClawHub skills through a three-step review that combines Skill-Vetter code review, ClawHub rating checks, and ThreatBook sandbox scanning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chj0w0](https://clawhub.ai/user/chj0w0)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to preflight ClawHub skill installations, review code, rating, and sandbox signals, and decide whether to install, confirm, or block a skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer downloads skills, executes local ClawHub, curl, tar, and zip commands, and uploads skill archives to ThreatBook.

Mitigation: Use it only when those actions are acceptable, review the skill and command behavior first, and avoid sensitive archives or credentials.

Risk: Bypass flags such as --auto, --yes, --force, --no-vetter, and --no-scan can reduce or skip review gates for untrusted skills.

Mitigation: Do not use bypass flags for untrusted skills; require explicit review when checks are suspicious, fail, or are skipped.

Risk: The security evidence flags command argument handling, API-key handling, and scan coverage as needing fixes before CI or sensitive use.

Mitigation: Keep the skill out of CI and sensitive credential contexts until those areas are reviewed and corrected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chj0w0/skills/skill-safe-install)
- [ThreatBook sandbox](https://s.threatbook.com)
- [ThreatBook API endpoint](https://api.threatbook.cn/v3)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, curl, tar, zip, and THREATBOOK_API_KEY; may upload skill archives to ThreatBook for sandbox analysis.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
