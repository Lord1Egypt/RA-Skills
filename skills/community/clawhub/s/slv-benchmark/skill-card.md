## Description: <br>
Run benchmark tests and connectivity checks for SLV endpoints using shredstream, grpc, or rpc with region-aware configuration and API key support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[poppin-fumi](https://clawhub.ai/user/poppin-fumi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to compare Solana shredstream, gRPC, and RPC endpoints by collecting benchmark type, region, endpoint URLs, and ERPC API key configuration before generating or running benchmark checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read and use a saved ERPC API key from ~/.slv/api.yml during benchmark runs. <br>
Mitigation: Require explicit user confirmation before reading or using the key, redact the key from generated config and output, and avoid sharing benchmark output that may contain secrets. <br>
Risk: The skill may run a local geyserbench binary with generated endpoint configuration. <br>
Mitigation: Review the generated config and command before execution, and verify the local geyserbench binary before allowing it to run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/poppin-fumi/slv-benchmark) <br>
- [SLV project repository](https://github.com/ValidatorsDAO/slv) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with TOML configuration snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use a local ERPC API key from ~/.slv/api.yml and may return benchmark output directly.] <br>

## Skill Version(s): <br>
0.13.15 (source: server release evidence; artifact skill.json lists 0.9.962) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
