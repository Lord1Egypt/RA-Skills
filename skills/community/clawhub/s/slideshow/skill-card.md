## Description:

Build a HyperFrames slideshow to present live - slides, fragment reveals, branching hotspots and presenter mode with speaker notes, served by `hyperframes present` - or turn an existing page into one. Use when the person wants a deck or presentation rather than a rendered video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heygen-com](https://clawhub.ai/user/heygen-com)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to create live, navigable slide decks with fragments, branching hotspots, and presenter notes, or to adapt an existing page into a presentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks to send a usage beacon that may be account-linked.

Mitigation: Review the telemetry opt-out and disable the beacon if you do not want usage data sent.

Risk: Package commands may use unpinned dependencies.

Mitigation: Verify the package source and pin the version or use a trusted local installation before running commands.

Risk: The reference includes runtime code loaded from a public CDN.

Mitigation: Review and pin the dependency, or use a trusted local copy, before enabling the CDN-based example.

Risk: The security review was incomplete, including limited inspection of a referenced file.

Mitigation: Review the standalone harness reference before applying its patterns in a project.

## Reference(s):

- [Slideshow on ClawHub](https://clawhub.ai/heygen-com/skills/slideshow)
- [Standalone HyperFrames Slideshow Harness](references/standalone-harness.md)

## Skill Output:

**Output Type(s):** [Files, Code, Configuration instructions, Shell commands, Guidance]

**Output Format:** [HTML, JSON, JavaScript, and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include interactive slideshow project files and presenter notes.]

## Skill Version(s):

1.0.21 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
