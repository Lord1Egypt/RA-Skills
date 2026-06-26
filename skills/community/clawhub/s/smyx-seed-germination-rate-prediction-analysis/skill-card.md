## Description: <br>
Analyzes seedling tray images or videos to identify emerged seedlings, count germinated seeds, estimate germination rate, and surface historical germination reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and greenhouse, seed-testing, or home-planting operators use this skill to submit seedling tray media, receive visual seedling counts, estimate germination rate, and retrieve historical analysis reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User media and account-linked metadata are sent to LifeEmergence cloud APIs. <br>
Mitigation: Deploy only where users consent to external processing and the configured LifeEmergence endpoints are approved. <br>
Risk: The skill silently creates or reuses a local identity and stores tokens in a workspace SQLite database. <br>
Mitigation: Use isolated workspaces per user or session, restrict access to workspace data, and clear local identity and token data during deprovisioning. <br>
Risk: Historical report retrieval can expose account-linked report records. <br>
Mitigation: Confirm report ownership and tenant isolation before enabling shared or multi-user access. <br>


## Reference(s): <br>
- [API documentation](references/api_doc.md) <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-seed-germination-rate-prediction-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON text, with optional saved output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include emerged-seedling counts, germination-rate estimates, development-stage observations, historical report links, and low-rate alerts.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence; artifact frontmatter says 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
