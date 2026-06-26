## Description: <br>
Run document processing workflows using Upstage Document Agent API (v2) for Studio-configured agents and API-defined agents or configs, including file upload, agent/config creation, job execution, and result polling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[upstage-deployment](https://clawhub.ai/user/upstage-deployment) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to run Upstage Document Agent workflows that parse, classify, extract, and route document processing jobs through Studio-created or REST-defined agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents and derived outputs are sent to Upstage's API for processing. <br>
Mitigation: Use only documents approved for external processing, avoid confidential or regulated content unless authorized, and delete uploaded files or jobs when cleanup is appropriate. <br>
Risk: Agent publishing, resource deletion, or cloning historical jobs can expose or remove workflow resources. <br>
Mitigation: Require explicit user confirmation before public publishing, deleting resources, or cloning jobs with historical data. <br>
Risk: The skill requires a sensitive Upstage API credential. <br>
Mitigation: Read the key from UPSTAGE_API_KEY, avoid hard-coding secrets, and keep credentials out of generated files and logs. <br>


## Reference(s): <br>
- [Upstage Studio](https://console.upstage.ai/studio) <br>
- [ClawHub skill page](https://clawhub.ai/upstage-deployment/upstage-studio) <br>
- [Agents & Configs API](references/agents-and-configs.md) <br>
- [Files API](references/files.md) <br>
- [Responses & Jobs API](references/jobs.md) <br>
- [Step Types](references/step-types.md) <br>
- [Preset Agents](references/preset-agents.md) <br>
- [End-to-End Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON files, guidance] <br>
**Output Format:** [Markdown guidance with Python or curl examples; workflow and per-step results are written as JSON files when the agent runs jobs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires UPSTAGE_API_KEY and may print resolved absolute output paths for generated result files.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
