## Description: <br>
Fetch, filter, and summarize RSS/Atom feeds into a clean daily or weekly digest. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zacjiang](https://clawhub.ai/user/zacjiang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to collect RSS or Atom feed items, filter them by recency and keywords, deduplicate entries, and produce daily or weekly digests for monitoring, newsletters, or briefings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts user-provided feed URLs and processes external feed content. <br>
Mitigation: Use reviewed feed lists and treat generated digest text as untrusted external content. <br>
Risk: A selected output path may overwrite an existing file. <br>
Mitigation: Choose output paths carefully and review destination files before running the command. <br>
Risk: The skill requires the feedparser Python package. <br>
Mitigation: Install the dependency only in an environment where adding this package is acceptable. <br>


## Reference(s): <br>
- [RSS Feed Digest on ClawHub](https://clawhub.ai/zacjiang/rss-feed-digest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text digest, with shell command examples for running the feed fetcher] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write the generated digest to stdout or to a user-selected output file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
