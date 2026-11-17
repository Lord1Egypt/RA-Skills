## Description:

Vuact is a best-practices and integration guide for using Vuact as a React and Vue interoperability layer covering component conversion, events, reactivity, context, refs, slots, render props, and project configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinhangfeng](https://clawhub.ai/user/yinhangfeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when mixing React and Vue in the same application, migrating components across frameworks, or configuring Vuact-based component interoperability. It helps select and apply the relevant r2v and v2r patterns, project aliases, package overrides, and initialization steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recommended package aliases and pnpm overrides can change how React, React DOM, Vue, or Vue runtime dependencies resolve in an application.

Mitigation: Review the aliases and overrides in a test branch, then verify dependency resolution, bundling, and runtime behavior before applying them to production projects.

Risk: Vuact does not fully replicate React concurrent rendering, commit-phase timing, SyntheticEvent behavior, or some native DOM handling.

Mitigation: Validate affected components with integration tests, especially components that depend on React scheduling, lifecycle timing, input events, or form behavior.

## Reference(s):

- [Vuact ClawHub Skill Page](https://clawhub.ai/yinhangfeng/skills/vuact)
- [Vuact Configuration and Initialization](artifact/references/setup-config.md)
- [r2v Basics](artifact/references/r2v-basic.md)
- [v2r Basics](artifact/references/v2r-basic.md)
- [r2v Render Props and Slots](artifact/references/r2v-render-props.md)
- [v2r Slots](artifact/references/v2r-slots.md)
- [r2v Event Callbacks](artifact/references/r2v-event.md)
- [v2r Event Callbacks](artifact/references/v2r-event.md)
- [r2v React Context](artifact/references/r2v-react-context.md)
- [v2r React Context](artifact/references/v2r-react-context.md)
- [r2v Vue Context](artifact/references/r2v-vue-context.md)
- [v2r Vue Context](artifact/references/v2r-vue-context.md)
- [r2v Component Ref](artifact/references/r2v-ref.md)
- [v2r Component Ref](artifact/references/v2r-ref.md)
- [r2v Vue Hooks](artifact/references/r2v-vue-hooks.md)
- [r2v Hybrid Components](artifact/references/r2v-hybrid.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline TypeScript, TSX, Vue, JavaScript, JSON, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces implementation guidance and examples for React and Vue interoperability; no hidden execution or data-access behavior was found in security evidence.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
