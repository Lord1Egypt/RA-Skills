## Description: <br>
This skill helps agents draft standardized functional, API, platform-specific, and AI agent test cases, including exception scenarios, boundary values, complex interactions, security boundaries, linkage, routing, compatibility, adaptation, and UI visual coverage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cassianran](https://clawhub.ai/user/cassianran) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and product teams use this skill to generate executable Markdown test cases for functional, API, AI agent, and platform-specific scenarios. It is intended for test case drafting and coverage review, not test planning, automation scripting, vulnerability scanning, or performance testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The broad Agent trigger may activate the skill when the user did not intend AI agent test case design. <br>
Mitigation: Use specific phrasing such as "AI agent testing" or "agent test case design" when requesting agent test cases. <br>
Risk: Generated test cases may be incomplete or may not match the product's actual requirements. <br>
Mitigation: Review generated cases against the requirement source and the applicable checklist before using them for QA execution. <br>
Risk: The skill is scoped to drafting test cases and may not safely satisfy requests for planning documents, automation scripts, vulnerability scanning, or load testing. <br>
Mitigation: Keep use to test case design and route out-of-scope testing, security, or automation work to appropriate specialist processes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cassianran/software-test-case-design) <br>
- [General Test Case Rules](references/templates/common-rules.md) <br>
- [Functional Testing](references/core-capabilities/functional-testing.md) <br>
- [API Testing](references/core-capabilities/api-testing.md) <br>
- [AI Agent Testing](references/core-capabilities/agent-testing.md) <br>
- [Test Case Output Format Specification](references/examples/format-spec.md) <br>
- [General Testing Checklist](references/checklists/common-checklist.md) <br>
- [API Testing Checklist](references/checklists/api-checklist.md) <br>
- [AI Agent Test Case Design Checklist](references/checklists/agent-checklist.md) <br>
- [PC Web Platform-Specific Testing](references/platform/pc-web.md) <br>
- [Mobile App Platform-Specific Testing](references/platform/mobile-app.md) <br>
- [Mobile Web Platform-Specific Testing](references/platform/mobile-web.md) <br>
- [Desktop Platform-Specific Testing](references/platform/desktop.md) <br>
- [Mini-Program Platform-Specific Testing](references/platform/mini-program.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance] <br>
**Output Format:** [Markdown table] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces drafted test cases and self-check guidance; does not produce test plans, automation scripts, vulnerability scans, or performance test execution.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
