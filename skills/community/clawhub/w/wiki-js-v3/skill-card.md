## Description: <br>
Provides Wiki.js administration through GraphQL and REST operations for pages, assets, search, tags, page trees, history, versioning, and rendering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nyhx1101](https://clawhub.ai/user/nyhx1101) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent or CLI administer a Wiki.js instance, including page, asset, search, tag, history, render, and version operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform destructive Wiki.js administration actions, including delete, asset-delete, tag delete, upload, move, restore, and upsert operations. <br>
Mitigation: Use a dedicated least-privilege Wiki.js API token and manually review destructive or content-changing commands before execution. <br>
Risk: A misconfigured WIKIJS_URL can direct administration commands at the wrong Wiki.js instance. <br>
Mitigation: Verify WIKIJS_URL before running write, delete, upload, restore, or move operations. <br>
Risk: Exposure of WIKIJS_TOKEN would allow Wiki.js actions within the token's permissions. <br>
Mitigation: Provide WIKIJS_TOKEN through environment or secret management, keep it out of logs and committed files, and rotate dedicated tokens when access changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nyhx1101/wiki-js-v3) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Wiki.js URL and API token configuration before use] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
