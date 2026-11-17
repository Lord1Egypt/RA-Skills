## Description:

Queries public Shanghai residency notice information, including talent-introduction and residence-permit-to-hukou notice lists from the Shanghai International Talent Network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luduoxin](https://clawhub.ai/user/luduoxin)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to help users find current Shanghai residency public notice pages and report official links for talent-introduction and residence-permit conversion notices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes live requests to sh-italent.com and opens notice pages in a local browser by default.

Mitigation: Install only if this network and browser behavior is acceptable; use --no-browser when printed results are sufficient.

Risk: Company and person filtering is described in examples, but the inspected code does not implement that filtering.

Mitigation: Treat company or person searches as unsupported unless the skill code is updated and re-reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luduoxin/skills/shanghai-luohu)
- [Shanghai International Talent Network](https://www.sh-italent.com/)
- [Shanghai residency notice list](https://www.sh-italent.com/News/NewsList.aspx?TagID=5696)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Console text with official notice titles, dates, and URLs; may also open pages in a local browser.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Use --no-browser when only printed results are desired.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
