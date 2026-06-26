## Description: <br>
Accesses the sora-2 model on the vwu.ai platform through an OpenAI-compatible chat completions API using a user-supplied API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a3273283](https://clawhub.ai/user/a3273283) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure a vwu.ai API key and send prompts to the supported sora-2 chat model from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and chat content are sent to vwu.ai for processing. <br>
Mitigation: Use only data approved for that provider and avoid submitting secrets or regulated data unless the provider has been approved for that use. <br>
Risk: The wrapper uses a user-supplied API key and supports an alternate VWU_BASE_URL. <br>
Mitigation: Use a dedicated API key where possible, protect the environment variable, and leave VWU_BASE_URL unset unless the alternate endpoint is intentionally trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/a3273283/vwu-sora) <br>
- [vwu.ai](https://vwu.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the selected chat completion content from the vwu.ai API; requires VWU_API_KEY and optionally accepts VWU_BASE_URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
