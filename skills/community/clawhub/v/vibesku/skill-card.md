## Description: <br>
CLI for VibeSKU, an AI-powered creative automation platform that turns product SKU photos into professional e-commerce visuals and marketplace-ready copy at scale. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[visoar](https://clawhub.ai/user/visoar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, e-commerce operators, and agents use this skill to authenticate with VibeSKU, select generation templates, run image or listing-copy jobs, refine outputs, export results, and manage batch or credit workflows from the command line. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI can access a VibeSKU account and use API keys or browser-login tokens stored in local configuration. <br>
Mitigation: Protect VIBESKU_API_KEY and ~/.vibesku/config.json, avoid exposing credentials in shared logs, and revoke or rotate credentials if they are mishandled. <br>
Risk: Generation, refinement, upload, export, and batch commands can send selected product assets to VibeSKU and consume or purchase account credits. <br>
Mitigation: Review product assets and generated command arguments before execution, use dry-run or JSON inspection for batch work when available, and confirm credit-impacting actions with the user. <br>
Risk: The skill recommends updating from an upstream source when the local version is stale. <br>
Mitigation: Require explicit user approval before installing or updating the skill from GitHub or any other upstream source. <br>
Risk: A custom VIBESKU_BASE_URL or configured base URL could direct requests to an untrusted service. <br>
Mitigation: Use only trusted VibeSKU base URLs and inspect configuration before authenticating, uploading assets, or running generation commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/visoar/vibesku) <br>
- [VibeSKU homepage](https://www.vibesku.com) <br>
- [Command reference](references/commands.md) <br>
- [E-commerce hero template](references/ecom-hero.md) <br>
- [Exploded-view template](references/exploded-view.md) <br>
- [Key visual image-set template](references/kv-image-set.md) <br>
- [Listing copy template](references/listing.md) <br>
- [Versioning and update guidance](references/versioning.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may upload selected product assets, download generated image or text outputs, and use VibeSKU account credits.] <br>

## Skill Version(s): <br>
0.2.4 (source: release evidence and VERSION) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
