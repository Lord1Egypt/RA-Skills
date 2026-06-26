## Description: <br>
Cross-platform second-hand price comparison and in-depth item evaluation across supported marketplaces, including seller trust, condition, and value assessment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fastislow](https://clawhub.ai/user/fastislow) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and shopping agents use this skill to compare used-item listings across supported marketplaces and evaluate shortlisted listings for price, seller trust, condition, and buy recommendations. <br>

### Deployment Geography for Use: <br>
United Kingdom for current marketplace support; additional regions are listed as coming later. <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses active browser sessions for supported marketplace searches, which can expose signed-in shopping context. <br>
Mitigation: Use a separate browser profile or a signed-out session for privacy-sensitive shopping. <br>
Risk: The skill can manage local bb-browser state and write marketplace adapters under the user's home directory. <br>
Mitigation: Review adapter installation behavior before first use and run it only in environments where local bb-browser changes are acceptable. <br>
Risk: Optional vision analysis may send listing photos and descriptions to the configured vision API provider. <br>
Mitigation: Enable the vision API only when the configured provider and data sharing are acceptable for the listings being evaluated. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fastislow/used-price-compare) <br>
- [Chinese instructions](references/zh-CN.md) <br>
- [Compare sub-skill](skills/compare/SKILL.md) <br>
- [Evaluate sub-skill](skills/evaluate/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown tables and narrative recommendations with inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bb-browser adapters for marketplace access; optional vision analysis requires a configured API key.] <br>

## Skill Version(s): <br>
0.6.4 (source: frontmatter, pyproject.toml, CHANGELOG, released 2026-05-21) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
