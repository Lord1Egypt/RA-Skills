## Description: <br>
Query Wisgate for model pricing, capabilities, and configuration details when adding a model to OpenClaw, comparing Wisgate pricing, or checking whether a model supports a specific API type. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flofrie](https://clawhub.ai/user/flofrie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect Wisgate model capabilities, pricing, endpoint types, and configuration fields before updating OpenClaw model settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide changes to OpenClaw model configuration files, and incorrect values could misconfigure model routing, pricing, or capabilities. <br>
Mitigation: Review proposed changes to openclaw.json and MODELS.json before writing or deploying them. <br>
Risk: The Firecrawl fallback uses a sensitive API key and depends on a separate scraping script. <br>
Mitigation: Only allow the Firecrawl fallback when the user trusts the Firecrawl script and is comfortable using the API key referenced in TOOLS.md. <br>


## Reference(s): <br>
- [Wisgate model catalog](https://wisgate.ai/models/MODEL_ID) <br>
- [Wisgate Anthropic-compatible API base URL](https://api.wisgate.ai/) <br>
- [Wisgate OpenAI-compatible API base URL](https://api.wisgate.ai/v1) <br>
- [Wisgate Google-compatible API base URL](https://api.wisgate.ai/v1beta) <br>
- [ClawHub skill page](https://clawhub.ai/flofrie/wisgate-models) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, code, shell commands, markdown] <br>
**Output Format:** [Markdown with inline JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend edits to MODELS.json and openclaw.json and may propose a Firecrawl scrape command when catalog data is missing.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
