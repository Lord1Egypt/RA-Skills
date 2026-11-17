## Description:

Taobao Advisor generates read-only Taobao advertising plans, optimization suggestions, review reports, and lifecycle guidance for men's apparel campaigns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guowaa223](https://clawhub.ai/user/guowaa223)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce operators and marketing teams use this skill to draft Taobao advertising test plans, adjustment review sheets, periodic performance reports, and product lifecycle guidance. The skill is advisory only, with all campaign and budget changes reviewed and executed manually outside the skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advertising recommendations could be mistaken for approved campaign changes.

Mitigation: Keep the skill in advisory mode and require manual review before any budget, bid, targeting, or campaign status change is executed in Taobao systems.

Risk: Runtime dependencies may change behavior if installed without version control.

Mitigation: Install in a virtual environment and pin or review dependencies before operational use.

Risk: The skill writes local logs and report files that may contain campaign identifiers or business metrics.

Mitigation: Run it in a controlled workspace and handle generated logs and reports according to the user's data retention and access policies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guowaa223/skills/taobao-advisor)
- [Publisher profile](https://clawhub.ai/user/guowaa223)
- [Skill definition](artifact/SKILL.md)
- [Usage README](artifact/README.md)
- [Runtime requirements](artifact/requirements.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown, terminal text, and local Excel report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local reports and logs; all advertising actions require human review and manual execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
