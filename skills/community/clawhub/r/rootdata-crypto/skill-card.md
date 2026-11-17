## Description:

Query RootData for crypto projects, investors, people, funding rounds, upcoming crypto events, RD and X rankings, stock contract exchanges, and personnel changes. Use for factual Web3 research backed by RootData records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rdquanyu](https://clawhub.ai/user/rdquanyu)

### License/Terms of Use:

MIT-0

## Use Case:

Web3 researchers and analysts use this skill to look up RootData records about crypto projects, investors, people, funding, events, rankings, exchange metrics, and personnel changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was only able to inspect part of one reference file.

Mitigation: Review the skill references before installation, including the portion that was not fully inspected by the scan.

Risk: API requests use a RootData skill key.

Mitigation: Keep ROOTDATA_SKILL_KEY in local secret storage and do not include it in answers, shared files, or URLs.

## Reference(s):

- [RootData Skill API](https://api.rootdata.com/open/skill)
- [RootData Crypto release page](https://clawhub.ai/rdquanyu/skills/rootdata-crypto)
- [Search projects, investors and people](artifact/references/ser_inv.md)
- [List IDs](artifact/references/id_map.md)
- [Project details](artifact/references/get_item.md)
- [Person details](artifact/references/get_people.md)
- [Calendar events](artifact/references/get_event.md)
- [Funding rounds](artifact/references/get_fac.md)
- [RD Hot Index Top 100](artifact/references/hot_index.md)
- [RD Growth Index Top 300](artifact/references/get_rd_top300.md)
- [Stock contract exchange ranking](artifact/references/stock_leaderboard.md)
- [X hot projects](artifact/references/hot_project_on_x.md)
- [X popular people](artifact/references/leading_figures_on_crypto_x.md)
- [Personnel position changes](artifact/references/job_changes.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text research summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Coverage follows RootData records and documented date and investor limits.]

## Skill Version(s):

2.0.0 (source: frontmatter; confirmed by server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
