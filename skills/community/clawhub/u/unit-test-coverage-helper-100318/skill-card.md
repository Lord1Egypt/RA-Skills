## Description:

Helps developers and QA teams plan, implement, and verify useful unit tests and coverage improvements for existing codebases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, software maintainers, QA engineers, open-source contributors, and product teams use this skill to turn testing and regression concerns into concrete unit-test plans, implementation changes, coverage checks, and validation notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Implicit invocation may activate the skill for broad testing or quality-related requests.

Mitigation: Confirm the user's testing goal and repository constraints before proposing or changing tests.

Risk: Generated test guidance or code changes may assert incorrect behavior if the existing codebase is not inspected carefully.

Mitigation: Validate proposed tests with local test and coverage commands and call out assumptions or remaining gaps.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/unit-test-coverage-helper-100318)
- [autonomous-run 2026-07-04](https://github.com/shanevcantwell/llauncher/issues/255)
- [flaky: internal/e2e/internal/fakerelay 503 WebSocket handshake under concurrent -race load](https://github.com/pyrycode/pyrycode/issues/789)
- [test: missing E2E paths - wall-clock watchdog timeout, invoker-driven dead-host fail-fast, [AtlasScenario] on a non-AtlasScenarioBase class](https://github.com/Pixnop/Atlas/issues/11)
- [Writing Great Unit Tests: Best and Worst Practices](https://segmentfault.com/a/1190000009709754)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text with optional code blocks and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, checklists, test plans, coverage commands, and validation notes tailored to the user's codebase.]

## Skill Version(s):

0.20260729.110214 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
