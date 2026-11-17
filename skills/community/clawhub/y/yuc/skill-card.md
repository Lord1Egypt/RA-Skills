## Description:

Scrape quarterly anime lineups from https://yuc.wiki/ and output structured results for a specified or latest quarter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yjl9903](https://clawhub.ai/user/yjl9903)

### License/Terms of Use:

GNU Affero General Public License v3.0

## Use Case:

Agents and developers use this skill to fetch a seasonal anime quarter from yuc.wiki, extract structured lineup data, and present a concise human-readable airing table grouped by schedule section.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches public web pages and can write JSON to a user-specified output path.

Mitigation: Keep network access scoped to yuc.wiki and provide an output path only when file creation is intended.

Risk: Changes to the yuc.wiki page layout can produce incomplete or suspicious scrape results.

Mitigation: Use the built-in quarter title, empty item, deduplication, and count checks; switch to the manual scrape guide when selector drift is suspected.

## Reference(s):

- [Yuc Anime List](https://yuc.wiki/)
- [Manual Scrape Guide](reference/manual_scrape.md)
- [ClawHub Skill Page](https://clawhub.ai/yjl9903/skills/yuc)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Structured JSON plus a concise Markdown airing table with source quarter information.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output includes quarter_code, quarter_title, source URL, grouped lineup items, status or time, episode notes, platform links, and optional file output when requested.]

## Skill Version(s):

0.0.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
