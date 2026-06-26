## Description: <br>
Create custom React hooks in TypeScript for game loops and animations with requestAnimationFrame integration, delta-time handling, stale-closure safety, unmount cleanup, and configurable parameters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ravenquasar](https://clawhub.ai/user/ravenquasar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to add a browser-side React game loop hook with start and stop controls, elapsed-time tracking, delta-time clamping, and cleanup behavior. It is suited for animation and game UI components that need requestAnimationFrame-driven updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The hook depends on requestAnimationFrame and is not suitable for Node.js or server-side rendering execution. <br>
Mitigation: Use it only in client-side React components and guard usage in applications that also render on the server. <br>
Risk: Slow or error-prone frame callbacks can affect animation behavior and user experience. <br>
Mitigation: Review and test onFrame callbacks, keep frame work lightweight, and validate start, stop, and cleanup behavior before deployment. <br>


## Reference(s): <br>
- [React Game Loop Hooks on ClawHub](https://clawhub.ai/ravenquasar/react-game-loop) <br>
- [useGameLoop hook source](assets/hooks/useGameLoop.ts) <br>
- [GameTimer usage example](assets/examples/GameTimer.tsx) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with TypeScript and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces client-side React hook code and examples for environments where requestAnimationFrame is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
