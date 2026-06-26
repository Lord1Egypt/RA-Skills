## Description: <br>
Record, inspect, mock, replay, and generate API traffic using the proxymock CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mleray24](https://clawhub.ai/user/mleray24) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to capture, inspect, mock, replay, and generate HTTP, gRPC, and database traffic with proxymock for local testing, regression testing, load testing, and CI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recorded API or database traffic can include secrets, regulated data, or other sensitive content. <br>
Mitigation: Use local or staging traffic when possible, avoid recording production secrets or regulated data, and review and redact RRPair files before sharing or uploading them. <br>
Risk: Proxy environment variables can unintentionally route later application traffic through proxymock. <br>
Mitigation: Unset proxy environment variables after use and prefer child-process mode when practical. <br>
Risk: Replay, load, and cloud workflows can target the wrong service or upload captured traffic. <br>
Mitigation: Confirm replay targets, virtual-user counts, duration, and cloud destinations before running those workflows. <br>


## Reference(s): <br>
- [proxymock Skill Page](https://clawhub.ai/mleray24/proxymock) <br>
- [proxymock CLI Reference](references/cli-reference.md) <br>
- [Language-Specific Proxy Configuration](references/language-reference.md) <br>
- [Speedscale proxymock Language Reference](https://docs.speedscale.com/proxymock/getting-started/language-reference/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Code] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the proxymock binary; replay workflows may create local RRPair files and logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
