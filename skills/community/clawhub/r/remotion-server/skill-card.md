## Description:

Headless video rendering with Remotion v5 on Linux servers, with templates for chat demos, promos, and title cards using Chrome Headless Shell.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mvanhorn](https://clawhub.ai/user/mvanhorn)

### License/Terms of Use:

MIT

## Use Case:

Developers and technical creators use this skill to scaffold Remotion video projects, install headless Linux rendering dependencies, and render videos such as chat demos, promo clips, title cards, MP4s, WebM files, GIFs, or PNG sequences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can install Linux system browser libraries and project creation can install npm packages.

Mitigation: Run setup and project creation in a non-privileged or disposable development environment before adopting it in a persistent workspace.

Risk: Generated projects and rendered videos may include unintended content or dependency changes.

Mitigation: Review generated project files and rendered output before publishing, and pin dependency versions or use a lockfile for reproducible builds.

## Reference(s):

- [Remotion Documentation](https://remotion.dev)
- [Remotion Linux Dependencies](https://www.remotion.dev/docs/miscellaneous/linux-dependencies)
- [ClawHub Skill Page](https://clawhub.ai/mvanhorn/skills/remotion-server)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and generated Remotion project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create TypeScript, React, Tailwind, JSON, and Remotion configuration files for a local video project.]

## Skill Version(s):

1.2.1 (source: server release metadata; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
