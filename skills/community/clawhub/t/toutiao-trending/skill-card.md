## Description:

Helps agents retrieve and summarize public Toutiao articles, videos, and topics with lightweight analysis of titles, authors, publish times, interaction data, and tags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to guide agents through keyword-based summaries, channel distribution analysis, and public video metadata summaries for Toutiao content. It is intended for manual or light automation against public pages, with collection time and source links included in results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Use beyond light public-page analysis could violate Toutiao rules or create unwanted bulk collection behavior.

Mitigation: Keep use manual or lightly automated, follow Toutiao's rules, apply frequency controls, and avoid bulk collection.

Risk: Video workflows could be misused to download or remove watermarks from media.

Mitigation: Only summarize public video metadata such as title, description, and visible interactions; do not download media or perform watermark removal.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/codekungfu/skills/toutiao-trending)
- [Toutiao homepage](https://www.toutiao.com/)
- [Toutiao search](https://www.toutiao.com/search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown summaries and procedural guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include titles, authors, publish times, source links, public interaction counts, tags, channel names, collection time, and brief topic statistics.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
