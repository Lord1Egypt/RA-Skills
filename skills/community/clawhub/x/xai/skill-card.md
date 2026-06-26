## Description: <br>
Chat with Grok models via xAI API. Supports Grok-4, Grok-4.20, Grok-3, Grok-3-mini, vision, and real-time X search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mvanhorn](https://clawhub.ai/user/mvanhorn) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to ask Grok models for text responses, analyze selected images, search recent X posts with citations, and list xAI models from a configured xAI API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, X search queries, and any selected image files are sent to xAI when the skill's commands run. <br>
Mitigation: Use a dedicated xAI API key where possible, avoid sending sensitive prompts or files unless appropriate, and monitor API usage or billing. <br>
Risk: The bundled version metadata is inconsistent across the server release, skill frontmatter, and package.json. <br>
Mitigation: Treat the server release version as the release identifier and verify the repository or release before deployment. <br>


## Reference(s): <br>
- [xAI ClawHub skill page](https://clawhub.ai/mvanhorn/xai) <br>
- [xAI API documentation](https://docs.x.ai/api) <br>
- [xAI documentation](https://docs.x.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or JSON command output, including X search citations when available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires XAI_API_KEY and sends prompts, search queries, and selected image files to xAI under the user's API key.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release evidence; artifact frontmatter is 1.1.0 and package.json is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
