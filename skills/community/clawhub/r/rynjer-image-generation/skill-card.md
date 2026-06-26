## Description: <br>
Generates and refines image prompts, estimates costs, recommends image sizes, and submits marketing image-generation jobs for agent workflows through Rynjer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Antipas](https://clawhub.ai/user/Antipas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add a short marketing-image workflow that rewrites rough prompts, estimates credit cost, chooses practical size defaults, generates images, and polls for results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode sends prompts and generation settings to Rynjer. <br>
Mitigation: Avoid secrets and confidential business details in prompts unless the operator intends to share them with Rynjer. <br>
Risk: Image generation can spend Rynjer credits. <br>
Mitigation: Run estimate_image_cost before generate_image, keep count and resolution modest, and use a limited Rynjer token. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/Antipas/rynjer-image-generation) <br>
- [README](artifact/README.md) <br>
- [Tool schema draft](artifact/SCHEMA.md) <br>
- [Implementation notes](artifact/IMPLEMENTATION.md) <br>
- [Tool definitions](artifact/src/tools.json) <br>
- [Templates and size recommendations](artifact/src/templates.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON tool inputs and structured JSON tool results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Live mode can return Rynjer request IDs, cost estimates, task status, and generated image URLs; mock mode returns local test responses without credentials.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
