## Description: <br>
Set up, run, compare, and debug StockValuation.io, a local-first DCF valuation platform, including Docker startup, ticker valuations, LLM provider changes, prompt dumping, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[softcane](https://clawhub.ai/user/softcane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to set up and operate a local StockValuation.io environment for DCF valuation runs, model/provider comparisons, prompt inspection, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup uses local secrets and multiple provider API keys. <br>
Mitigation: Keep secrets in a local .env file, provide only the keys needed for the workflow, and avoid pasting or printing live credentials. <br>
Risk: Prompt dumping can write sensitive prompt contents, ticker context, and retrieved research snippets to disk. <br>
Mitigation: Enable prompt dumping only for intentional inspection, choose a local output directory, and clean up dumped prompts after use. <br>
Risk: Docker volume deletion can erase local application state. <br>
Mitigation: Use destructive Docker cleanup such as volume deletion only when intentionally resetting local state. <br>
Risk: Installer scripts and Docker Compose files may execute local setup actions. <br>
Mitigation: Inspect the cloned repository and installer or Docker Compose file before running them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/softcane/stockvaluation-io) <br>
- [StockValuation.io GitHub Repository](https://github.com/stockvaluation-io/stockvaluation_io) <br>
- [Setup And Run](references/setup-and-run.md) <br>
- [Model And Provider Experiments](references/model-and-provider-experiments.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, markdown] <br>
**Output Format:** [Markdown with inline shell commands, configuration values, and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local Docker Compose commands, environment variable guidance, health checks, and valuation request examples.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
