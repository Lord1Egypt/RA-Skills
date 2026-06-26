## Description: <br>
Zustand state management for React and vanilla JavaScript. Use when creating stores, using selectors, persisting state to localStorage, integrating devtools, or managing global state without Redux complexity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill for concise Zustand guidance when creating stores, selecting state efficiently, using middleware, testing store behavior, and applying TypeScript patterns in React or vanilla JavaScript projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persist middleware can write sensitive application state to browser or custom storage if developers persist full state without review. <br>
Mitigation: Use explicit persisted keys with partialize or a reviewed full-state snapshot, and exclude auth tokens, API keys, and other secrets. <br>
Risk: Devtools middleware can expose state and action details in shipped bundles when left enabled without an environment gate. <br>
Mitigation: Enable devtools only in development, or document and review the reason it remains enabled in production. <br>
Risk: Generic trigger terms such as persist or devtools may activate the skill in non-Zustand JavaScript tasks. <br>
Mitigation: Review the advice for Zustand relevance before applying code changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/anderskev/skills/zustand-state) <br>
- [Middleware](references/middleware.md) <br>
- [Patterns & Best Practices](references/patterns.md) <br>
- [TypeScript Patterns](references/typescript.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown with TypeScript code examples and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces advisory text and code snippets; it does not execute commands or access data.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
