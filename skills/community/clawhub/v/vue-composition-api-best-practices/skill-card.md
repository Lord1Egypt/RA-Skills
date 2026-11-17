## Description:

Guides agents on Vue 3 Composition API and <script setup> best practices, including code organization, useXxx patterns, composable design, Store integration, reactivity optimization, and feature extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acanzaima](https://clawhub.ai/user/acanzaima)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering agents use this skill to review, refactor, and generate Vue 3 Composition API guidance and code patterns for maintainable TypeScript, Pinia, and <script setup> projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that the skill presents an unsafe JSONP search-suggestion pattern as production-grade guidance.

Mitigation: Review generated Vue code carefully and replace JSONP search-suggestion examples with data-only fetch logic or strict trusted-origin controls before adopting them.

## Reference(s):

- [Skill overview](SKILL.md)
- [SFC code organization order](reference/sfc-code-organization.md)
- [UseXxx function pattern](reference/use-function-pattern.md)
- [Feature extraction to composables](reference/feature-extraction.md)
- [Handling cross-feature dependencies](reference/cross-feature-dependencies.md)
- [script setup best practices](reference/script-setup-best-practices.md)
- [Store Without pattern](reference/store-without-pattern.md)
- [Composable design patterns](reference/composable-design-patterns.md)
- [Reactivity and performance](reference/reactivity-performance.md)
- [Vue.js script setup](https://vuejs.org/api/sfc-script-setup.html)
- [Vue.js TypeScript with Composition API](https://vuejs.org/guide/typescript/composition-api.html)
- [Vue.js Composables](https://vuejs.org/guide/reusability/composables.html)
- [VueUse utilities](https://vueuse.org/)
- [mitt event emitter](https://github.com/developit/mitt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with Vue, TypeScript, and shell-style examples where relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language guidance focused on Vue 3.3+ with some patterns requiring Vue 3.4+ or 3.5+.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
