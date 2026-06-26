## Description: <br>
AI trading card generator for designing custom collectible card art in MTG, Pokemon, Yu-Gi-Oh, and sports card styles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omactiengartelle](https://clawhub.ai/user/omactiengartelle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate collectible trading card images from text prompts, with optional size selection and reference-image style inheritance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional reference IDs, and the Neta API token are sent to api.talesofai.com. <br>
Mitigation: Avoid sensitive prompts or reference IDs, and use the skill only when sharing those inputs with the external API is acceptable. <br>
Risk: The --token argument can appear in shell history, logs, or process listings. <br>
Mitigation: Run commands in a private shell, clear shell history when needed, and prefer safer secret-handling practices where available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/omactiengartelle/trading-card-generator) <br>
- [Neta API token page](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, text] <br>
**Output Format:** [String containing a generated image URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token passed with --token; supports portrait, landscape, square, and tall image sizes plus an optional reference image UUID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
