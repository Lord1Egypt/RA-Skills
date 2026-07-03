## Description: <br>
A Chinese-language skill that helps agents design AI agent testing plans across functional behavior, safety, controllability, reliability, hallucination, reasoning, and tool-call dimensions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kokxi](https://clawhub.ai/user/kokxi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and agent evaluators use this skill to plan and document testing for AI agents, chatbots, and AI assistants. It focuses on agent-specific risks such as prompt injection, tool misuse, hallucination, role-boundary failures, memory consistency, and unsafe autonomous behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested Bash or WebFetch actions could affect real tools, credentials, customer data, or production systems if followed without review. <br>
Mitigation: Review suggested actions before execution and run tests in controlled environments with scoped credentials and non-production data. <br>
Risk: Testing guidance may be incomplete or unsuitable for a specific agent, domain, or risk profile. <br>
Mitigation: Review the generated test plan against the target agent requirements, risk assessment, and safety controls before using it for release decisions. <br>


## Reference(s): <br>
- [Agent nine-dimension testing framework](references/test-framework.md) <br>
- [ClawHub skill page](https://clawhub.ai/kokxi/skills/qa-agent-testing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with structured test plans, test cases, checklists, safety audit items, reasoning validation, and tool-call test sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language guidance; may suggest Bash or WebFetch actions for test execution, which should be reviewed before use.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
