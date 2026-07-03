## Description: <br>
Using agricultural camera images, this skill detects leaf curl direction and leaf-margin scorch patterns, optionally considers soil-moisture data, and returns likely causes such as drought stress, disease, pesticide damage, or fertilizer burn with directional recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agricultural developers use this skill to analyze plant leaf images or videos for curl direction, scorch distribution, affected leaf layer, likely stress or disease causes, and practical next-step guidance. It can also query cloud-hosted historical diagnosis reports for the same scenario. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Provided plant images, videos, or URLs are processed by a cloud service. <br>
Mitigation: Use non-sensitive agricultural media, review the configured service endpoints before installation, and avoid sending private or regulated files. <br>
Risk: The skill can silently create or reuse a service identity and store returned service tokens in the workspace data directory. <br>
Mitigation: Install only in workspaces where local token storage is acceptable, restrict workspace access, and rotate or remove stored service credentials when no longer needed. <br>
Risk: Diagnosis results are advisory and may confuse drought, disease, pesticide damage, fertilizer burn, or other similar symptoms. <br>
Mitigation: Treat outputs as plant-stress screening guidance and confirm severe or high-impact findings with field inspection or professional crop-protection advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-leaf-curling-scorch-diagnosis-analysis) <br>
- [API interface documentation](references/api_doc.md) <br>
- [Shared analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown text with structured JSON analysis, report links, and optional file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The command-line interface accepts local image or video paths, public media URLs, a history-list mode, detail level, and an optional output file.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter says 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
