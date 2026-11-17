## Description:

Security-first skill vetting for AI agents. Use before installing any skill from ClawHub, GitHub, or other sources. Checks for red flags, permission scope, and suspicious patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ray-778](https://clawhub.ai/user/ray-778)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agent users use Vetter to review third-party skills before installation and surface permission, script, URL, and environment concerns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security evidence reports suspicious behavior: the skill claims to vet third-party skills, but its runnable code only records local machine and user details into a home-directory file.

Mitigation: Review before installation; prefer a version that removes or clearly explains the marker file and minimizes collected local data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ray-778/skills/vetter)
- [ClawHub publisher profile](https://clawhub.ai/user/ray-778)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and plain text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included script writes ~/vetter_skill_marker.json with host, user, platform, and skill details.]

## Skill Version(s):

1.0.7 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
