## Description: <br>
This skill helps agents search Chinese statutes, cases, regulations, enterprise records, and legal hallucination checks through the Yuandian/Open Chinese Law API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cat-xierluo](https://clawhub.ai/user/cat-xierluo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Legal practitioners, researchers, and agents use this skill to retrieve current Chinese legal materials, compare cases, check citations, perform enterprise due diligence, and generate archived legal research reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Legal queries, case facts, and company due-diligence text may be sent to the Yuandian/Open Chinese Law service and stored locally. <br>
Mitigation: Use only with authorization for the matter, avoid unnecessary sensitive details, protect scripts/.env and local archives, and use --no-cwd-report or --no-report for sensitive work. <br>
Risk: The skill includes an unsigned self-update path that can replace skill files. <br>
Mitigation: Avoid do-update unless the upstream GitHub source and proposed changes have been independently verified. <br>
Risk: The artifact recommends disabling safeguards for some network scenarios. <br>
Mitigation: Keep normal sandbox and approval protections enabled unless an operator explicitly approves a constrained, isolated environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cat-xierluo/yuandian-law-search) <br>
- [Publisher Profile](https://clawhub.ai/user/cat-xierluo) <br>
- [Clawdis Homepage](https://github.com/cat-xierluo/legal-skills) <br>
- [Yuandian/Open Chinese Law Platform](https://open.chineselaw.com) <br>
- [Endpoint Manifest](endpoints/MANIFEST.json) <br>
- [Keyword Expansion](references/01-keyword-expansion.md) <br>
- [Typical Workflows](references/02-typical-workflows.md) <br>
- [Report Consolidation](references/03-report-consolidation.md) <br>
- [Report Design Notes](references/04-report-design-notes.md) <br>
- [MCP Workflow](references/05-mcp-workflow.md) <br>
- [Enterprise Portrait](references/06-enterprise-portrait.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and generated legal research reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include archived API responses, report files, citation checks, and point-cost summaries for Yuandian/Open Chinese Law API calls.] <br>

## Skill Version(s): <br>
1.7.4 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
