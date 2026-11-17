## Description:

Retrieves public Xiaohongshu notes, note details, comments, and creator post lists for trend research, competitor analysis, KOL screening, and content planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, content creators, market researchers, and agent developers use this skill to fetch structured public Xiaohongshu data for topic discovery, competitor monitoring, comment insight, creator tracking, and downstream reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Xiaohongshu keywords, URLs, and the GUAIKEI_API_TOKEN are sent to www.guaikei.com for lookup.

Mitigation: Use only approved inputs and tokens, avoid sensitive data, and rotate the token if logs or request URLs may have exposed it.

Risk: Successful results are saved automatically in local plaintext logs.

Mitigation: Review, protect, redact, or delete the logs/ directory after use when results, URLs, or derived analysis are sensitive.

Risk: The skill is limited to public Xiaohongshu data and can return empty or error results for invalid, private, deleted, or unsupported links.

Mitigation: Validate keyword and URL inputs, use the correct command for the link type, and do not infer or fabricate missing results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/xhs-insight-generate)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and structured JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful command results are saved automatically as plaintext JSON files under logs/.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact source metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
