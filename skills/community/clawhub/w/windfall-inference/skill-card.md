## Description: <br>
Spatially-routed LLM inference at $0.004/req. Routes to cheapest, greenest energy. 200+ models. OpenAI-compatible. Onchain attestations on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[papa-raw](https://clawhub.ai/user/papa-raw) <br>

### License/Terms of Use: <br>
Business Source License 1.1 <br>


## Use Case: <br>
External developers and agents use Windfall Inference as an OpenAI-compatible gateway for paid LLM chat completions with routing modes for lower cost, lower carbon intensity, or a balanced tradeoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Windfall is a third-party remote inference and billing service that may involve routing, caching, logging, OpenRouter forwarding, and onchain attestations. <br>
Mitigation: Do not send secrets or regulated data unless those service behaviors are acceptable for the workflow. <br>
Risk: The authoritative security evidence says the dashboard and top-up pages store API keys or wallet sessions in browser localStorage and that top-up copy gives a false assurance about API key handling. <br>
Mitigation: Use dedicated low-privilege Windfall keys, avoid shared browsers, clear browser storage after use, and verify payment and API-key behavior before sensitive use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/papa-raw/windfall-inference) <br>
- [Windfall homepage](https://windfall.ecofrontiers.xyz) <br>
- [OpenAI-compatible API base](https://windfall.ecofrontiers.xyz/v1) <br>
- [Chat completions endpoint](https://windfall.ecofrontiers.xyz/v1/chat/completions) <br>
- [Dashboard](https://windfall.ecofrontiers.xyz/dashboard) <br>
- [Status](https://windfall.ecofrontiers.xyz/status) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, shell commands, configuration, guidance] <br>
**Output Format:** [OpenAI-compatible chat completion JSON plus Markdown setup guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WINDFALL_API_KEY for API-key authentication, or x402/Base wallet payment for keyless paid requests; max_tokens is capped at 8192 and the documented rate limit is 60 requests per minute.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; package.json reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
