## Description:

uniapp-test helps agents analyze uni-app and uni-app x pages, create or update adjacent automated test files, run platform-specific test commands, and iterate on failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dengzy321](https://clawhub.ai/user/dengzy321)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to maintain uni-app automated tests for .vue and .uvue pages, including generating page-adjacent *.test.js files and repairing failing test cases. It is most useful for Web, Android, iOS, Harmony, and WeChat Mini Program test workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may edit page-adjacent test files and run npm test commands, including platform or device tests.

Mitigation: Use it for explicit uni-app testing tasks, confirm required devices or simulators are available before running platform tests, and review file changes before keeping them.

Risk: The security summary notes overbroad activation language.

Mitigation: Invoke the skill only for uni-app or uni-app x automated testing work where page analysis, test generation, test execution, or test repair is intended.

## Reference(s):

- [uni-app automated testing API](https://uniapp.dcloud.net.cn/worktile/auto/api.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with JavaScript test snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update page-adjacent *.test.js files and propose targeted reruns with --testcaseFile.]

## Skill Version(s):

1.0.0 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
