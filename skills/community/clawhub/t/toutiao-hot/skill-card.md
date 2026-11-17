## Description:

Fetches Toutiao hot-list and trending-news data, including ranked titles, heat values, cleaned detail links, optional cover images, labels, cluster IDs, and categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noah-1106](https://clawhub.ai/user/noah-1106)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to fetch current Toutiao hot-board rankings and optionally persist them to a local SQLite database or generate an HTML report for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports may render remote or tampered data unsafely.

Mitigation: Do not open generated reports from untrusted or modified data until HTML output safely escapes remote content.

Risk: scripts/fetch-toutiao.py can execute code from a hard-coded external local skill path.

Mitigation: Avoid that script unless it is changed to call the bundled Toutiao script in this artifact.

Risk: Normal documented commands write a local SQLite database and HTML report under data/.

Mitigation: Review generated local files before sharing, publishing, or opening them in a browser.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/noah-1106/skills/toutiao-hot)
- [Toutiao hot-board endpoint](https://www.toutiao.com/hot-event/hot-board/)
- [Toutiao website](https://www.toutiao.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [JSON hot-list records, terminal text, Markdown usage guidance, local SQLite data, and generated HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normal commands fetch public Toutiao data and may write local files under data/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
