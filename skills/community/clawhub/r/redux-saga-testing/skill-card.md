## Description: <br>
Write tests for Redux Sagas using redux-saga-test-plan, runSaga, and manual generator testing, covering expectSaga, testSaga, providers, partial matchers, reducer integration, error simulation, and cancellation testing with Jest and Vitest. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anivar](https://clawhub.ai/user/anivar) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering agents use this skill to write maintainable Redux Saga tests, choose between expectSaga, testSaga, runSaga, and manual generator testing, and avoid brittle or incomplete saga test patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested dependency or skill installation commands may change a development environment. <br>
Mitigation: Review install commands and dependency changes before running them, as recommended by the security guidance. <br>
Risk: Saga tests can become brittle or misleading when they assert implementation order, omit providers, or skip async/error/cancellation paths. <br>
Mitigation: Prefer expectSaga for behavior-focused tests, provide mocks for external calls, await saga execution, and cover error and cancellation paths using the documented reference patterns. <br>


## Reference(s): <br>
- [Redux Saga Testing API Reference](references/api-reference.md) <br>
- [Redux Saga Testing Anti-Patterns](references/anti-patterns.md) <br>
- [ClawHub Redux Saga Testing Skill Page](https://clawhub.ai/anivar/redux-saga-testing) <br>
- [Redux Saga Testing Source URL](https://github.com/anivar/redux-saga-testing) <br>
- [Publisher Website](https://anivar.net) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JavaScript and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides testing patterns and examples for Redux Saga projects using redux-saga-test-plan, Jest, or Vitest.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
