## Description: <br>
Monitor and analyze Weights & Biases training runs for status, failures, loss curves, comparisons, and experiment health. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrisvoncsefalvay](https://clawhub.ai/user/chrisvoncsefalvay) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and ML engineers use this skill to inspect W&B training runs, detect stalled or failed jobs, review loss and gradient health, compare runs, and generate brief status summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and display data from the user's W&B-authenticated environment, including run metadata, configs, summaries, and metrics. <br>
Mitigation: Install and run it only in environments where the agent is allowed to access W&B data, and avoid storing secrets in W&B configs or summaries. <br>
Risk: No-argument or broad monitoring modes may inspect unintended entities or projects if defaults are not what the user expects. <br>
Mitigation: Pass explicit entity, project, and run arguments, and use all-project or default watch modes only when those scopes are intended. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; helper scripts emit terminal text or JSON when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads W&B-authenticated run metadata and metrics; JSON output is available with --json on supported scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
