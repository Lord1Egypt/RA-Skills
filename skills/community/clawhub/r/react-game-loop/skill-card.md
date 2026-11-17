## Description:

Create custom React hooks in TypeScript for game loops and animations using requestAnimationFrame, with stale-closure safety, unmount cleanup, error resilience, and configurable delta-time handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ravenquasar](https://clawhub.ai/user/ravenquasar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add a browser-only React game loop hook and example component to animation or game projects that need requestAnimationFrame timing, start/stop controls, and delta-time clamping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repeated synchronous start calls can leave duplicate animation-frame loops running.

Mitigation: Review or patch the start/stop cleanup logic before production use.

## Reference(s):

- [useGameLoop hook](assets/hooks/useGameLoop.ts)
- [GameTimer example](assets/examples/GameTimer.tsx)

## Skill Output:

**Output Type(s):** [code, markdown, shell commands, guidance]

**Output Format:** [Markdown with TypeScript and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces browser-focused React hook integration guidance; no backend services or credentials are required.]

## Skill Version(s):

1.0.0 (source: server release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
