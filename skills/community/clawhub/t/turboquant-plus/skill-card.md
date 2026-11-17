## Description:

TurboQuant+ helps agents guide Apple Silicon users through llama.cpp TurboQuant KV cache compression settings for larger local LLM contexts with controlled quality tradeoffs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wukai8289](https://clawhub.ai/user/wukai8289)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and local AI practitioners use this skill to choose TurboQuant cache settings, build the referenced llama.cpp fork, and run Apple Silicon LLM inference with lower KV cache memory use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release asks users to build and run mutable third-party native code.

Mitigation: Pin a reviewed commit or verified release and build in a least-privileged environment before using the resulting binaries.

Risk: The artifact includes a privileged GPU memory tuning command for macOS.

Mitigation: Run the sudo sysctl command only after recording the prior setting and confirming how to restore it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wukai8289/skills/turboquant-plus)
- [TurboQuant llama.cpp fork](https://github.com/TheTom/llama-cpp-turboquant)
- [Getting Started Guide](https://github.com/TheTom/llama-cpp-turboquant/tree/main/docs/getting-started.md)
- [Configuration Recommendations](https://github.com/TheTom/llama-cpp-turboquant/tree/main/docs/turboquant-recommendations.md)
- [TurboQuant Paper](https://research.google/blog/turboquant-redefining-ai-efficiency-with-extreme-compression/)
- [Asymmetric K/V Compression](https://github.com/TheTom/llama-cpp-turboquant/tree/main/docs/papers/asymmetric-kv-compression.md)
- [M5 Max Stress Test](https://github.com/TheTom/llama-cpp-turboquant/tree/main/docs/papers/m5-max-stress-test.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with tables and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes scenario-based cache recommendations and warnings around third-party native builds and privileged system tuning.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
