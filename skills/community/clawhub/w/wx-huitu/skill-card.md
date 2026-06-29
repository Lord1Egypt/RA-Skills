## Description: <br>
Wx Huitu helps agents turn article or data descriptions into WeChat-ready PNG chart packs by profiling the data, recommending one of 18 chart layouts, generating HTML, and screenshotting the result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardwason](https://clawhub.ai/user/edwardwason) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content teams, editors, and data storytellers use this skill to convert article data or metric descriptions into static PNG charts for WeChat public-account articles, with chart-choice checks before generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated chart files may be uploaded to Feishu cloud storage as part of the standard delivery path without a clear per-task consent step. <br>
Mitigation: Use a local-only workflow for sensitive drafts or require explicit confirmation before any cloud upload. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/edwardwason/wx-huitu) <br>
- [Workflow Reference](references/workflow.md) <br>
- [Chart System Reference](references/chart-system.md) <br>
- [Design Tokens Reference](references/design-tokens.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with generated HTML and PNG chart files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates fixed-size HTML/SVG chart assets, screenshots them to PNG, saves them locally, and may sync them to Feishu cloud storage.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
