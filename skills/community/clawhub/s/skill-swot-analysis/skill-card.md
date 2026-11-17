## Description:

Guides an agent through an interactive SWOT analysis, collecting user-provided strengths, weaknesses, opportunities, and threats before generating SO/WO/ST/WT strategy recommendations and report outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Business users, strategy teams, and consultants use this skill to structure SWOT analysis for a department, product, project, or supplier and turn user-confirmed inputs into strategy recommendations and presentation-ready reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SWOT findings and strategy recommendations can be incomplete or misleading if the user-provided business context is sparse, inaccurate, or outdated.

Mitigation: Collect concrete inputs for all four SWOT quadrants and have stakeholders review generated strategies before relying on them.

Risk: The workflow is written for Chinese-language interaction, which may create review or comprehension gaps for teams that do not operate in Chinese.

Mitigation: Use the skill only where users can review Chinese-language prompts and outputs, or translate and review the result before decisions are made.

Risk: Skipped SWOT quadrants can distort the generated SO, WO, ST, or WT strategy combinations.

Mitigation: Mark missing quadrants as unconfirmed or placeholders and revisit them before final strategy planning.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-swot-analysis)
- [GitHub source repository](https://github.com/duding-engicool/skill-swot-analysis)
- [GitHub source commit](https://github.com/duding-engicool/skill-swot-analysis/commit/3d692ef5f09dee66b68f614ede328a4135740899)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Interactive prompts followed by Markdown report content and HTML code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided SWOT inputs; missing quadrants should be marked as unconfirmed or placeholders.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
