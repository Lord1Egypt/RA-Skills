## Description: <br>
Vuact is a reference skill for using a React runtime compatibility layer in Vue 3 projects, covering React-to-Vue and Vue-to-React component interop, events, reactivity, context, refs, slots, render props, and setup guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinhangfeng](https://clawhub.ai/user/yinhangfeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when integrating React components into Vue 3 applications, using Vue components from React, or planning incremental migration between React and Vue codebases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Package aliases and pnpm overrides can replace react, react-dom, or @vue/runtime-dom across a project dependency tree. <br>
Mitigation: Review dependency overrides in the target application, test affected components, and keep changes scoped to projects that intentionally use Vuact interop. <br>
Risk: The compatibility guidance notes limits around React concurrent rendering, commit-phase behavior, and synthetic events. <br>
Mitigation: Validate framework-sensitive components and event behavior before relying on Vuact for production migration or shared component libraries. <br>


## Reference(s): <br>
- [Vuact ClawHub Release](https://clawhub.ai/yinhangfeng/vuact) <br>
- [Configuration and Initialization](references/setup-config.md) <br>
- [r2v Basics](references/r2v-basic.md) <br>
- [v2r Basics](references/v2r-basic.md) <br>
- [r2v Event Callbacks](references/r2v-event.md) <br>
- [v2r Event Callbacks](references/v2r-event.md) <br>
- [r2v Render Props and Slots](references/r2v-render-props.md) <br>
- [v2r Slots](references/v2r-slots.md) <br>
- [r2v React Context](references/r2v-react-context.md) <br>
- [r2v Vue Context](references/r2v-vue-context.md) <br>
- [v2r React Context](references/v2r-react-context.md) <br>
- [v2r Vue Context](references/v2r-vue-context.md) <br>
- [r2v Component Ref](references/r2v-ref.md) <br>
- [v2r Component Ref](references/v2r-ref.md) <br>
- [r2v Vue Hooks](references/r2v-vue-hooks.md) <br>
- [r2v Hybrid Components](references/r2v-hybrid.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with TypeScript, Vue, JavaScript, JSON, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; no hidden execution or data-access behavior found in security evidence.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
