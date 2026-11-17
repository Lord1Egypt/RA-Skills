## Description:

Analyzes Bilibili video comments and danmaku by collecting public interaction data, extracting sentiment and keywords, and generating a structured Markdown report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unclecheng-li](https://clawhub.ai/user/unclecheng-li)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and content researchers use this skill to summarize audience response on Bilibili videos from public comments and danmaku. It produces a structured report covering interaction volume, sentiment, keywords, timing patterns, and selected popular comments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installers can install unpinned or ambiguous third-party packages into the user's Python environment.

Mitigation: Review dependencies first, use an isolated virtual environment, avoid running install_check.py or install_deps.sh as-is, and install only reviewed pinned packages.

Risk: Generated Markdown can contain untrusted public Bilibili user content from comments and danmaku.

Mitigation: Treat report content as untrusted user-generated text and review it before publishing, rendering in privileged contexts, or using it for decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unclecheng-li/skills/unclecheng-bilibilianalyzer)
- [Bilibili video page](https://www.bilibili.com/)
- [Bilibili video information API](https://api.bilibili.com/x/web-interface/view?bvid={bvid})
- [Bilibili danmaku API](https://api.bilibili.com/x/v1/dm/list.so?oid={cid})
- [Bilibili replies API](https://api.bilibili.com/x/v2/reply/main?next={page}&type=1&oid={bvid}&mode=3)

## Skill Output:

**Output Type(s):** [markdown, analysis, shell commands, guidance]

**Output Format:** [Markdown report with tables, bullet summaries, and command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are based on public Bilibili API responses and may include untrusted public user-generated text.]

## Skill Version(s):

1.0.0 (source: server release metadata and _skillhub_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
