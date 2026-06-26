## Description: <br>
Extract recipe information from TikTok links, reconstruct a clean recipe, localize it to the user's language when needed, and import it into Mealie. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Elyasuuuuu](https://clawhub.ai/user/Elyasuuuuu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and self-hosted Mealie operators use this skill to turn TikTok cooking content into structured, localized recipes and import acceptable reconstructions into Mealie. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Mealie credentials to create recipes and upload cover images. <br>
Mitigation: Use a dedicated or least-privilege token if available, keep the token out of shared files and logs, and ask for a preview when import should not happen immediately. <br>
Risk: Sparse or noisy TikTok content can produce an unreliable reconstructed recipe. <br>
Mitigation: Import only when the title, ingredients, and steps meet the documented quality threshold; otherwise stop with a short failure reason or ask one confirmation question. <br>


## Reference(s): <br>
- [Configuration](references/configuration.md) <br>
- [Failure modes](references/failure-modes.md) <br>
- [Localization](references/localization.md) <br>
- [Mealie API notes](references/mealie-api-notes.md) <br>
- [Output templates](references/output-templates.md) <br>
- [Workflow](references/workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown, API Calls, Configuration instructions] <br>
**Output Format:** [Concise text or Markdown containing a recipe link, short failure reason, or one confirmation question.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create Mealie recipes and upload cover images when a Mealie base URL and API token are configured.] <br>

## Skill Version(s): <br>
1.2.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
