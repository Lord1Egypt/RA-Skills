## Description:

Walter Competitor analyzes Amazon competitor traffic by discovering rival ASINs, mapping traffic and keyword opportunities, identifying weaknesses, and producing ad attack plans with budget and ROI guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beyondbright](https://clawhub.ai/user/beyondbright)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and marketplace operators use this skill to analyze Amazon category competitors from a keyword, price, and optional margin, then plan keyword, traffic, advertising, budget, and ROI actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI wrapper can turn normal user inputs into shell commands.

Mitigation: Do not install for production use until shell=True command execution is removed and arguments are passed safely or a direct API client is used.

Risk: The documented SellerSprite setup flow can expose credentials through shell history or CLI configuration.

Mitigation: Use a safer secret configuration flow and rotate any SellerSprite key already used with the documented command.

Risk: The mcporter dependency is not pinned or localized in the release evidence.

Mitigation: Pin and localize the mcporter dependency, or replace it with a reviewed direct API client, before deployment.

## Reference(s):

- [SIF Data Source Parsing Reference](references/data_parsing.md)
- [SellerSprite MCP Documentation](https://open.sellersprite.com/mcp/43)
- [ClawHub Skill Page](https://clawhub.ai/beyondbright/skills/walter-competitor)
- [ClawHub Publisher Profile](https://clawhub.ai/user/beyondbright)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown-style analysis with structured competitor intelligence, keyword matrices, budget plans, ROI estimates, and setup guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses SellerSprite API access and accepts a keyword, product price, and optional margin.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
