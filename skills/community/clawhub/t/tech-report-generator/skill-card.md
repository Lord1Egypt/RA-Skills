## Description: <br>
Generates structured technical reports for onboarding and training, including Markdown and HTML outputs with SVG visualizations and optional synchronization to IMA knowledge bases and Tencent Docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fandywang87](https://clawhub.ai/user/fandywang87) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical leads, and training authors use this skill to turn a technical topic into a newcomer-friendly deep technical report with diagrams, tables, summaries, Markdown, and HTML. It is especially suited for creating tutorials, onboarding materials, and internal knowledge-sharing documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The normal workflow can publish generated reports to IMA and Tencent Docs using local credentials without a clear approval gate. <br>
Mitigation: Before syncing, verify the target knowledge base, Tencent Docs account, sharing permissions, and credentials, and review each report for confidential or inappropriate content. <br>


## Reference(s): <br>
- [Report Structure Template](references/report-template.md) <br>
- [SVG Visualization Design Guide](references/svg-design-guide.md) <br>
- [Sync Distribution Workflow](references/sync-workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and HTML with inline SVG, tables, pseudocode, and synchronization guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated report files and publishing steps for IMA and Tencent Docs when the required credentials and tools are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
