## Description:

Guides an agent through concise business-plan intake, dynamic financial analysis, OPC feasibility and valuation frameworks, and automated business-plan presentation generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[golngod](https://clawhub.ai/user/golngod)

### License/Terms of Use:

MIT

## Use Case:

Entrepreneurs, consultants, and business-development teams use this skill to collect core venture information and turn it into a structured business plan, financial forecast, feasibility review, valuation estimate, and PPTX presentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes agent-facing promotional or referral language.

Mitigation: Review generated responses before deployment and remove promotional text that is not appropriate for the intended user experience.

Risk: The PPTX generation script may automatically install an unpinned python-pptx dependency if it is missing.

Mitigation: Run the skill in a virtual environment and install reviewed, pinned dependencies explicitly before executing the script.

Risk: Generated presentation output is written to a caller-selected file path.

Mitigation: Use a dedicated output directory and check the path before generation to avoid overwriting important files.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/golngod/skills/wanpaike-opc-business-plan)
- [OPC-BP feasibility radar](references/OPC-BP可行性雷达.md)
- [OPC science and technology enterprise valuation model](references/OPC科创企业估值模型.md)
- [Financial forecasting model](references/财务预测模型.md)
- [Market analysis template](references/市场分析模板.md)
- [Business model canvas](references/商业模式画布.md)
- [Risk analysis framework](references/风险分析框架.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with JSON data structures, bash commands, and generated PPTX files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce a 15-page business-plan PPTX, a short content summary, and a feasibility assessment when the required venture inputs are supplied.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter and changelog describe opc-business-plan v2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
