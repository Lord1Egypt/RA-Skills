## Description:

Agentforce agent testing with dual-track workflow and 100-point scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dsouza-anush](https://clawhub.ai/user/dsouza-anush)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quality engineers use this skill to plan and run Salesforce Agentforce tests, generate YAML test specs, analyze topic and action coverage, and guide a structured test-fix loop after an agent is published and activated.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Salesforce credential tooling can persist and handle secrets in ways that may expose them.

Mitigation: Use a least-privilege Salesforce External Client App, keep secrets out of repositories and command-line arguments, and avoid sourcing generated credentials.env files.

Risk: Authentication workflows can be pointed at an unintended or invalid Salesforce domain.

Mitigation: Validate that target domains are real Salesforce org domains before authentication.

Risk: Automatic fix loops or worker orchestration can make unintended changes when run against production orgs.

Mitigation: Run automation in non-production by default and require explicit review before any production execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dsouza-anush/skills/sf-ai-agentforce-testing)
- [Salesforce Agent Testing API and CLI](https://developer.salesforce.com/docs/einstein/genai/guide/testing-api-cli.html)
- [Salesforce Agent DX Test Run Guide](https://developer.salesforce.com/docs/einstein/genai/guide/agent-dx-test-run.html)
- [Salesforce CLI Agent Commands](https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_agent_commands_unified.htm)
- [Salesforce Agentforce Testing Center](https://help.salesforce.com/s/articleView?id=ai.agent_testing_center.htm)
- [Interview Wizard](references/interview-wizard.md)
- [Multi-Turn Testing](references/multi-turn-testing.md)
- [CLI Commands Reference](references/cli-commands.md)
- [Test Spec Reference](references/test-spec-reference.md)
- [Connected App Setup](references/connected-app-setup.md)
- [Coverage Analysis](references/coverage-analysis.md)
- [Agentic Fix Loops](references/agentic-fix-loops.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with YAML examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce test plans, test specs, pass/fail summaries, coverage gaps, root-cause themes, and recommended next test steps.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
