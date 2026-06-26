## Description: <br>
Provides configuration guidance for TurboQuant+ KV cache compression with llama.cpp on Apple Silicon, including cache formats, asymmetric K/V settings, and long-context setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wukai8289](https://clawhub.ai/user/wukai8289) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and local LLM operators use this skill to choose TurboQuant+ KV cache settings for llama.cpp on Apple Silicon, balancing quality, memory use, and context length. It also supplies shell command examples for building the referenced fork and running llama-server configurations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill references building and using an external TurboQuant llama.cpp fork. <br>
Mitigation: Verify the repository source and pin a trusted commit or release before building or running it. <br>
Risk: One long-context example uses sudo sysctl to change a local macOS GPU memory setting. <br>
Mitigation: Run that command only after understanding the setting, recording the prior value, and preparing a rollback such as restoring the old value or rebooting where applicable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wukai8289/turboquant-plus) <br>
- [llama.cpp TurboQuant fork](https://github.com/TheTom/llama-cpp-turboquant) <br>
- [Getting Started Guide](https://github.com/TheTom/llama-cpp-turboquant/tree/main/docs/getting-started.md) <br>
- [Configuration Recommendations](https://github.com/TheTom/llama-cpp-turboquant/tree/main/docs/turboquant-recommendations.md) <br>
- [TurboQuant Paper and Google Research overview](https://research.google/blog/turboquant-redefining-ai-efficiency-with-extreme-compression/) <br>
- [Asymmetric K/V Compression](https://github.com/TheTom/llama-cpp-turboquant/tree/main/docs/papers/asymmetric-kv-compression.md) <br>
- [M5 Max Stress Test](https://github.com/TheTom/llama-cpp-turboquant/tree/main/docs/papers/m5-max-stress-test.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and configuration tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no runtime dependency is bundled with the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
