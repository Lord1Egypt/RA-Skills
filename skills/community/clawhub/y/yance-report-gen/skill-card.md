## Description:

研策Skill — 综合投研报告生成，多角色观点归一化合成

This skill is for demonstration purposes and not for production usage.

## Publisher:

[caoling7878-arch](https://clawhub.ai/user/caoling7878-arch)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to combine Chinese-language role-analysis JSON files into a dated Markdown investment-research report for course teaching demonstrations. The generated report is explicitly not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated teaching-demo investment reports may be mistaken for investment advice.

Mitigation: Keep the disclaimer with generated reports and have a qualified reviewer check the inputs and report before any external use.

Risk: Missing or incomplete role JSON inputs produce placeholder sections instead of full analysis.

Mitigation: Provide the intended role JSON files and review the report for teaching-demo placeholder markers before sharing it.

Risk: The script creates the selected output directory and writes a dated Markdown report there.

Mitigation: Choose a deliberate output path and run the script only with files intended for report generation.

## Reference(s):


## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration]

**Output Format:** [Markdown report file with optional JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a dated report named 研家团投研报告_YYYY-MM-DD.md to the selected output directory; missing role inputs are marked as teaching-demo placeholders.]

## Skill Version(s):

1.0.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
