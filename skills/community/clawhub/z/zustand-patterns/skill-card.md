## Description: <br>
Provides practical Zustand state-management patterns for React projects, including store design, reusable slices, persistence, recoverable tasks, Electron IPC integration, testing, and common pitfalls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bingfoon](https://clawhub.ai/user/bingfoon) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to design and review Zustand stores in React applications, especially when splitting state by module, persisting selected fields, recovering remote tasks, wiring Electron IPC events, and testing store actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persisted Zustand state could accidentally retain secrets, raw logs, or runtime-only data if examples are applied without filtering fields. <br>
Mitigation: Use partial persistence for user configuration and preferences only; avoid persisting secrets, raw logs, in-flight progress, and transient errors. <br>
Risk: Recoverable polling flows can continue after restart without clear user awareness or control. <br>
Mitigation: Keep recovered polling visible to users and provide a cancellable recovery flow. <br>
Risk: Electron IPC examples can expose unsafe channels if the main process does not validate requests. <br>
Mitigation: Validate IPC channel names and payloads in the Electron main process before acting on renderer requests. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown with TypeScript examples and implementation checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no executable install behavior was identified in the server security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
