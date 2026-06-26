## Description: <br>
Chat with Grok models via xAI API. Supports Grok-3, Grok-3-mini, vision, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blueberrywoodsym](https://clawhub.ai/user/blueberrywoodsym) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to ask Grok models for text responses, analyze selected image files, list available xAI models, and search X posts through xAI APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, system prompts, X search queries, and selected images are sent to xAI. <br>
Mitigation: Use the skill only when sharing that content with xAI is acceptable, and avoid secrets, personal data, regulated data, and proprietary information. <br>
Risk: Vision use can transmit local image contents selected by path. <br>
Mitigation: Review selected image files before use and do not submit screenshots, documents, or photos that contain sensitive information unless approved for xAI processing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/blueberrywoodsym/x-ai) <br>
- [xAI Documentation](https://docs.x.ai) <br>
- [xAI API Reference](https://docs.x.ai/api) <br>
- [xAI Console](https://console.x.ai) <br>
- [Installation and Use Instructions](https://claude.ai/public/artifacts/5bb1d4ca-68ef-4d74-900c-d14fefa5c094) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Command-line text or JSON from xAI API responses, often presented as Markdown by the invoking agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and XAI_API_KEY; optional inputs include model name, system prompt, selected image path, X search date range, and X handle filters.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
