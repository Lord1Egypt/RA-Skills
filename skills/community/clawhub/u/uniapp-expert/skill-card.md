## Description:

A uni-app cross-platform development skill covering Vue 2 and Vue 3 development, Vue 2 to Vue 3 migration, and WeChat Mini Program automated testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[include5943](https://clawhub.ai/user/include5943)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to build uni-app applications, migrate Vue 2 uni-app code to Vue 3, and prepare local WeChat Mini Program automation tests. It provides implementation guidance, migration checklists, code examples, and test automation setup steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included automation workflow runs local Python and Node scripts against WeChat DevTools.

Mitigation: Use the skill in a disposable or low-privilege development environment and review generated scripts before execution.

Risk: Unsafe code-generation paths in the automation scripts could run unintended local JavaScript.

Mitigation: Do not pass untrusted endpoint, selector, or test-step values into automation runs.

Risk: Automation testing can expose local credentials, app data, or production-like Mini Program traffic.

Mitigation: Avoid real credentials and production data during testing; pin npm dependencies used by the automation stack.

Risk: Mini Program domain validation may be disabled during local testing.

Mitigation: Re-enable domain validation after testing and before using the project in normal development or release workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/include5943/skills/uniapp-expert)
- [uni-app official documentation](https://uniapp.dcloud.io/)
- [Vue official documentation](https://vuejs.org/)
- [WeChat DevTools CLI documentation](https://developers.weixin.qq.com/miniprogram/dev/devtools/cli.html)
- [WeChat Mini Program automation API reference](skills/weapp-automated-testing/references/api_reference.md)
- [Vue Expert Composition API reference](skills/vue-expert/references/composition-api.md)
- [Vue Expert state management reference](skills/vue-expert/references/state-management.md)
- [Vue reactivity reference](skills/vue/reactivity.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, command examples, and configuration checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local test scripts and screenshots when used with WeChat DevTools automation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
