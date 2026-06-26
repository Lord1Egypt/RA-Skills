## Description: <br>
Generate and sync a README environment-variable table from .env.example using marker blocks, with drift detection for CI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to keep README environment-variable documentation aligned with an env template, detect drift in CI, and optionally update the marked README table. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Apply mode can modify the README file selected by environment variables. <br>
Mitigation: Run the default report mode first, and set ENV_FILE and README_FILE to the intended repository paths before using SYNC_MODE=apply. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniellummis/readme-env-table-sync) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Sync script](artifact/scripts/sync-readme-env-table.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown table updates, terminal summaries, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash and python3; report mode detects drift, apply mode updates the README marker block.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
