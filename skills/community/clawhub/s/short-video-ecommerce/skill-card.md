## Description: <br>
Automates short-form ecommerce workflows from product sourcing and 15-second scripts to AI media prompts, compliance checks, listing support, and performance review templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laomao-at](https://clawhub.ai/user/laomao-at) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ecommerce sellers, dropshipping operators, and short-form content creators use this skill to plan product promotions, generate scripts and media prompts, prepare platform-specific listing material, and track campaign results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The visible artifact documentation describes YouTube Shorts generation while server security evidence and code behavior indicate ecommerce and dropshipping automation. <br>
Mitigation: Review the source and intended workflow before installing, and treat the skill as an ecommerce automation package. <br>
Risk: Marketplace credentials or sensitive API keys could enable commerce listing workflows. <br>
Mitigation: Use least-privilege or sandbox credentials and provide production marketplace credentials only after confirming the workflow is intended. <br>
Risk: Generated product listings, compliance checks, and platform publishing support may be incomplete or inaccurate. <br>
Mitigation: Manually review product claims, brand authorization, sensitive wording, and platform rules before publishing. <br>
Risk: The workflow may send prompts, product details, or media tasks to third-party AI or media services when API keys are configured. <br>
Mitigation: Avoid submitting private or sensitive product data unless the connected services and their terms are acceptable. <br>
Risk: The skill writes local output files for sourcing, media prompts, and review material. <br>
Mitigation: Check the configured output directory and review generated files before sharing or uploading them. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/laomao-at/short-video-ecommerce) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill manifest](artifact/skill.json) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Plain text and markdown-style sections with local file paths, generated prompts, checklists, and optional shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local media outputs, API-key-gated AI services, and ecommerce platform publishing settings when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
