## Description:

Always active in every session. Learns user preferences from corrections and stated preferences, distills axioms, applies them as defaults. Makes every other skill better over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckpxgfnksd-max](https://clawhub.ai/user/ckpxgfnksd-max)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to maintain lightweight preference memory across sessions, recording explicit corrections, stated preferences, and retractions, then distilling stable patterns into reusable defaults.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can silently persist preference observations and influence future conversations across sessions.

Mitigation: Install only when persistent preference memory is desired, periodically review the memory/context-infra files, and avoid sharing sensitive preferences that should not be retained.

Risk: The security review notes reliance on natural-language retraction rather than a dedicated disable or deletion workflow.

Mitigation: Use explicit retraction requests for preferences that should no longer apply and manually inspect or remove stored memory files when stronger deletion assurance is needed.

## Reference(s):

- [Profile Format](profile-format.md)
- [Autoresearch Method](https://github.com/karpathy/autoresearch)
- [Context Infrastructure](https://yage.ai/context-infrastructure.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown profile entries and plain-text observation log entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local memory files for observations and distilled preference axioms.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
