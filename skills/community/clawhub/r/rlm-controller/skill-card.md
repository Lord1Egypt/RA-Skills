## Description: <br>
RLM-style long-context controller that treats inputs as external context, slices/peeks/searches, and spawns recursive subcalls with strict safety limits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Skywyze](https://clawhub.ai/user/Skywyze) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and engineers use RLM Controller to analyze very large documents, logs, datasets, or repositories by storing inputs externally, slicing and searching context, spawning bounded sub-agent work, and aggregating findings with traceability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled helper scripts can write analysis artifacts and spawn sub-agent sessions. <br>
Mitigation: Install only when that behavior fits the deployment threat model, and keep executions within the documented policy limits. <br>
Risk: Generated prompts, logs, and traces may include sensitive content from the analyzed inputs. <br>
Mitigation: Keep redaction enabled for sensitive repositories or logs, and review generated prompts and logs before sharing them. <br>
Risk: Using cleanup with CLEAN_RETENTION=0 removes retained RLM scratch artifacts. <br>
Mitigation: Review retention settings and ignore rules before cleanup when run artifacts need to be preserved. <br>


## Reference(s): <br>
- [RLM Controller on ClawHub](https://clawhub.ai/Skywyze/rlm-controller) <br>
- [Publisher profile: Skywyze](https://clawhub.ai/user/Skywyze) <br>
- [OpenClaw framework](https://github.com/Skywyze/openclaw) <br>
- [Security documentation](docs/security.md) <br>
- [Policy and limits](docs/policy.md) <br>
- [Workflow documentation](docs/flows.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces plans, spawn manifests, toolcall JSON, logs, summaries, and cleanup commands for bounded long-context workflows.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
