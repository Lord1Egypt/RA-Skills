## Description:

Web Profiler provides command-line helpers for logging, reviewing, searching, and exporting user-supplied web profiling notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can use this skill to record command-line notes about request profiling, performance investigations, comparisons, status checks, and exports for later review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be mistaken for a real web profiling or instrumentation tool even though the shipped script mostly records user-supplied text.

Mitigation: Treat entries as local notes and history, not as measurements from live requests, traces, or server instrumentation.

Risk: Sensitive debugging data can be retained in plaintext under ~/.local/share/web-profiler/.

Mitigation: Do not enter tokens, credentials, private URLs, authorization headers, database connection strings, or sensitive stack traces unless local plaintext retention is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/web-profiler)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local files under ~/.local/share/web-profiler/ when describing logs or exports.]

## Skill Version(s):

1.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
