## Description: <br>
Agentforce agent testing with dual-track workflow and 100-point scoring for test execution, test spec generation, topic routing validation, and coverage analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dsouza-anush](https://clawhub.ai/user/dsouza-anush) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and Salesforce teams use this skill to plan, run, and analyze Agentforce tests across multi-turn Agent Runtime API workflows, CLI Testing Center specs, preview sessions, coverage checks, and post-publish fix loops. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OAuth credentials can grant access to Salesforce org actions during Agent Runtime API testing. <br>
Mitigation: Use sandbox or test orgs, least-privilege ECA credentials, and avoid passing secrets on the command line. <br>
Risk: Live previews, live org actions, and automated test runs can affect org state or business data. <br>
Mitigation: Prefer simulated actions by default and use controlled test data before enabling live actions. <br>
Risk: Automated fix loops can change, publish, or re-publish agent behavior based on test failures. <br>
Mitigation: Require human review before applying fixes or publishing/re-publishing agents. <br>
Risk: Transcripts, traces, and test results may contain sensitive conversation or org data. <br>
Mitigation: Treat generated results as sensitive and store or share them only in approved locations. <br>
Risk: Injected boolean auth variables are not reliable proof that protected flows are correctly secured. <br>
Mitigation: Validate protected flows with real authorization controls rather than relying only on injected test variables. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dsouza-anush/sf-ai-agentforce-testing) <br>
- [Salesforce Agent Testing API and CLI](https://developer.salesforce.com/docs/einstein/genai/guide/testing-api-cli.html) <br>
- [Salesforce Run Agent Tests](https://developer.salesforce.com/docs/einstein/genai/guide/agent-dx-test-run.html) <br>
- [Salesforce CLI Agent Commands](https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_agent_commands_unified.htm) <br>
- [Salesforce Agentforce Testing Center](https://help.salesforce.com/s/articleView?id=ai.agent_testing_center.htm) <br>
- [Multi-turn testing](references/multi-turn-testing.md) <br>
- [CLI commands](references/cli-commands.md) <br>
- [Test spec reference](references/test-spec-reference.md) <br>
- [Coverage analysis](references/coverage-analysis.md) <br>
- [External Client App setup guide](references/eca-setup-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, YAML test specifications, JSON result summaries, and concise test reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference Salesforce org aliases, Agentforce agent names, ECA credential setup, test specification files, and generated reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
